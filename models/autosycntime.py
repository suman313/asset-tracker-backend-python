from config import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime


class AutoSycnTime(db.Model):
    __tablename__ = "autosycntime"
    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    date = db.Column(db.String(255), nullable=False)
    section = db.Column(db.String(255))
    created_at = db.Column(db.String(255), nullable=False, default=datetime.datetime.now())