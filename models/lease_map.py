from config import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Lease_map(db.Model):
    __tablename__ = 'lease_map'
    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    sale_person = db.Column(db.String(255), nullable=False)
    lease_id = db.Column(UUID(as_uuid=True), db.ForeignKey('lease.id'), nullable=False)