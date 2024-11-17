import yt_dlp
import os
from datetime import datetime

class YouTubeDownloader:
    def __init__(self):
        self.output_dir = 'downloads/youtube'
        os.makedirs(self.output_dir, exist_ok=True)

    def download(self, url, format_type):
        try:
            options = {
                'format': self._get_format_option(format_type),
                'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
                'progress_hooks': [self._progress_hook],
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }

            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                # Handle the case where the file extension might change
                if format_type == 'MP3 Audio':
                    base, _ = os.path.splitext(filename)
                    filename = f"{base}.mp3"
                
                if not os.path.exists(filename):
                    raise Exception("Download failed - file not created")

                return {
                    'status': 'success',
                    'title': info['title'],
                    'filename': filename,
                    'format': format_type,
                    'filesize': os.path.getsize(filename)
                }
        except Exception as e:
            raise Exception(f"YouTube download failed: {str(e)}")

    def _get_format_option(self, format_type):
        format_options = {
            'MP4 - 1080p': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best',
            'MP4 - 720p': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best',
            'MP4 - 480p': 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best',
            'MP3 Audio': 'bestaudio/best'
        }
        return format_options.get(format_type, 'best')

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                progress = float(d['downloaded_bytes']) / float(d['total_bytes']) * 100
                print(f"Download Progress: {progress:.1f}%")
            except:
                pass  # Skip progress for unknown total size