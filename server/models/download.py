from datetime import datetime
from .user import db

class Download(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    format = db.Column(db.String(50))
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    file_path = db.Column(db.String(500))

    def __repr__(self):
        return f'<Download {self.platform}:{self.id}>'