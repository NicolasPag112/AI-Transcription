import sys
import subprocess
import platform
import importlib.util
import urllib.request
import os
import zipfile
import tarfile

REQUIRED_LIBS = ['librosa', 'whisper']

def create_venv(venv_path):
    print("Creating virtual environment...")
    subprocess.check_call([sys.executable, "-m", "venv", venv_path])
    print("Virtual environment created.")

def get_venv_python(venv_path):
    if platform.system() == "Windows":
        return os.path.join(venv_path, "Scripts", "python.exe")
    else:
        return os.path.join(venv_path, "bin", "python")

def install_libs(venv_python):
    requirements_path = os.path.join(os.getcwd(), "requirements.txt")
    if os.path.exists(requirements_path):
        print("Installing libraries from requirements.txt...")
        subprocess.check_call([venv_python, "-m", "pip", "install", "-r", requirements_path])
    else:
        print("Warning: requirements.txt not found. Skipping library installation.")

def extract_archive(archive_path, extract_to, os_type):
    if os_type == 'Windows':
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print("Archive extracted (zip).")
    elif os_type == 'Linux':
        with tarfile.open(archive_path, 'r:xz') as tar_ref:
            tar_ref.extractall(extract_to)
        print("Archive extracted (tar.xz).")

def ensure_directories():
    files_dir = os.path.join(os.getcwd(), "Files")
    audios_dir = os.path.join(files_dir, "Audios")
    videos_dir = os.path.join(files_dir, "Videos")

    for folder in [files_dir, audios_dir, videos_dir]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created missing folder: {folder}")

def main():
    # Check and create virtual environment
    venv_path = os.path.join(os.getcwd(), ".venv")
    if not os.path.exists(venv_path):
        create_venv(venv_path)
        venv_python = get_venv_python(venv_path)
        install_libs(venv_python)
    else:
        venv_python = get_venv_python(venv_path)

    # Ensure Files/Audios/Videos folders exist
    ensure_directories()

    # Check OS and set download URL and archive name
    os_type = platform.system()
    if os_type == 'Windows':
        ffmpeg_folder = "ffmpeg-master-latest-win64-gpl-shared"
        github_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl-shared.zip"
        archive_path = os.path.join(os.getcwd(), "ffmpeg-master-latest-win64-gpl-shared.zip")
    elif os_type == 'Linux':
        ffmpeg_folder = "ffmpeg-master-latest-linux64-gpl"
        github_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz"
        archive_path = os.path.join(os.getcwd(), "ffmpeg-master-latest-linux64-gpl.tar.xz")
    else:
        print("Error: Unsupported operating system. Only Windows and Linux are supported.")
        sys.exit(1)

    # Download and extract only if folder does not exist
    if not os.path.exists(os.path.join(os.getcwd(), ffmpeg_folder)):
        print(f"{ffmpeg_folder} not found. Downloading archive from {github_url}...")
        urllib.request.urlretrieve(github_url, archive_path)
        print("Download complete.")
        extract_archive(archive_path, os.getcwd(), os_type)
        os.remove(archive_path)
        print(f"Archive {archive_path} deleted after extraction.")

    # Run main program
    subprocess.run([sys.executable, "src/main.py"])

if __name__ == "__main__":
    main()