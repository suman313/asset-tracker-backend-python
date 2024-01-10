from flask import Blueprint, request, jsonify
from functions.operator_module import (
        create_operator, update_operator, delete_operator, 
        get_operator_by_id, get_operator_list, get_all_data_operator_company_id,
        search_operator_list
    )
from helper import token_required
from functions.photo_module import add_photo, remove_photo



operator_bp = Blueprint('operator', __name__)

def index_of(val, in_list):
    try:
        return in_list.index(val)
    except ValueError:
        return -1 

@operator_bp.before_request
@token_required
def hook(current_user, user_perms):
    if request.url.split("/")[4] == "upload_photo" or request.url.split("/")[4] == "upload_attachment" :
        print("do you want to upload")
    elif (index_of("OPERATOR.ALL", user_perms) == -1 and index_of("ADMIN.ALL", user_perms) == -1 
          and index_of("OPERATOR.VIEW",user_perms) == -1 and index_of("OPERATOR.CRU",user_perms) == -1 ):
                    return jsonify(msg="you are not authorize for this section"), 406
    elif  index_of("OPERATOR.VIEW",user_perms) != -1 and request.method != "GET":
                    return jsonify(msg="you are not authorize for this section"), 406
    elif  index_of("OPERATOR.CRU",user_perms) != -1 and request.method == "DELETE":
                    return jsonify(msg="you are not authorize for this section"), 406
    else:
        request.environ['company_security_id'] = current_user.company_id


@operator_bp.route('/create', methods=['POST'])
def lets_create():
    try:
        data = request.json
        company_id = request.environ.get('company_security_id')
        nw_operator = create_operator(data, company_id)
        return jsonify(nw_operator)
    except Exception as e:
        return jsonify(error=str(e)),400
    

@operator_bp.route("/get_all", methods=['GET'])
def lets_get_all():
            try:
                  company_id = request.environ.get('company_security_id')
                  limit = request.headers.get('limit')
                  offset = request.headers.get('offset')
                  aadhar_no = request.headers.get('aadhar_no')
                  name = request.headers.get('name')
                  pf_account = request.headers.get('pf_account')
                  all_operators = get_operator_list(company_id, limit, offset, aadhar_no, name, pf_account)
                  return jsonify(all_operators)
            except Exception as e:
                return jsonify(error=str(e)),400
            

@operator_bp.route("/get_by_id", methods=['GET'])
def lets_get_by_id():
        try:
                    data = request.headers
                    id = data.get('id')
                    operator = get_operator_by_id(id)
                    return jsonify(operator)
        except Exception as e:
                    return jsonify(error=str(e)),400
        
                 

@operator_bp.route("/update", methods=['POST', 'PUT'])
def lets_update_operator():
            try:
                    data = request.json
                    id = data.get('id')
                    operator = update_operator(id,data)
                    return jsonify(operator)
            
            except Exception as e:
                    return jsonify(error=str(e)),400
            

            

@operator_bp.route("/delete", methods=['DELETE'])
def lets_delete_operator():
            try:
                    deta = request.json
                    id = deta.get('id')
                    operator = delete_operator(id)
                    return jsonify(msg=f"successfully delete {operator.id}")
            except Exception as e:
                    return jsonify(error=str(e)),400
            
@operator_bp.route("/get-json-data", methods=["GET"])
def lets_get_json_data():
        try:
            company_id = request.environ.get("company_security_id")
            data =  get_all_data_operator_company_id(company_id=company_id)
            return data, 200
        except Exception as e:
              return jsonify(error=str(e)), 400
        

@operator_bp.route("/upload-file",methods=["POST"])
def upload_photo():
    try:
        photos = request.files.getlist("photo")
        if len(photos) >= 2:
            list_photo_ids = []
            for photo in photos:
                data = request.form.to_dict(flat=True)
                create_photo = add_photo(photo, data)
                list_photo_ids.append(create_photo.id)
            return jsonify(mgs=f"photo successfully added ids : {list_photo_ids}"), 200
        elif len(photos) == 1:
            photo = request.files["photo"]
            data = request.form.to_dict(flat=True)
            create_photo = add_photo(photo, data)
            return jsonify(mgs=f"photo successfully added id : {create_photo.id}"), 200
    except Exception as e:
        return jsonify(error=str(e)), 400
    
    
@operator_bp.route("/delete-file",methods=["DELETE"])
def delete_photo():
        try:
            data = request.json
            id = data.get("id")
            delete_photo = remove_photo(id)
            return jsonify(mgs=f"photo successfully deleted id : {delete_photo.id}"), 200
        except Exception as e:
            return jsonify(error=str(e)), 400
        
@operator_bp.route("/search", methods=["GET"])
def get_photo():
        try:
            company_id = request.environ.get('company_security_id')
            search_list = search_operator_list(company_id)
            return jsonify(search_list), 200
        except Exception as e:
               return jsonify(error=str(e)), 400