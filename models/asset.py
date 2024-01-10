from config import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid
import time
  
class Asset(db.Model):
    __tablename__ = 'asset'
    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    asset_no = db.Column(db.String(255), nullable=False)
    make = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    serial_no = db.Column(db.String(255), nullable=False)
    purchased_from = db.Column(db.String(255), nullable=False)
    site_location = db.Column(db.String(255), nullable=False)
    yom = db.Column(db.String(255), nullable=False)
    rfid = db.Column(db.String(255))
    device_hash = db.Column(db.String(255) )
    device_id = db.Column(db.String(255))
    platform = db.Column(db.String(255))
    group = db.Column(db.String(255))
    created_at = db.Column(db.String(255), nullable=False, default=time.time())
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey('company.id'), nullable=True)
    fild_id = db.Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4) 
    updated_at = db.Column(db.String(255), default=time.time())
    asset_config = db.relationship('AssetConfig', backref='asset')
    maintenance = db.relationship('Maintenance', backref='asset')
    lease = db.relationship('Lease', backref='asset')
    commercial_details = db.relationship('CommercialDetail', backref='asset')
    attachment = db.relationship("Attachment", backref="asset")
    photo = db.relationship("Photo", backref="asset")
    time_sheet = db.relationship("TimeSheet", backref="asset")