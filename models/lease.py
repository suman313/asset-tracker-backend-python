from config import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid
 




class Lease(db.Model):
    __tablename__ = 'lease'
    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    lease_type = db.Column(db.String(255), nullable=False)
    customer_po_no = db.Column(db.String(255), nullable=False)
    currency = db.Column(db.String(255), nullable=False)
    rental_start_date = db.Column(db.String(255), nullable=False)
    rental_end_date = db.Column(db.String(255), nullable=False)
    customer = db.Column(db.String(255), nullable=False)
    lease_status = db.Column(db.String(255), nullable=False, default="active")
    contract_value = db.Column(db.String(255), nullable=False)
    transportation_charge = db.Column(db.String(255), nullable=False)
    normal_amount = db.Column(db.String(255), nullable=False)
    overtime_amount = db.Column(db.String(255), nullable=False)
    reimbursements = db.Column(db.String(255), nullable=False)
    total_claimable_amount = db.Column(db.String(255), nullable=False)
    x_studio_rental_register_mask_no = db.Column(db.Integer)
    x_studio_rental_register_no = db.Column(db.Integer)
    x_currency_id = db.Column(db.Integer) 
    odoo_mask_order_id = db.Column(db.Integer)
    odoo_order_id = db.Column(db.String(255))
    asset_id = db.Column(UUID(as_uuid=True), db.ForeignKey('asset.id'), nullable=False)
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey('company.id'), nullable=True)
    fild_id = db.Column(db.String(255), nullable=False) 
    attachment = db.relationship("Attachment", backref="lease")
    photo = db.relationship("Photo", backref="lease")
    maintenance = db.relationship('Maintenance', backref='lease')
    invoice = db.relationship('Invoice', backref='lease')
    lease_operator_mapping = db.relationship('Lease_Operator_Mapping', backref="lease")
    lease_map = db.relationship('Lease_map', backref="lease")
    time_sheet = db.relationship("TimeSheet", backref="lease")