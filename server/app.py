from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import jwt
import bcrypt
import os
from dotenv import load_dotenv
import traceback
from downloaders.youtube import YouTubeDownloader
from downloaders.instagram import InstagramDownloader
from downloaders.pinterest import PinterestDownloader
from downloaders.linkedin import LinkedInDownloader
from downloaders.twitter import TwitterDownloader
from downloaders.snapchat import SnapchatDownloader
from models.user import User, db
from models.download import Download
from models.contact import Contact
from bot.telegram_bot import TelegramBot
import threading
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///vmget.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-length

db.init_app(app)

# Initialize and start Telegram bot in a separate thread
def start_telegram_bot():
    try:
        bot = TelegramBot()
        bot.run()
    except Exception as e:
        logger.error(f"Telegram bot error: {str(e)}")
 
# Start bot in thread
bot_thread = threading.Thread(target=start_telegram_bot)
bot_thread.daemon = True
bot_thread.start()
        

# Ensure the downloads directory exists
os.makedirs('downloads', exist_ok=True)
for platform in ['youtube', 'instagram', 'pinterest', 'linkedin', 'twitter', 'snapchat']:
    os.makedirs(f'downloads/{platform}', exist_ok=True)

with app.app_context():
    db.create_all()

def get_current_user():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return User.query.get(payload['user_id'])
    except:
        return None

def handle_download_error(e: Exception) -> Response:
    error_msg = str(e)
    logger.error(f"Download error: {error_msg}")
    logger.error(traceback.format_exc())
    return jsonify({
        'error': error_msg,
        'status': 'error',
        'details': traceback.format_exc()
    }), 400

