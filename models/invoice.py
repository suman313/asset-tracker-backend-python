from config import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Invoice(db.Model):
        __table_name__ = 'invioce'
        id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        invoice_no= db.Column(db.String(255), nullable=False)
        invoice_date = db.Column(db.String(255), nullable=False)
        invoice_name = db.Column(db.String(255), nullable=False) 
        operator_name = db.Column(db.String(255), nullable=False)
        documents_link = db.Column(db.String(255), nullable=False)
        lease_id = db.Column(UUID(as_uuid=True), db.ForeignKey('lease.id'), nullable=True)
        company_id = db.Column(UUID(as_uuid=True), db.ForeignKey('company.id'), nullable=True)
        