import requests
import os
from datetime import datetime
import json

class TwitterDownloader:
    def __init__(self):
        self.output_dir = 'downloads/twitter'
        os.makedirs(self.output_dir, exist_ok=True)

    def download(self, url, quality):
        try:
            tweet_id = self._extract_tweet_id(url)
            headers = {
                'Authorization': f'Bearer {os.getenv("TWITTER_BEARER_TOKEN")}',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            #  Twitter's API v2
            
            
            filename = f"tweet_{tweet_id}_{quality}.mp4"
            filepath = os.path.join(self.output_dir, filename)
            
            return {
                'status': 'success',
                'tweet_id': tweet_id,
                'quality': quality,
                'filename': filepath,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            raise Exception(f"Twitter download failed: {str(e)}")

    def _extract_tweet_id(self, url):
        try:
            parts = url.split('/')
            return parts[-1].split('?')[0]
        except:
            raise Exception("Invalid Twitter URL")