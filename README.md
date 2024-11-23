
## Project Overview
easy download and access your Content .Supporting Multiple plateforms.
 
## Prerequisites

Before you begin, ensure you have the following installed on your local machine:

- **Node.js**: Required for running the frontend/server.
- **Python 3.10 or later**: Required for the backend and handling media downloads.
- **pip**: Python package manager.
- **npm**: Node.js package manager.
- **ffmpeg**: streamline of video & audio  .
- **Requirements packages**: Upgrade packages only if required .

If you don't have Node.js or Python installed, visit the following pages for installation guides:

- [Install Node.js](https://nodejs.org/)
- [Install Python](https://www.python.org/)

## Installation

Follow these steps to set up the tool on your local machine.

### Setting up Python Environment

1**Create a Virtual Environment**:  
   Open your terminal or command prompt and navigate to the project directory. Then, create a virtual environment.

   ```bash
   cd /path/to/your/project

   # Create the virtual environment
   python -m venv venv

   # Activate the virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate

### Key Points:

- **Step 1**: You first create and activate a virtual environment for Python dependencies.
- **Step 2**: You install the necessary Node.js dependencies (`npm install`), followed by running the dev server (`npm run dev`).
- **Step 3**: You install Python dependencies using `pip install -r requirements.txt` in the `/server` directory.
- **Step 4**: You run the application using either the Python backend (`python your_backend_script.py`) or the frontend/server   Using (`npm run dev`).

Make sure you adjust the file paths or commands based on your actual project structure (e.g., which Python script or server is run by default).

Let me know if you need further modifications!

---

# VMGET
- vmget is a command line tool for downloading videos and audio from youtube by providing links in different qualities.
  
## You can build you own executable file
```bash
pyinstaller --onefile vmget.py
```

```powershell
 PS C:\Users\Abhi> vmget -h
usage: vmget.exe [-h] [-o OUTPUT] url {mp4,mp3} [{360p,480p,720p,1080p}]

YT Video Downloader by [Abhi]

positional arguments:
  url                   URL of the YouTube video
  {mp4,mp3}             Desired file format (mp4 or mp3)
  {360p,480p,720p,1080p}
                        Desired video quality (optional if format is mp3)

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output directory for the downloaded file

Examples:
  python vmget.py "https://www.youtube.com/watch?v=S2sBNY9Wg8o" mp4 720p
  python vmget.py "https://www.youtube.com/watch?v=S2sBNY9Wg8o" mp3 -o C:\Users\Abhi\Downloads

```

# How to setup locally the web of vmget

1. Create python virtual environment
```bash
python -m venv env
```
2. Activate environment & Install dependencies
```bash
./env/Scripts/active
pip install -r requirements.txt
```
3. Run flask app
```bash
flask --app main run
```

> Pull requests are always welcome. 😁
