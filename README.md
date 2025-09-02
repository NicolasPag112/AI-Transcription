# AI-Transcription

AI-Transcription is a Python program that automatically transcribes audio and video files into text using OpenAI's Whisper model.  
It supports multiple languages and works on both Windows and Linux.

## Features
- Transcribes audio files (`.wav`, `.mp3`, `.flac`) and video files (`.mp4`, `.avi`, `.mov`, `.mkv`)
- Automatically extracts audio from video files
- Easy model and language selection via popup
- Organizes files and transcriptions in dedicated folders

## Usage Tips
- Place your audio files in `Files/Audios` and video files in `Files/Videos`
- Run `run.py` to set up the environment and start the program
- Transcriptions are saved in the `Transcriptions` folder
- Make sure you have Python installed
- The program will automatically download and set up FFmpeg if needed

## Requirements
- Python

## Quick Start
1. Clone the repository
2. Place your media files in the appropriate folders
3. Run:
   ```
   python run.py
   ```
4. Follow the prompts to select model and language

## Notes
- For best results, use clear audio/video files
- Python 3.13+ is recommended (not tested on older versions yet)
- Linux version may have some problem, only tested on Windows yet
