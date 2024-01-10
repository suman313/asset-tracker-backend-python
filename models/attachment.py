from config import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Attachment(db.Model):
    __tablename__ = 'attachment'
    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    serial_no = db.Column(db.String(255), nullable=False)
    types = db.Column(db.String(255), nullable=False)
    doc_uri = db.Column(db.String(255), nullable=False)
    doc_expiry_date = db.Column(db.String(255), nullable=False)
    archive_flag = db.Column(db.Boolean, nullable=False)
    asset_id = db.Column(UUID(as_uuid=True), db.ForeignKey("asset.id"), nullable=True)
    maintenance_id = db.Column(UUID(as_uuid=True), db.ForeignKey("maintenance.id"), nullable=True)
    lease_id = db.Column(UUID(as_uuid=True), db.ForeignKey("lease.id"), nullable=True)
