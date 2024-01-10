from flask import request, jsonify, Blueprint
from functions.maintenance_module import (
        create_maintenance, get_maintenance_list, 
        get_maintenance_by_id, update_maintenance, 
        update_parts, delete_maintenance, get_data_list_for_search, get_all_json_data_in_maintenance_by_company
    )
from functions.utilities.odoo_funtions.main import main_odoo_function
from functions.photo_module import add_photo, remove_photo
from functions.attachment_module import add_attachment, remove_attachment, update_attachment
from helper import token_required



maintenance_bp = Blueprint('maintenance', __name__)

def index_of(val, in_list):
    try:
        return in_list.index(val)
    except ValueError:
        return -1 

@maintenance_bp.before_request
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


@maintenance_bp.route('/create', methods=['POST'])
def let_create():
    try:
        data = request.json
        company_id = request.environ['company_security_id']
        nw_maintenance = create_maintenance(data, company_id)
        return jsonify(id=nw_maintenance.id), 200
    except Exception as e:
            return jsonify(error=str(e)), 400


@maintenance_bp.route('/get_all', methods=['GET'])
def let_get_all():
     try:
        company_id = request.environ.get('company_security_id')
        data = request.headers
        asset_id = data.get("asset-id")
        lease_id = data.get("lease-id")
        limit = data.get("limit")
        offset = data.get("offset")
        scheduled_date_from = data.get("scheduled-date-from")
        scheduled_date_to = data.get("scheduled-date-to")
        maintenance_list = get_maintenance_list(asset_id, lease_id, company_id, limit, offset, scheduled_date_from, scheduled_date_to)
        return jsonify(maintenance_list), 200
     except Exception as e:
       return jsonify(error=str(e)), 400
     

@maintenance_bp.route('/get_by_id', methods=['GET'])
def let_get_by_id():
    try:
        data = request.headers
        id = data.get("id")
        maintenance = get_maintenance_by_id(id)
        return jsonify(maintenance), 200
    except Exception as e:
        return jsonify(error=str(e)), 400


@maintenance_bp.route('/update', methods=['POST', "PUT"])
def let_update():
    try:
        data = request.json
        id = data.get("id")
        parts = data.get("parts") or []
        maintenance_parts = []
        maintenance = update_maintenance(id,data)
        for part in parts:
                maintenance_part = update_parts(id,part)
                maintenance_parts.append(maintenance_part)
        maintenance["parts"] = maintenance_parts
        return jsonify(maintenance), 200
    except Exception as e:
        return jsonify(error=str(e)), 400
    
    


@maintenance_bp.route('/delete', methods=['DELETE'])
def let_delete():
    try:
        data = request.json
        id = data.get("id")
        maintenance = delete_maintenance(id)
        return jsonify(maintenance), 200
    except Exception as e:
        return jsonify(error=str(e)), 400
    


# s3 module start

@maintenance_bp.route("/upload_photo",methods=["POST"])
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
    
    
@maintenance_bp.route("/delete_photo",methods=["DELETE"])
def delete_photo():
        try:
            data = request.json
            id = data.get("id")
            delete_photo = remove_photo(id)
            return jsonify(mgs=f"photo successfully deleted id : {delete_photo.id}"), 200
        except Exception as e:
            return jsonify(error=str(e)), 400



@maintenance_bp.route("/upload_attachment",methods=["POST"])
def upload_attachment():
        try:
                attachments = request.files.getlist("attachment")
                if len(attachments) >= 2:
                    list_attachment_ids = []
                    for attachment in attachments:
                        data = request.form.to_dict(flat=True)
                        create_attachment = add_attachment(attachment, data)
                        list_attachment_ids.append(create_attachment.id)
                    return jsonify(mgs=f"attachment successfully added ids : {list_attachment_ids}"), 200
                elif len(attachments) == 1:
                    attachment = request.files["attachment"]
                    data = request.form.to_dict(flat=True)
                    create_attachment = add_attachment(attachment, data)
                    return jsonify(mgs=f"attachment successfully added id : {create_attachment.id}"), 200
        except Exception as e:
            return jsonify(error=str(e)), 400



@maintenance_bp.route("/delete_attachment",methods=["DELETE"])
def delete_attachment():
        try:
            data = request.json
            id = data.get("id")
            delete_attachments = remove_attachment(id)
            return jsonify(mgs=f"attachment successfully deleted id:{delete_attachments.id}"), 200
        except Exception as e:
            return jsonify(error=str(e)), 400


@maintenance_bp.route("/update_attachment",methods=["PUT"])
def update_attachments():
     try:
        data = request.json
        attachment = update_attachment(data)
        return jsonify( attachment), 200
     except Exception as e:
          return jsonify(error=str(e)), 400
     

# s3 module ends ==>


@maintenance_bp.route("/search",methods=["GET"])
def search():
        try:
                    company_id = request.environ.get('company_security_id') 
                    data = get_data_list_for_search(company_id)
                    return data, 200
        except Exception as e:
                    return jsonify(error=str(e)), 400


@maintenance_bp.route("/get-json-data", methods=["GET"])
def lets_get_json_data():
        try:
            company_id = request.environ.get("company_security_id")
            data =  get_all_json_data_in_maintenance_by_company(company_id=company_id)
            return data, 200
        except Exception as e:
              return jsonify(error=str(e)), 400
        
@maintenance_bp.route("/get-parts-name", methods=["GET"])
def lets_get_parts_name():
        try:
            data =  main_odoo_function(func_type="get_part_list")
            return data, 200
        except Exception as e:
              return jsonify(error=str(e)), 400