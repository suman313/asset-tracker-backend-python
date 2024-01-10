from models.company import Company
from models.employee import Employee
from models.permission import Permission
from models.employee_permission_map import EmployeePermissionMap
from functions.utilities.mailSender import send_email
from config import db, SECRET_KEY
from uuid import uuid4
from flask import session
import jwt, datetime, secrets

def register_company(company_obj, superadmin):
    try:
        new_company = Company(
            name=company_obj.name,
            email=company_obj.email,
            company_name=company_obj.company_name,
            address=company_obj.address,
            phone_no=company_obj.phone_no,
            super_admin_id=superadmin.id
        )

        auto_pass = secrets.token_urlsafe(32)
        new_company.set_password(auto_pass)

        token = uuid4()
        new_company.set_registration_token(token)
        db.session.add(new_company)
        db.session.commit()

        permission = Permission.query.filter_by(title="ADMIN.ALL").first()
        
        
        new_company_admin = Employee(
            email=company_obj.email,
            name=company_obj.name,
            company_id=new_company.id
        )

        new_company_admin.set_password(auto_pass)
        new_company_admin.set_registration_token(token)

        print("Email: ", company_obj.email)
        print("Password: ", auto_pass)
        db.session.add(new_company_admin)
        db.session.commit()

        new_employee_permission_map = EmployeePermissionMap(
            employee_id=new_company_admin.id,
            permission_id=permission.id
        )

        db.session.add(new_employee_permission_map)
        db.session.commit()
        send_email(topic_type="approve_company", email=company_obj.email, username=company_obj.email, password=auto_pass)
        return new_company
    except Exception as e:
        raise e

def check_company_credentials(request_body):
    try : 
        existing_user = Employee.query.filter_by(email=request_body['email']).first()
        if existing_user:
            company = Company.query.filter_by(id=existing_user.company_id).first()
            token = None
            data = existing_user.check_password(password=request_body['password'])
            print(existing_user, data)
            if existing_user and existing_user.check_password(password=request_body['password']):
                session['company'] = company.name
                token = jwt.encode({
                    'verified': existing_user.verified,
                    'public_id': existing_user.registration_token,
                    'exp': datetime.datetime.now() + datetime.timedelta(days=7)
                }, SECRET_KEY, "HS256")
                
                return existing_user, token
            else:
                return existing_user, token
        else:
             raise Exception("Unathorized acces: user not found")
    except Exception as e:
        raise e
    
def change_password_entry(request_body):
    existing_user = Employee.query.filter_by(email=request_body['email']).first()

    if existing_user is None:
        return existing_user, False
    elif existing_user.email == request_body['email'] and existing_user.password == request_body['password']:
        return existing_user, False
    elif existing_user.email == request_body['email']:
        existing_user.set_password(request_body['password'])
        existing_user.verified = True
        db.session.commit()
        send_email(topic_type="change_password", email=request_body['email'])
        return existing_user, True
    
def register_employee(request_body, company):
    existing_user = Employee.query.filter_by(email=request_body['email']).first()
    
    try:
        if existing_user is not None:
            return existing_user, False
        else:
            new_employee = Employee(
                email=request_body['email'],
                name=request_body['name'],
                company_id=company.id
            )

            auto_pass = secrets.token_urlsafe(32)
            new_employee.set_password(auto_pass)

            print(auto_pass)
            token = uuid4()
            new_employee.set_registration_token(token)

            db.session.add(new_employee)
            db.session.commit()
            send_email(topic_type="add_employee", email=request_body['email'], username=request_body['email'],password=auto_pass)
            return new_employee, True
    except Exception as e:
        raise e
    
def add_permissions_to_employee(request_body):
    existing_user = Employee.query.filter_by(email=request_body['email']).first()
    
    existing_perms = []
    added_perms = []

    if existing_user is None:
        return added_perms, False
    else:
        existing_emp_perm_map = EmployeePermissionMap.query.filter_by(employee_id=existing_user.id).all()

        
        for existing_map in existing_emp_perm_map:
            perm = Permission.query.filter_by(id=existing_map.permission_id).first()
            existing_perms.append(perm.title)

        for perms in request_body["permissions"]:
            if perms in existing_perms:
                continue
            else:
                permission = Permission.query.filter_by(title=perms).first()
                new_permission = EmployeePermissionMap(
                    employee_id=existing_user.id,
                    permission_id=permission.id
                )
                added_perms.append(perms)
                db.session.add(new_permission)
        db.session.commit()

        return added_perms, True
    

def get_all_employ_under_company(company_id):
        employees = Employee.query.filter_by(company_id=company_id).all()
        list_employees = []
        for employee in employees:
                list_employees.append({
                        "id":employee.id,
                        "name":employee.name,
                        "email":employee.email,
                        "verified":employee.verified,
                        "company_id": employee.company_id
                })
        return list_employees


def edit_permissions_to_employee(request_body):
    try: 
            existing_user = Employee.query.filter_by(email=request_body['email']).first()
            print(existing_user)
            existing_perms = []
            added_perms = []
            
            if existing_user != None:
                    print(existing_user)
                    
                    existing_emp_perm_map = EmployeePermissionMap.query.filter_by(employee_id=existing_user.id).all()
                    print(existing_emp_perm_map[0].permission_id)
                    for existing_map in existing_emp_perm_map:
                            perm = Permission.query.filter_by(id=existing_map.permission_id).first()
                            existing_perms.append(perm.title)
                    print(existing_perms)
                    for data in request_body["permissions"]:
                        perms_for_update = request_body.get("perms_for_update") 
                        perms = data.get("perms")
                        perms_id = data.get("id")
                        permission_now = Permission.query.filter_by(title=perms_for_update).first()
                        
                        if perms_for_update is None or permission_now is None:
                            continue
                        elif perms_for_update:
                            edit_permission = EmployeePermissionMap.query.filter_by(employee_id=existing_user.id).filter_by(permission_id=perms_id).first()
                            print(perms_for_update,existing_user.id, perms_id)
                            edit_permission.permission_id = permission_now.id
                            added_perms.append(perms)
                            db.session.add(edit_permission)
                    db.session.commit()

                    return added_perms, True
            
    except Exception as e:
         raise e
