import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SnapchatDownloader:
    def __init__(self):
        self.output_dir = 'downloads/snapchat'
        os.makedirs(self.output_dir, exist_ok=True)

    def download(self, url, content_type):
        try:
            story_id = self._extract_story_id(url)
            snapchat_api_key = os.getenv("SNAPCHAT_API_KEY")
            snapchat_session_token = os.getenv("SNAPCHAT_SESSION_TOKEN")
            
            if not snapchat_api_key or not snapchat_session_token:
                raise Exception("Snapchat API credentials missing")

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json',
                'Authorization': f'Bearer {snapchat_session_token}'  # Assuming token-based auth
            }
            
            if content_type == 'Story':
                media_url = self._get_media_url(story_id, 'story', snapchat_api_key, headers)
                filename = f"snap_story_{story_id}.mp4"
            elif content_type == 'Spotlight':
                media_url = self._get_media_url(story_id, 'spotlight', snapchat_api_key, headers)
                filename = f"snap_spotlight_{story_id}.mp4"
            else:
                
                media_url = self._get_media_url(story_id, 'photo', snapchat_api_key, headers)
                filename = f"snap_{story_id}.jpg"
            
            filepath = os.path.join(self.output_dir, filename)

      
            self._download_media(media_url, filepath)

            return {
                'status': 'success',
                'story_id': story_id,
                'type': content_type,
                'filename': filepath,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            raise Exception(f"Snapchat download failed: {str(e)}")

    def _extract_story_id(self, url):
        try:
            
            parts = url.split('/')
            return parts[-1].split('?')[0]
        except Exception as e:
            raise Exception("Invalid Snapchat URL format")

    def _get_media_url(self, story_id, content_type, api_key, headers):
       
        try:
            url = f'https://api.snapchat.com/v1/media/{content_type}/{story_id}'  # Example URL (replace with actual endpoint)
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise Exception(f"Error fetching media URL: {response.text}")

            media_data = response.json()  
            if 'media_url' not in media_data:
                raise Exception(f"Media URL not found in the response")
            return media_data['media_url']

        except Exception as e:
            raise Exception(f"Error fetching media URL: {str(e)}")

    def _download_media(self, media_url, filepath):
        """ Download the media file to the specified path. """
        try:
            response = requests.get(media_url, stream=True)
            response.raise_for_status()  # Check for request success
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print(f"Media saved as {filepath}")
        except Exception as e:
            raise Exception(f"Error downloading media: {str(e)}")
