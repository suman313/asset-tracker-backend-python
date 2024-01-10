from config import db 
from sqlalchemy.dialects.postgresql import UUID
import uuid 

class EmployeePermissionMap(db.Model):
    __tablename__ = 'employee_permission_map'
    id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    employee_id = db.Column(UUID(as_uuid=True), db.ForeignKey('employee.id'), nullable=False)
    permission_id = db.Column(UUID(as_uuid=True), db.ForeignKey('permission.id'), nullable=False)