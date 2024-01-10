from config import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid 

class Maintenance(db.Model):
    __tablename__ = 'maintenance'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    scheduled_date = db.Column(db.String(255), nullable=False)
    types = db.Column(db.String(255), nullable=False)
    asset_name = db.Column(db.String(255), nullable=False)
    asset_no = db.Column(db.String(255), nullable=False)
    asset_id = db.Column(UUID(as_uuid=True), db.ForeignKey('asset.id'), nullable=False)
    lease_id = db.Column(UUID(as_uuid=True), db.ForeignKey('lease.id'), nullable=True)
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey('company.id'), nullable=True)
    fild_id = db.Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4) 
    attachment = db.relationship("Attachment", backref="maintenance")
    parts =  db.relationship("Parts", backref="maintenance") 
    photo = db.relationship("Photo", backref="maintenance")