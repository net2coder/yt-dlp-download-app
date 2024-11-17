import instaloader
import os
from datetime import datetime

class InstagramDownloader:
    def __init__(self):
        self.output_dir = 'downloads/instagram'
        os.makedirs(self.output_dir, exist_ok=True)
        self.L = instaloader.Instaloader(
            dirname_pattern=self.output_dir,
            download_videos=True,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False
        )

    def download(self, url, content_type):
        try:
            shortcode = self._extract_shortcode(url)
            post = instaloader.Post.from_shortcode(self.L.context, shortcode)
            
            if content_type == 'Story' and post.is_video:
                self.L.download_stories([post.owner_username])
            elif content_type in ['Video', 'Reel'] and post.is_video:
                self.L.download_post(post, target='video')
            elif content_type == 'Image':
                self.L.download_post(post, target='image')
            elif content_type == 'Highlight':
                self.L.download_highlights(post.owner_username)
            
            return {
                'status': 'success',
                'type': content_type,
                'username': post.owner_username,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            raise Exception(f"Instagram download failed: {str(e)}")

    def _extract_shortcode(self, url):
        # Extract the shortcode from Instagram URL
        parts = url.split('/')
        return parts[-2] if parts[-1] == '' else parts[-1]