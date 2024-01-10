from flask import Blueprint, request, jsonify
from functions.superadmin_module import create_superadmin_user, check_credentials, create_onboarding_request, get_all_requested_companies, get_all_approved_companies
from helper import superadmin_token_required
from models.requested_companies import RequestedCompanies
from models.company import Company
from models.permission import Permission
from functions.company_module import register_company
from config import db
from functions.utilities.mailSender import send_email

superadmin_bp = Blueprint("superadmin", __name__)

@superadmin_bp.route("/superadmin/signup", methods=['POST'])
def signup():
    request_body = request.json

    user, message = create_superadmin_user(request_body)

    if message == True:
        return jsonify({
            "message": f"User with email id {user.email} added successfully",
            "response_code": 200
        })
    else:
        return jsonify({
            "message": f"User with email id {user.email} already exists",
            "response_code": 403
        })

@superadmin_bp.route("/superadmin/login", methods=['POST'])
def superadmin_login():
    request_body = request.json

    user, token = check_credentials(request_body)

    if user and token:
        return jsonify({
            "token": token,
            "message": "Log in successful",
            "response_code": 200
        })
    elif user and token is None:
        return jsonify({
            "message": "token missing",
            "response_code": 401
        })
    else:
        return jsonify({
            "message": "Unathorized acces: user not found",
            "response_code": 401
        })

@superadmin_bp.route("/onboard-company", methods=['POST'])
def request_company():
    request_body = request.json

    requested_company, flag = create_onboarding_request(request_body)

    if flag:
        return jsonify({
            "message": "Onboarding Request Granted",
            "response_code": 200
        })
    else:
        return jsonify({
            "message": "Request already exists",
            "response_code": 403
        })


@superadmin_bp.route("/superadmin/get-requested-companies", methods=['GET'])
@superadmin_token_required
def get_requested_companies(current_user):
    requested_companies = get_all_requested_companies()

    return jsonify({
        "response": requested_companies,
        "message": "Success",
        "response_code": 200
    })

@superadmin_bp.route("/superadmin/get-approve-companies", methods=['GET'])
@superadmin_token_required
def get_approve_companies(current_user):
    companies = get_all_approved_companies()

    return jsonify({
        "response": companies,
        "message": "Success",
        "response_code": 200
    }),200

@superadmin_bp.route("/superadmin/approve-company", methods=['POST'])
@superadmin_token_required
def approve_company(current_user):
    request_body = request.json

    try:
        target_request = RequestedCompanies.query.filter_by(email=request_body['email']).first()
        target_request.approved = True
        db.session.commit()
        # send_email(topic_type="signup", email=request_body['email'])
        #registers requested company to company table
        registered_company = register_company(target_request, current_user)
        return jsonify({
            "message": f"Company with email id {registered_company.email} approved",
            "response_code": 200
        })
    except Exception as e:
        raise e

@superadmin_bp.route("/superadmin/suspend-company", methods=['POST'])
@superadmin_token_required
def suspend_company(current_user):
    request_body = request.json

    company = Company.query.filter_by(email=request_body['email']).first()

    try:
        company.suspended = False
        db.session.commit()

        return jsonify({
            "message": f"Company with email id {company.email} is suspended",
            "response_code": 200
        })
    
    except Exception as e:
        raise e
    
@superadmin_bp.route("/initialize-permissions", methods=["POST"])
# @superadmin_token_required
def initialize_permissions():
    request_body = request.json

    perms_count = Permission.query.count()

    for perm in request_body["perms"]:
        existing_perms = Permission.query.filter_by(title=perm["title"]).first()
        if existing_perms is None:
            new_perms = Permission(
                title=perm['title'],
                description=perm['description']
            )
            db.session.add(new_perms)
            db.session.commit()
        else:
            continue
    
    return jsonify({
        "message": "Permissions initialized successfully",
        "response_code": 200
    })




