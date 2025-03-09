# Project Setup Guide

This guide provides instructions to set up and run the backend and frontend for the project.

---

## Prerequisites
Make sure you have the following installed:
- Python 3.8+
- Node.js & PNPM
- FFmpeg (for Whisper backend)
- Git (optional but recommended)

---

## Backend Setup (Flask)

### 1. Clone the Repository
```sh
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

### 2. Create a Virtual Environment
```sh
python -m venv venv
```

### 3. Activate Virtual Environment
#### Windows:
```sh
venv\Scripts\activate
```
#### macOS/Linux:
```sh
source venv/bin/activate
```

### 4. Install Dependencies
```sh
pip install -r requirements.txt
```

### 5. Ensure FFmpeg is Installed (Required for Whisper)
#### Windows (Using Chocolatey)
```sh
choco install ffmpeg
```
#### macOS (Using Homebrew)
```sh
brew install ffmpeg
```
#### Linux (Debian/Ubuntu)
```sh
sudo apt update && sudo apt install ffmpeg
```

### 6. Run the Backend Server
```sh
python -m s2s_back.main
```
OR use the provided startup script:
```sh
start.bat  # Windows
./start.sh # macOS/Linux
```

---

## Frontend Setup (Svelte)

### 1. Navigate to the Frontend Directory
```sh
cd frontend
```

### 2. Install Dependencies
```sh
pnpm install
```

### 3. Run the Development Server
```sh
pnpm run dev --open
```
This will open the Svelte app in your default browser.

---

## Troubleshooting
- If you face `ModuleNotFoundError`, ensure all dependencies are installed correctly.
- If FFmpeg-related errors occur, make sure FFmpeg is correctly installed and added to the system PATH.
- If the backend fails to start, check the error logs and ensure all necessary environment variables are set.

---

## Contributing
Feel free to fork the repository and submit pull requests with improvements or bug fixes!

---



