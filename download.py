import sys
import yt_dlp

def download_video(url):
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',  # Set the download filename template
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python download.py <video_url>")
        sys.exit(1)

    video_url = sys.argv[1]
    print(f"Downloading video from: {video_url}")
    download_video(video_url)
