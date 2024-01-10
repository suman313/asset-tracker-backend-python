from flask import Blueprint, request, jsonify
from functions.company_module import *
from helper import token_required, access_required_role
from models.permission import Permission
from models.employee import Employee
from models.employee_permission_map import EmployeePermissionMap

company_bp = Blueprint("company", __name__)

@company_bp.route("/company/login", methods=["POST"])
def company_login():
    try:
        request_body = request.json

        user, token = check_company_credentials(request_body)

        if user and token:
            return jsonify({
                "token": token,
                "message": "Log in successful",
                "response_code": 200
            }),200
        elif user and token is None:
            print(user,token)
            return jsonify({
                "message": "token missing worng credentials",
                "response_code": 401
            }),401
        else:
            return jsonify({
                "message": "Unathorized acces: user not found",
                "response_code": 401
            }),401
    except Exception as e:
         return jsonify(error=str(e)) , 400

@company_bp.route("/change-password", methods=["POST"])
def change_password():
    request_body = request.json

    user, flag = change_password_entry(request_body)
    
    if user and flag:
        return jsonify({
            "message": "Password changed successfully",
            "response_code": 200
        }), 200
    elif user and flag==False:
        return jsonify({
            "message": "Same password as previous",
            "response_code": 401
        }), 401 
    else:
        return jsonify({
            "message": "Unathorized acces: user not found",
            "response_code": 401
        }), 401

@company_bp.route("/company/add-employee", methods=["POST"])
@token_required
def add_employee(current_user, user_perms):
    request_body = request.json
    company = Company.query.filter_by(id=current_user.company_id).first()
    # permission = Permission.query.filter_by(id=current_user.permission.id).first()
    # print(user_perms)
    if user_perms[0] == "ADMIN.ALL":

        employee, flag = register_employee(request_body, company)

        if flag == False:
            return jsonify({
                "message": f"User with email id {employee.email} already exists",
                "response_code": 401
            }), 401
        else:
            return jsonify({
                "message": f"Employee with email id {employee.email} has been registered successfully",
                "response_code": 200
            }), 200
    else:
        return jsonify({
            "message": f"User does not have the permission to perform this action",
            "response_code": 401
        }), 401


@company_bp.route("/company/add-permissions", methods=["POST"])
@token_required
def add_permissions(current_user, user_perms):
    request_body = request.json

    
    if user_perms[0] == "ADMIN.ALL":
        added_perms, flag = add_permissions_to_employee(request_body)

        if len(added_perms) == 0 and flag==False:
            return jsonify({
                "message": f"Employee with given details does not exist",
                "response_code": 401
            })
        elif len(added_perms) == 0 and flag==True:
            return jsonify({
                "message": f"Permissions already exist",
                "response_code": 401
            })
        else:
            return jsonify({
                "permissions": added_perms,
                "message": f"permissions added successfully",
                "response_code": 200
            })



    pass

@company_bp.route("/company/view-permissions", methods=["GET"])
@token_required
def view_permissions(current_user, user_perms):
    try: 
        return jsonify({
        "permissions": user_perms,
        }), 200
    except Exception as e:
         return jsonify({
               "message": f"{e}",
                "response_code": 401
         }), 401


@company_bp.route("/company/view-permissions-for-update", methods=["GET"])
@token_required
def view_permissions_for_update(current_user, user_perms):
    request_body = request.headers
    try: 
        email = request_body.get('email')
        dataArray = []
        existing_user = Employee.query.filter_by(email=email).first()
        if existing_user is not None:
                ids_array = EmployeePermissionMap.query.filter_by(employee_id=existing_user.id).all()
                for array in ids_array:
                        data_of_permissions = Permission.query.filter_by(id=array.permission_id).first()
                        dataArray.append({"perms" : data_of_permissions.title, "id": data_of_permissions.id})
                return jsonify({
                    "message": dataArray,
                    "response_code": 200
                }), 200

        else: 
             print(request_body.get('data'))
             return jsonify({
               "message": f"{None}",
                "response_code": 401
            }), 400
    except Exception as e:
         print(e)
         return jsonify({
               "message": f"{e}",
                "response_code": 401
         }), 400


@company_bp.route("/company/edit-permissions", methods=["PUT"])
@token_required
def edit_permissions(current_user, user_perms):
    try: 
            request_body = request.json

    
            if user_perms[0] == "ADMIN.ALL":
                added_perms, flag = edit_permissions_to_employee(request_body)
                return jsonify({"perm" :added_perms,"flag": flag})
    except Exception as e:
                return   jsonify({
                        "message": f"something went wrong{e}",
                        "response_code": 401
                    }) , 400
         
        





@company_bp.route("/remove-employee", methods=["POST"])
def remove_employee():
    pass

@company_bp.route("/company/all_employee", methods=["GET"])
@token_required
def list_employees(current_user, user_perms):
        try:
                    data = get_all_employ_under_company(company_id=current_user.company_id)
                    return data
        except Exception as e:
                return jsonify({
                "message": f"Employee with given details does not exist",
                "response_code": 401
            }), 401

            