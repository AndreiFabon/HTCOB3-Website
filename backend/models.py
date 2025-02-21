from datetime import datetime
from . import db
from sqlalchemy.sql import func

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    points = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Flag(db.Model):
    __tablename__ = 'flags'
    id = db.Column(db.Integer, primary_key=True)
    flag = db.Column(db.String(255), unique=True, nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)  # "easy", "medium", or "hard"
    points = db.Column(db.Integer, nullable=False)

class FlagSubmission(db.Model):
    __tablename__ = 'flag_submissions'
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    flag_id = db.Column(db.Integer, db.ForeignKey('flags.id'), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint('team_id', 'flag_id', name='unique_team_flag'),)

