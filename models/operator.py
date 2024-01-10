from config import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid 

class Operator(db.Model): 
    __tablename__ = 'operator'
    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    aadhar_no = db.Column(db.String(255), nullable=False, unique=True)
    joining_date = db.Column(db.String(255), nullable=False)
    termination_date = db.Column(db.String(255))
    net_inhand_salary = db.Column(db.String(255), nullable=False)
    pf_account_no = db.Column(db.String(255), nullable=False)
    fild_id = db.Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4) 
    odoo_operator_mask_id = db.Column(db.String(255))
    odoo_employee_no = db.Column(db.String(255))
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey('company.id'), nullable=True)
    bank_details = db.relationship("BankDetails", backref="operator") 
    phone = db.relationship("Phone", backref="operator")
    photo = db.relationship("Photo", backref="operator")
    lease_operator_mapping = db.relationship("Lease_Operator_Mapping", backref="operator")
    time_sheet = db.relationship("TimeSheet", backref="operator")