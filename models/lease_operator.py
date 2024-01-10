from config import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Lease_Operator_Mapping(db.Model):
        __tablename__ = "lease_operator_mapping"
        id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
        operator_name = db.Column(db.String(255), nullable=False)
        company_id = db.Column(UUID(as_uuid=True), db.ForeignKey("company.id"), nullable=False)
        operator_id = db.Column(UUID(as_uuid=True), db.ForeignKey('operator.id'), nullable=False)
        lease_id = db.Column(UUID(as_uuid=True), db.ForeignKey('lease.id'), nullable=False)
        