import requests
import os
from datetime import datetime
import json
import re

class PinterestDownloader:
    def __init__(self):
        self.output_dir = 'downloads/pinterest'
        os.makedirs(self.output_dir, exist_ok=True)

    def download(self, url, quality):
        try:
            pin_id = self._extract_pin_id(url)
            # API URL to get pin data
            api_url = f"https://api.pinterest.com/v3/pins/{pin_id}/"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(api_url, headers=headers)
            # Check for valid response
            if response.status_code != 200:
                raise Exception(f"Failed to fetch data from Pinterest API: HTTP {response.status_code}")

            data = response.json()
            
            # Ensure we have valid data from the response
            if 'resource_response' in data and 'data' in data['resource_response']:
                pin_data = data['resource_response']['data']
                image_url = self._get_image_url(pin_data, quality)
                
                if image_url:
                    filename = f"pin_{pin_id}_{quality}.jpg"
                    filepath = os.path.join(self.output_dir, filename)
                    
                    
                    image_response = requests.get(image_url, headers=headers)
                    if image_response.status_code == 200:
                        with open(filepath, 'wb') as f:
                            f.write(image_response.content)
                    
                    return {
                        'status': 'success',
                        'pin_id': pin_id,
                        'quality': quality,
                        'filename': filepath,
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    raise Exception("Could not find image data for the given quality.")
            else:
                raise Exception("Pinterest API response did not contain expected data.")
        except Exception as e:
            raise Exception(f"Pinterest download failed: {str(e)}")

    def _extract_pin_id(self, url):
        # Handle both short (https://pin.it/{pin_id}) and full URLs (https://www.pinterest.com/pin/{pin_id}/)
        pin_url_pattern = r"https://(?:pin\.it|www\.pinterest\.com/pin)/([\w\d]+)"
        
        match = re.match(pin_url_pattern, url)
        if match:
            return match.group(1)
        
        raise Exception("Invalid Pinterest URL format. Could not extract pin ID.")

    def _get_image_url(self, pin_data, quality):
        quality_map = {
            'Original Quality': 'original',
            'High Quality': 'high',
            'Medium Quality': 'medium'
        }
        
        if 'images' in pin_data and quality in quality_map:
            quality_key = quality_map[quality]
            if quality_key in pin_data['images']:
                return pin_data['images'][quality_key]['url']
        
        return None
