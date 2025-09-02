import os
import librosa
import subprocess
import platform
import sys
import tkinter as tk
from tkinter import simpledialog
from transcriber import Transcriber

def select_model_weight_and_language():
    root = tk.Tk()
    root.withdraw()
    options = ['small', 'medium', 'large']
    weight = simpledialog.askstring("Model Selection", f"Choose model weight ({', '.join(options)}):", initialvalue='base')
    if weight not in options:
        print("Invalid selection. Using 'base'.")
        weight = 'base'
    language = simpledialog.askstring("Language Selection", "Enter language code (e.g., 'en', 'pt', 'es'):", initialvalue='en')
    root.destroy()
    return weight, language

def get_media_files(directory, audio_exts, video_exts):
    audio_files = []
    video_files = []
    for file in os.listdir(directory):
        if file.endswith(audio_exts):
            audio_files.append(os.path.join(directory, file))
        elif file.endswith(video_exts):
            video_files.append(os.path.join(directory, file))
    return audio_files, video_files

def extract_audio_from_video(video_path, output_audio_path, ffmpeg_path):
    command = [
        ffmpeg_path,
        '-i', video_path,
        '-vn',
        '-acodec', 'pcm_s16le',
        '-ar', '16000',
        '-ac', '1',
        output_audio_path
    ]
    subprocess.run(command, check=True)

def main():
    # Get the directory of the current script
    base_dir = os.path.dirname(__file__) # Main.py directory path
    files_dir = os.path.join(base_dir, '..', 'Files') # Files directory path
    audios_dir = os.path.join(files_dir, 'Audios') # Audios directory path
    videos_dir = os.path.join(files_dir, 'Videos') # Videos directory path
    transcript_directory = os.path.join(base_dir, '..', 'Transcriptions') # Transcriptions directory path

    if platform.system() == 'Windows':
         # Windows ffmpeg path
        ffmpeg_path = os.path.join(base_dir, '..', 'ffmpeg-master-latest-win64-gpl-shared', 'bin', 'ffmpeg.exe')
    elif platform.system() == 'Linux':
        # Linux ffmpeg path
        ffmpeg_path = os.path.join(base_dir, '..', 'ffmpeg-master-latest-linux64-gpl', 'bin', 'ffmpeg')
    else:
        ffmpeg_path = None
        print("Error: Unsupported operating system. Only Windows and Linux are supported.")
        sys.exit(1)

    

    # Popup for model and language selection
    model_weight, language = select_model_weight_and_language()

    if not os.path.exists(transcript_directory):
        os.makedirs(transcript_directory)

    audio_exts = ('.wav', '.mp3', '.flac')
    video_exts = ('.mp4', '.avi', '.mov', '.mkv')

    # Collect audio files
    audio_files, _ = get_media_files(audios_dir, audio_exts, video_exts)
    # Collect video files
    _, video_files = get_media_files(videos_dir, audio_exts, video_exts)
    print(f"Found {len(audio_files)} audio files and {len(video_files)} video files.")

    # Initialize transcriber
    transcriber = Transcriber(weight=model_weight)

    # Transcribe audio files
    for audio_path in audio_files:
        audio_file = os.path.basename(audio_path)
        print(f'Loading {audio_file}...')
        audio_data, sr = librosa.load(audio_path, sr=None)
        print(f'Transcribing {audio_file}...')
        transcribed_text = transcriber.transcribe_audio(audio_data, language=language)

        # Replace commas with line breaks
        transcribed_text = transcribed_text.replace(',', '\n')

        transcript_file = os.path.join(transcript_directory, f'{os.path.splitext(audio_file)[0]}.txt')
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(transcribed_text)
        print(f'Transcription saved to {transcript_file}')

    # Extract audio from videos and transcribe
    for video_path in video_files:
        video_file = os.path.basename(video_path)
        audio_output = os.path.join(transcript_directory, f'{os.path.splitext(video_file)[0]}_audio.wav')
        print(f'Extracting audio from {video_file}...')
        extract_audio_from_video(video_path, audio_output, ffmpeg_path)
        print(f'Loading extracted audio from {video_file}...')
        audio_data, sr = librosa.load(audio_output, sr=None)
        print(f'Transcribing {video_file}...')
        transcribed_text = transcriber.transcribe_audio(audio_data, language=language)

        # Replace commas with line breaks
        transcribed_text = transcribed_text.replace(',', '\n')

        transcript_file = os.path.join(transcript_directory, f'{os.path.splitext(video_file)[0]}.txt')
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(transcribed_text)
        print(f'Transcription saved to {transcript_file}')

if __name__ == '__main__':
    main()