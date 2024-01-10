from config import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Phone(db.Model):
    __tablename__ = 'phone'
    id = db.Column(UUID(as_uuid=True), primary_key=True,  default=uuid.uuid4)
    types = db.Column(db.String(255), nullable=False)
    phone_no = db.Column(db.String(255), nullable=False)
    operator_id = db.Column(UUID(as_uuid=True), db.ForeignKey('operator.id'), nullable=False)

    