from config import db 
from sqlalchemy.dialects.postgresql import UUID 
import uuid

class BankDetails(db.Model):
    __tablename__ = 'bank_details'
    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    account_no = db.Column(db.String(255), nullable=False)
    ifsc_code = db.Column(db.String(255), nullable=False)
    operator_id = db.Column(UUID(as_uuid=True), db.ForeignKey('operator.id'), nullable=False)