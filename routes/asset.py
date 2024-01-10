from flask import Blueprint, request, jsonify
from functions.asset_module import *
from functions.photo_module import add_photo , remove_photo
from functions.attachment_module import add_attachment , remove_attachment , update_attachment
from functions.asset_details import create_details, update_details
from helper import token_required
from functions.utilities.mailSender import send_email
from flask_mail import Mail
from analytical_db.DB import find_by_device_id
# mailer = Mail()


asset_bp = Blueprint("asset", __name__,static_url_path = "/asset")

def index_of(val, in_list):
    try:
        return in_list.index(val)
    except ValueError:
        return -1 
    
@asset_bp.before_request
@token_required
def hook(current_user, user_perms):
        try:
                if request.url.split("/")[4] == "upload_photo" or request.url.split("/")[4] == "upload_attachment" :
                    print("do you want to upload")
                elif  (
                       index_of("ASSETS.ALL",user_perms) == -1 
                       and index_of("ADMIN.ALL",user_perms) == -1 
                       and index_of("ASSETS.VIEW",user_perms) == -1 
                       and index_of("ASSETS.CRU",user_perms) == -1
                       ) :
                        return jsonify(msg="you are not authorize for this section"), 406
                elif  index_of("ASSETS.VIEW",user_perms) != -1 and request.method != "GET":
                        return jsonify(msg="you are not authorize for this section"), 406
                elif  index_of("ASSETS.CRU",user_perms) != -1 and request.method == "DELETE":
                        return jsonify(msg="you are not authorize for this section"), 406
                else:
                    request.environ['company_security_id'] = current_user.company_id
                    if index_of("ADMIN.ALL",user_perms) != -1 :
                         request.environ['company_security_permission'] = "ADMIN.ALL"

        except Exception :
                return jsonify(msg="you are not authorize for this section in catch"), 406



@asset_bp.route("/", methods=["GET"])
def get():
        res = send_email(username="admin", email="rocklikereeju5@gmail.com", password="asdf123345688#")
        return str(res)

@asset_bp.route("/create",methods=["POST"])
def create():
    try:
        data =request.json
        company_id = request.environ.get('company_security_id')
        print(company_id)
        asset_object = create_asset(data, company_id)
        return jsonify(asset_id=asset_object.id) , 200
    except Exception as e:
        return jsonify(error=str(e)), 400
    

@asset_bp.route("/create_config",methods=["POST"])
def create_config():
    try:
        data = request.json 
        asset_object = create_asset_config(data) 
        return jsonify(asset_config_id=asset_object.id) , 200
    except Exception as e:
        return jsonify(error=str(e)), 400
    

@asset_bp.route("/upload_photo",methods=["POST"])
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
        else:
            print(photos)
            return jsonify(error="str(e)"), 400
    except Exception as e:
        print(e)
        return jsonify(error=str(e)), 400
    
    
@asset_bp.route("/delete_photo",methods=["DELETE"])
def delete_photo():
        try:
            data = request.json
            id = data.get("id")
            delete_photo = remove_photo(id)
            return jsonify(mgs=f"photo successfully deleted id : {delete_photo.id}"), 200
        except Exception as e:
            return jsonify(error=str(e)), 400



@asset_bp.route("/upload_attachment",methods=["POST"])
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



@asset_bp.route("/delete_attachment",methods=["DELETE"])
def delete_attachment():
        try:
            data = request.json
            id = data.get("id")
            delete_attachment = remove_attachment(id)
            return jsonify(mgs=f"attachment successfully deleted id:{delete_attachment.id}"), 200
        except Exception as e:
            return jsonify(error=str(e)), 400


@asset_bp.route("/update_attachment",methods=["PUT"])
def update_attachments():
     try:
        data = request.json
        attachment = update_attachment(data)
        return jsonify( attachment), 200
     except Exception as e:
          return jsonify(error=str(e)), 400


