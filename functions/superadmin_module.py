from models.super_admin import SuperAdmin
from models.requested_companies import RequestedCompanies
from models.company import Company
from uuid import uuid4
from config import db, SECRET_KEY
from flask import session
import jwt, datetime
from functions.utilities.mailSender import send_email

def create_superadmin_user(request_body):
    existing_user = SuperAdmin.query.filter_by(email=request_body["email"]).first()

    try:
        if existing_user is None:
            new_superadmin = SuperAdmin(
                email=request_body["email"]
            )

            new_superadmin.set_password(request_body["password"])
            
            token = uuid4()
            new_superadmin.set_registration_token(token)

            db.session.add(new_superadmin)
            db.session.commit()

            return new_superadmin, True
        else:
            return existing_user, False
    except Exception as e:
        raise e
    
def check_credentials(data):
    existing_user = SuperAdmin.query.filter_by(email=data["email"]).first()
    token = None
    if existing_user is not None and existing_user.check_password(password=data["password"]):
        session['email'] = data["email"]
        token = jwt.encode({
            'public_id': existing_user.registration_token,
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=45)
        }, SECRET_KEY, "HS256")

        return existing_user, token
    else:
        existing_user, token

def create_onboarding_request(reqeust_body):
    existing_request = RequestedCompanies.query.filter_by(email=reqeust_body['email']).first()

    try:
        if existing_request is None:
            new_request = RequestedCompanies(
                name=reqeust_body['name'],
                email=reqeust_body['email'],
                address=reqeust_body['address'],
                company_name=reqeust_body['company_name'],
                phone_no=reqeust_body['phone_no'],
                approved=False
            )

            db.session.add(new_request)
            db.session.commit()
            send_email(topic_type="signup", email=reqeust_body['email'])
            return new_request, True
        else:
            return existing_request, False
    except Exception as e:
        raise e
    
def get_all_requested_companies():
    reqeust_companies = RequestedCompanies.query.filter_by(approved=False).all()

    companies_list = []

    for comp in reqeust_companies:
        companies_list.append({
            "name": comp.name,
            "email": comp.email,
            "address": comp.address,
            "company_name": comp.company_name,
            "phone_no": comp.phone_no
        })

    return companies_list

    
def get_all_approved_companies():
    approved_companies = Company.query.all()

    companies_list = []

    for comp in approved_companies:
        companies_list.append({
            "name": comp.name,
            "email": comp.email,
            "address": comp.address,
            "company_name": comp.company_name,
            "phone_no": comp.phone_no
        })

    return companies_list  
