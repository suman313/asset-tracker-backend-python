from config import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid

class TimeSheet(db.Model):
    __tablename__ = 'time_sheet'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    x_studio_customer = db.Column(db.String(255))
    x_studio_asset_number = db.Column(db.String(255))
    x_studio_time_adjust = db.Column(db.Float(15,2))
    x_studio_serial_no = db.Column(db.String(255))
    x_studio_rental_register_no = db.Column(db.String(200))
    x_studio_day_type = db.Column(db.Enum("WD","HD", name='day_type')) 
    x_studio_time_out = db.Column(db.String(255)) 
    x_studio_total_time = db.Column(db.Float(15,2))
    x_studio_time_in = db.Column(db.String(255)) 
    x_studio_breakdown_time = db.Column(db.String(255)) 
    x_studio_normal_billing_time = db.Column(db.Float(15,2))
    x_studio_nominal_hours = db.Column(db.Float(15,2))
    x_studio_normal_bill_amount = db.Column(db.Float(15,2))
    x_studio_overtime_amount = db.Column(db.Float(15,2))
    x_studio_overtime = db.Column(db.String(255)) 
    x_studio_date = db.Column(db.String(255)) 
    x_studio_model = db.Column(db.String(255))
    x_studio_remarks = db.Column(db.String(255))
    x_studio_reimbursements = db.Column(db.String(255)) 
    x_studio_operator = db.Column(db.Integer)  # may be not working
    x_studio_operator1 = db.Column(db.Integer) 
    x_studio_operator1_name = db.Column(db.String(255))
    x_studio_operator_name = db.Column(db.String(255))
    odoo_id = db.Column(db.Integer) 
    lease_id = db.Column(UUID(as_uuid=True), db.ForeignKey("lease.id"))
    asset_id = db.Column(UUID(as_uuid=True), db.ForeignKey("asset.id"))
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey("company.id"))
    operator_id = db.Column(UUID(as_uuid=True), db.ForeignKey("operator.id"))
    operator2_id = db.Column(db.String(255))
    