@asset_bp.route("/get_all",methods=["GET"])
def get_all():
    try:
        company_id = request.environ.get('company_security_id')
        asset_no = request.headers.get('assetnumber')
        category = request.headers.get('category')
        limit = request.headers.get('limit')
        offset = request.headers.get('offset')
        yom = request.headers.get('yom')
        not_in_maintenance = True  if request.headers.get('not-in-maintenance') == 'true' else False
        inactive_asset=request.headers.get("inactive-asset")
        # rental_end_date=request.headers.get("rental-end-date")
        rental_start_date=request.headers.get("rental-start-date")
        unassigned_asset = request.headers.get('unassigned-asset')
        if unassigned_asset == "false":
             unassigned_asset = False
        elif unassigned_asset == "true":
             unassigned_asset = True
        list_data= get_asset_list(
                                company_id, asset_no,
                                category, limit, offset, 
                                yom, unassigned_asset, not_in_maintenance,
                                inactive_asset, # rental_end_date, 
                                rental_start_date
                                )
        return jsonify(list_data), 200
    except Exception as e:
        return jsonify(error=str(e)), 400
    

    
@asset_bp.route("/update",methods=["PUT"])
def lets_update():
    try:
        data = request.json 
        id = data.get("id")
        table_data = update_by_id(id, data)
        return jsonify( table_data) , 200
    except Exception as e:
            return jsonify(error=str(e)), 400


@asset_bp.route("/update_config", methods=["PUT"])
def lets_update_config():
     try:
        data = request.json 
        id = data.get("asset_id")
        table_data = update_asset_config(id, data)
        return jsonify( table_data), 200
     except Exception as e:
               return jsonify(error=str(e)), 400

@asset_bp.route("/get_data_by_id",methods=["GET"])
def get_data_by_id():
     try:
          data = request.headers
          id = data.get("id")
          company_id = request.environ.get('company_security_id')
          permission = request.environ.get('company_security_permission') or None
          all_asset_data = get_asset_by_id(id, company_id, permission)
          return jsonify(all_asset_data) , 200
     except Exception as e:
        return jsonify(error=str(e)), 400


@asset_bp.route("/delete",methods=["DELETE"])
def lets_delete():
     try:
        data = request.json
        id = data.get("id")
        table_data = delete_by_id(id)
        return jsonify(msg=f"asset is deleted id : {table_data.id}") , 200
     except Exception as e:
        return jsonify(error=str(e)), 400
     

@asset_bp.route("/create_details", methods=["POST"])
def lets_create_details():
            try: 
                 data = request.json
                 asset_object = create_details(data)
                 return jsonify(asset_details_id=asset_object.id), 200
            except Exception as e:
                return jsonify(error=str(e)), 400
            


@asset_bp.route("/update_details",methods=["PUT"])
def lets_update_details():
            try: 
                 data = request.json
                 asset_object = update_details(data)
                 return jsonify(asset_object), 200
            except Exception as e:
                return jsonify(error=str(e)), 400
            


@asset_bp.route("/search",methods=["GET"])
def get_asset_search_object():
            try: 
                company_id = request.environ.get('company_security_id')
                data = get_asset_data_list(company_id)
                return data,200
            except Exception as e:
                return jsonify(error=str(e)), 400


@asset_bp.route("/get_excel_json", methods=["GET"])
def get_excel_json():
        try:
            company_id = request.environ.get('company_security_id')
            permission = request.environ.get('company_security_permission') or None
            data =  get_all_asset_json_data(company_id, permission)
            return data,200
        except Exception as e:
            return jsonify(error=str(e)), 400
        

@asset_bp.route("/get_device/<device_id>", methods=["GET"])
def get_device_by_id(device_id):
    try:
        # print(device_id)
        data = find_by_device_id(device_id)
        return jsonify(data), 200
    except Exception as e:
         return jsonify(error=str(e)), 400
    