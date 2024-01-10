from config  import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid

class RequestedCompanies(db.Model):
    __tablename__ = 'requested_companies'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    phone_no = db.Column(db.String(255), nullable=False)
    approved = db.Column(db.Boolean, nullable=False)