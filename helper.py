from flask import session, jsonify, request
import jwt
from config import SECRET_KEY
from models.employee import Employee
from models.super_admin import SuperAdmin
from models.employee_permission_map import EmployeePermissionMap
from models.permission import Permission
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
            # print(token)

        if not token:
            return jsonify(message="valid token is missing")

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = Employee.query.filter_by(registration_token=data['public_id']).first()
            permission_maps = EmployeePermissionMap.query.filter_by(employee_id=current_user.id).all()
            user_perms = []
            for permission_map in permission_maps:
                perm = Permission.query.filter_by(id=permission_map.permission_id).first()
                if perm is not None:
                    user_perms.append(perm.title)
                else:
                    continue

            # user_perms = Permission.query.filter_by(id=permission_map.permission_id).first()
            
        except:
            return jsonify(message="token is invalid"), 400
        return f(current_user, user_perms, *args, **kwargs)
    return decorator

def superadmin_token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
            # print(token)

        if not token:
            return jsonify(message="valid token is missing")

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = SuperAdmin.query.filter_by(registration_token=data['public_id']).first()
            print(current_user)
        except:
            return jsonify(message="token is invalid")
        return f(current_user, *args, **kwargs)
    return decorator

def access_required_role(role=[]):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if session.get("role") == None or role == []:
                session["header"] = "Welcome Guest!!"
            if session.get("role") == "company" and "company" in role:
                session["header"] = "Welcome Company User"
            if session.get("role") == "superadmin" and "superadmin" in role:
                session["header"] = "Welcome Super Admin"
            else:
                session["header"] = "Sorry No Access"
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

