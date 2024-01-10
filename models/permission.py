from config import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid 

class Permission(db.Model):
    __tablename__ = 'permission'
    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    employee_permission_map = db.relationship("EmployeePermissionMap", backref="permission")