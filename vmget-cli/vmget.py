from flask import Flask, render_template, request, jsonify
import os
from yt_dlp import YoutubeDL

app = Flask(__name__)

progress_info = {'progress': 0}

def progress_hook(d):
    if d['status'] == 'downloading':
        progress_info['progress'] = d['_percent_str']

def download_video(url, quality=None, file_format="mp4", output_dir=None):
    if file_format not in ["mp4", "mp3"]:
        return "Unsupported format"

    if not output_dir:
        output_dir = os.getcwd()  # Default to the current directory if no output directory is specified

    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook]
    }

    if file_format == "mp3":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })
    else:
        ydl_opts['format'] = f'bestvideo[height<={quality[:-1]}]+bestaudio/best[height<={quality[:-1]}]'

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    quality = request.form.get('quality')
    file_type = 'mp4' if request.form.get('type') == 'video' else 'mp3'
    
    download_video(url, quality, file_type)
    return jsonify({'message': 'Download complete'})

@app.route('/progress')
def get_progress():
    return jsonify(progress_info)

if __name__ == "__main__":
    app.run(debug=True)
