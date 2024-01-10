from config  import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid
from werkzeug.security import check_password_hash, generate_password_hash


class  Company(db.Model):
	__tablename__ =  'company'
	id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	name = db.Column(db.String(255), nullable=False)
	email = db.Column(db.String(200), nullable=False)
	password = db.Column(db.String(200), nullable=False)
	company_name = db.Column(db.String(200), nullable=False)
	address = db.Column(db.String(200), nullable=False)
	phone_no = db.Column(db.String(50), nullable=False)
	registration_token = db.Column(db.String(200), nullable=False)
	suspended = db.Column(db.Boolean, default=False)
	super_admin_id = db.Column(UUID(as_uuid=True), db.ForeignKey('super_admin.id'), nullable=False)
	employee = db.relationship('Employee', backref='company')
	lease = db.relationship('Lease', backref='company')
	maintenance = db.relationship('Maintenance', backref='company')
	operator = db.relationship('Operator', backref='company')
	asset = db.relationship("Asset", backref="company")
	invoice = db.relationship("Invoice", backref="company")
	lease_operator_mapping = db.relationship('Lease_Operator_Mapping', backref="company")
	time_sheet = db.relationship("TimeSheet", backref="company")


	def set_password(self, password):
		self.password = generate_password_hash(password, method='sha256')
		
	def set_registration_token(self, token):
		self.registration_token = token
		
	def check_password(self, password):
		return check_password_hash(self.password, password)