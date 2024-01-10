from config  import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid
from werkzeug.security import check_password_hash, generate_password_hash


class  SuperAdmin (db.Model):
	__tablename__ =  'super_admin'
	id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	email= db.Column(db.String(200), nullable=False)
	password= db.Column(db.String(200), nullable=False)
	registration_token = db.Column(db.String(200), nullable=False)
	company = db.relationship('Company', backref='super_admin')

	def set_password(self, password):
		self.password = generate_password_hash(password, method='sha256')
		
	def set_registration_token(self, token):
		self.registration_token = token
		
	def check_password(self, password):
		return check_password_hash(self.password, password)