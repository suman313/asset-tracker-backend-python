from flask import request, jsonify, Blueprint
from helper import token_required
from functions.dashboard_module import *
# import datetime 

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

def index_of(val, in_list):
    try:
        return in_list.index(val)
    except ValueError:
        return -1 
    
@dashboard_bp.before_request
@token_required
def hook(current_user, user_perms):
    if request.url.split("/")[4] == "upload_photo" or request.url.split("/")[4] == "upload_attachment" :
        print("do you want to upload")
    elif index_of("MAINT.ALL",user_perms) == -1 and index_of("ADMIN.ALL",user_perms) == -1 and index_of("MAINT.VIEW",user_perms) == -1 and index_of("MAINT.CRU",user_perms) == -1 :
                    return jsonify(msg="you are not authorize for this section"), 406
    elif  index_of("MAINT.VIEW",user_perms) != -1 and request.method != "GET":
                    return jsonify(msg="you are not authorize for this section"), 406
    elif  index_of("MAINT.CRU",user_perms) != -1 and request.method == "DELETE":
                    return jsonify(msg="you are not authorize for this section"), 406
    else:
        request.environ['company_security_id'] = current_user.company_id

@dashboard_bp.route('/get_all_details', methods=['GET'])
def all_details():
        try:
                company_id = request.environ['company_security_id']
                msg = get_all_overview(company_id)
                return jsonify(msg), 200
        except Exception as e:
                return jsonify(error=str(e)), 400
        
# @dashboard_bp.route('/get_details')
# def call_dum_function():
#         try:
#             company_id = request.environ['company_security_id']
#             date_start_from = str(datetime.datetime.now()).split(" ")[0]
#             date_end_from = '2023-11-18'
#             data =  get_free_assets_list(company_id)
#             return  jsonify(data=data), 200
#         except Exception as e:
#             return jsonify(error=str(e)), 400
        
@dashboard_bp.route("/get-data-by-model-category", methods=["GET"])
def get_data_by_filter_by_category_or_category():
    try:
        company_id = request.environ['company_security_id']
        category = request.headers.get("category", None)
        model = request.headers.get("model", None)
        data = get_all_data_by_all_category(company_id)
        return jsonify(data), 200
    except Exception as e:
           return jsonify(error=str(e)), 400