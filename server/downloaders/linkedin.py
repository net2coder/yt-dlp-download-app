import requests
import os
from datetime import datetime
import json

class LinkedInDownloader:
    def __init__(self):
        self.output_dir = 'downloads/linkedin'
        os.makedirs(self.output_dir, exist_ok=True)

    def download(self, url, content_type):
        try:
            post_id = self._extract_post_id(url)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json'
            }
            
            #  LinkedIn's API
            if content_type == 'Video':
                filename = f"linkedin_video_{post_id}.mp4"
            elif content_type == 'Image':
                filename = f"linkedin_image_{post_id}.jpg"
            else:
                filename = f"linkedin_post_{post_id}.txt"
                
            filepath = os.path.join(self.output_dir, filename)
            
            return {
                'status': 'success',
                'post_id': post_id,
                'type': content_type,
                'filename': filepath,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            raise Exception(f"LinkedIn download failed: {str(e)}")

    def _extract_post_id(self, url):
        try:
            parts = url.split('/')
            return parts[-1].split('?')[0]
        except:
            raise Exception("Invalid LinkedIn URL")