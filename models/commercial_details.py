from config  import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid

class CommercialDetail(db.Model):
    id = db.Column(UUID(), primary_key=True, nullable=False, default=uuid.uuid4)
    purchase_order_no = db.Column(db.String(255), nullable=False)
    purchase_order_date = db.Column(db.String(255), nullable=False)
    invoice_no = db.Column(db.String(255), nullable=False)
    invoice_date = db.Column(db.String(255), nullable=False)
    payment_terms = db.Column(db.String(255), nullable=False)
    amount_rem_to_oem = db.Column(db.String(255), nullable=False)
    date_of_rem_to_oem = db.Column(db.String(255), nullable=False)
    exchange_rate_rem = db.Column(db.String(255), nullable=False)
    custom_duty_payment = db.Column(db.String(255), nullable=False)
    exworks_price = db.Column(db.String(255), nullable=False)
    cif_charges = db.Column(db.String(255), nullable=False)
    total_cost = db.Column(db.String(255), nullable=False)
    boe_no = db.Column(db.String(255), nullable=False)
    custom_duty_value = db.Column(db.String(255), nullable=False)
    gst_amount = db.Column(db.String(255), nullable=False)
    exrate_boe = db.Column(db.String(255), nullable=False)
    clearing_charges = db.Column(db.String(255), nullable=False)
    cha_charges = db.Column(db.String(255), nullable=False)
    transportation_charges = db.Column(db.String(255), nullable=False)
    port_of_dispatch = db.Column(db.String(255), nullable=False)
    port_of_clearance = db.Column(db.String(255), nullable=False)
    period_of_insurance = db.Column(db.String(255), nullable=False)
    insurance_renewal = db.Column(db.String(255), nullable=False)
    total_landed_cost = db.Column(db.String(255), nullable=False)
    total_landed_cost_with_gst = db.Column(db.String(255), nullable=False)
    asset_id = db.Column(UUID(as_uuid=True), db.ForeignKey("asset.id"), nullable=False)