from config import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid 

class AssetConfig(db.Model):
    __tablename__ = 'asset_config'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    used_or_new = db.Column(db.String(255), nullable=False)
    ansi_or_new = db.Column(db.String(255), nullable=False)
    machine_ownership_type = db.Column(db.String(255), nullable=False)
    battery_type = db.Column(db.String(255), nullable=False)
    engine_serial_no = db.Column(db.String(255), nullable=False)
    two_or_four_wd = db.Column(db.String(255), nullable=False)
    accessories = db.Column(db.String(255), nullable=False)
    tyres = db.Column(db.String(255), nullable=False)
    asset_id = db.Column(UUID(as_uuid=True), db.ForeignKey('asset.id'))