def log_download(user_id, url, platform, format_type, status='completed'):
    try:
        download = Download(
            user_id=user_id,
            url=url,
            platform=platform,
            format=format_type,
            status=status,
            completed_at=datetime.utcnow() if status == 'completed' else None
        )
        db.session.add(download)
        db.session.commit()
    except Exception as e:
        logger.error(f"Error logging download: {str(e)}")
        db.session.rollback()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        
        new_user = User(
            name=data['name'],
            email=data['email'],
            password=hashed_password
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        token = jwt.encode(
            {'user_id': new_user.id, 'exp': datetime.utcnow() + timedelta(days=1)},
            app.config['JWT_SECRET_KEY']
        )
        
        return jsonify({
            'token': token,
            'user': {
                'id': new_user.id,
                'name': new_user.name,
                'email': new_user.email
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user.password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        token = jwt.encode(
            {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(days=1)},
            app.config['JWT_SECRET_KEY']
        )
        
        return jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
        })
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/download/youtube', methods=['POST'])
def youtube_download():
    try:
        data = request.get_json()
        if not data or 'url' not in data or 'format' not in data:
            return jsonify({'error': 'Missing required parameters'}), 400

        user = get_current_user()
        downloader = YouTubeDownloader()
        result = downloader.download(data['url'], data['format'])
        
        if user:
            log_download(user.id, data['url'], 'youtube', data['format'])
        
        if not os.path.exists(result['filename']):
            return jsonify({'error': 'Download failed - file not found'}), 400

        return send_file(
            result['filename'],
            as_attachment=True,
            download_name=os.path.basename(result['filename'])
        )
    except Exception as e:
        return handle_download_error(e)

@app.route('/api/download/instagram', methods=['POST'])
def instagram_download():
    try:
        data = request.get_json()
        if not data or 'url' not in data or 'type' not in data:
            return jsonify({'error': 'Missing required parameters'}), 400

        user = get_current_user()
        downloader = InstagramDownloader()
        result = downloader.download(data['url'], data['type'])
        
        if user:
            log_download(user.id, data['url'], 'instagram', data['type'])
            
        return jsonify(result)
    except Exception as e:
        return handle_download_error(e)

@app.route('/api/download/pinterest', methods=['POST'])
def pinterest_download():
    try:
        data = request.get_json()
        if not data or 'url' not in data or 'quality' not in data:
            return jsonify({'error': 'Missing required parameters'}), 400

        user = get_current_user()
        downloader = PinterestDownloader()
        result = downloader.download(data['url'], data['quality'])
        
        if user:
            log_download(user.id, data['url'], 'pinterest', data['quality'])
        
        if not os.path.exists(result['filename']):
            return jsonify({'error': 'Download failed - file not found'}), 400

        return send_file(
            result['filename'],
            as_attachment=True,
            download_name=os.path.basename(result['filename'])
        )
    except Exception as e:
        return handle_download_error(e)

@app.route('/api/download/linkedin', methods=['POST'])
def linkedin_download():
    try:
        data = request.get_json()
        if not data or 'url' not in data or 'type' not in data:
            return jsonify({'error': 'Missing required parameters'}), 400

        user = get_current_user()
        downloader = LinkedInDownloader()
        result = downloader.download(data['url'], data['type'])
        
        if user:
            log_download(user.id, data['url'], 'linkedin', data['type'])
        
        if not os.path.exists(result['filename']):
            return jsonify({'error': 'Download failed - file not found'}), 400

        return send_file(
            result['filename'],
            as_attachment=True,
            download_name=os.path.basename(result['filename'])
        )
    except Exception as e:
        return handle_download_error(e)

@app.route('/api/download/twitter', methods=['POST'])
def twitter_download():
    try:
        data = request.get_json()
        if not data or 'url' not in data or 'quality' not in data:
            return jsonify({'error': 'Missing required parameters'}), 400

        user = get_current_user()
        downloader = TwitterDownloader()
        result = downloader.download(data['url'], data['quality'])
        
        if user:
            log_download(user.id, data['url'], 'twitter', data['quality'])
        
        if not os.path.exists(result['filename']):
            return jsonify({'error': 'Download failed - file not found'}), 400

        return send_file(
            result['filename'],
            as_attachment=True,
            download_name=os.path.basename(result['filename'])
        )
    except Exception as e:
        return handle_download_error(e)

@app.route('/api/download/snapchat', methods=['POST'])
def snapchat_download():
    try:
        data = request.get_json()
        if not data or 'url' not in data or 'type' not in data:
            return jsonify({'error': 'Missing required parameters'}), 400

        user = get_current_user()
        downloader = SnapchatDownloader()
        result = downloader.download(data['url'], data['type'])
        
        if user:
            log_download(user.id, data['url'], 'snapchat', data['type'])
        
        if not os.path.exists(result['filename']):
            return jsonify({'error': 'Download failed - file not found'}), 400

        return send_file(
            result['filename'],
            as_attachment=True,
            download_name=os.path.basename(result['filename'])
        )
    except Exception as e:
        return handle_download_error(e)


@app.route('/api/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()
        
        new_contact = Contact(
            name=data['name'],
            email=data['email'],
            subject=data['subject'],
            message=data['message']
        )
        
        db.session.add(new_contact)
        db.session.commit()
        
        # In a production environment, you might want to send an email notification here
        logger.info(f"New contact message from {data['email']}: {data['subject']}")
        
        return jsonify({
            'status': 'success',
            'message': 'Contact message sent successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Contact form error: {str(e)}")
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/api/user/downloads', methods=['GET'])
def get_user_downloads():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        downloads = Download.query.filter_by(user_id=user.id).order_by(Download.created_at.desc()).all()
        return jsonify({
            'downloads': [{
                'id': d.id,
                'url': d.url,
                'platform': d.platform,
                'format': d.format,
                'status': d.status,
                'created_at': d.created_at.isoformat(),
                'completed_at': d.completed_at.isoformat() if d.completed_at else None
            } for d in downloads]
        })
    except Exception as e:
        logger.error(f"Error fetching user downloads: {str(e)}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)