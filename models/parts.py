from config import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Parts (db.Model):
    __tablename__ = 'parts'
    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    part_no = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.String(255), nullable=False)
    price = db.Column(db.String(255), nullable=False)
    installation = db.Column(db.Boolean, nullable=False)
    maintenance_id = db.Column(UUID(as_uuid=True), db.ForeignKey('maintenance.id'), nullable=False, default=False)
