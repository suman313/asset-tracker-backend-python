from config import db 
from sqlalchemy.dialects.postgresql import UUID 
import uuid

class Photo(db.Model):
    __tablename__ = 'photo'
    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    image_uri = db.Column(db.String(355), nullable=False)
    asset_id = db.Column(UUID(as_uuid=True), db.ForeignKey("asset.id"), nullable=True)
    maintenance_id = db.Column(UUID(as_uuid=True), db.ForeignKey("maintenance.id"), nullable=True)
    lease_id = db.Column(UUID(as_uuid=True), db.ForeignKey("lease.id"), nullable=True)
    operator_id = db.Column(UUID(as_uuid=True), db.ForeignKey("operator.id"), nullable=True)