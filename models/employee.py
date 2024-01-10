from config import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid
from werkzeug.security import check_password_hash, generate_password_hash


class Employee(db.Model):
    __tablenme__ = 'employee'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4 )
    name=db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registration_token = db.Column(db.String(200), nullable=False)
    verified = db.Column(db.Boolean(), default=False, nullable=False)
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey('company.id'))
    employee_permission_map = db.relationship("EmployeePermissionMap", backref="employee")

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')
        
    def set_registration_token(self, token):
        self.registration_token = token
        
    def check_password(self, password):
        return check_password_hash(self.password, password)