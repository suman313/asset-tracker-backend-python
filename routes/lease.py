from flask import Blueprint, request, jsonify
from functions.lease_module import *
from functions.photo_module import add_photo, remove_photo
from functions.attachment_module import add_attachment, remove_attachment, update_attachment
from helper import token_required
from functions.invoice_module import create_invoice, update_invoice, get_invoice, delete_invoice
from functions.utilities.odoo_funtions.main import main_odoo_function
import pandas
from init_func import updated_odoo_init

lease_bp = Blueprint('lease', __name__, url_prefix='/lease')

def index_of(val, in_list):
    try:
        return in_list.index(val)
    except ValueError:
        return -1 

@lease_bp.before_request
@token_required
def hook(current_user, user_perms):
    if request.url.split("/")[4] == "upload_photo" or request.url.split("/")[4] == "upload_attachment" :
        print("do you want to upload")
    elif index_of("LEASE.ALL",user_perms) == -1 and index_of("ADMIN.ALL", user_perms) == -1 and index_of("LEASE.VIEW",user_perms) == -1 and index_of("LEASE.CRU",user_perms) == -1 :
                    return jsonify(msg="you are not authorize for this section"), 406
    elif  index_of("LEASE.VIEW",user_perms) != -1 and request.method != "GET":
                    return jsonify(msg="you are not authorize for this section"), 406
    elif  index_of("LEASE.CRU",user_perms) != -1 and request.method == "DELETE":
                    return jsonify(msg="you are not authorize for this section"), 406
    else:
        request.environ['company_security_id'] = current_user.company_id


@lease_bp.route('/create', methods=['POST'])
def create():
        try:
            data = request.json
            company_id = request.environ.get('company_security_id')
            nw_lease=create_lease(data, company_id)
            return jsonify(lease_id=nw_lease.id),200
        except Exception as e:
            print(e)
            return jsonify(error=str(e)), 400
        

# s3 module starts ==> 

@lease_bp.route("/upload_photo",methods=["POST"])
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
    
    
@lease_bp.route("/delete_photo",methods=["DELETE"])
def delete_photo():
        try:
            data = request.json
            id = data.get("id")
            delete_photo = remove_photo(id)
            return jsonify(mgs=f"photo successfully deleted id : {delete_photo.id}"), 200
        except Exception as e:
            return jsonify(error=str(e)), 400



@lease_bp.route("/upload_attachment",methods=["POST"])
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



@lease_bp.route("/delete_attachment",methods=["DELETE"])
def delete_attachment():
        try:
            data = request.json
            id = data.get("id")
            delete_attachments = remove_attachment(id)
            return jsonify(mgs=f"attachment successfully deleted id:{delete_attachments.id}"), 200
        except Exception as e:
            return jsonify(error=str(e)), 400


@lease_bp.route("/update_attachment",methods=["PUT"])
def update_attachments():
     try:
        data = request.json
        attachment = update_attachment(data)
        return jsonify( attachment), 200
     except Exception as e:
          return jsonify(error=str(e)), 400
     

# s3 module ends ==>


@lease_bp.route("/get_all",methods=["GET"])
def get_all():
    try:
        company_id = request.environ.get('company_security_id')
        asset_id = request.headers.get("asset-id")
        limit = request.headers.get('limit')
        offset = request.headers.get('offset')
        start_date = request.headers.get('start_date')
        end_date = request.headers.get('end_date')
        lease_genarated_id = request.headers.get('lease-genarated-id')
        list_data= get_lease_list(asset_id, company_id, limit, offset, lease_genarated_id, start_date, end_date)
        return jsonify(list_data), 200
    except Exception as e:
        return jsonify(error=str(e)), 400
    

    
@lease_bp.route("/update",methods=["PUT"])
def lets_update():
    try:
        data = request.json
        id = data.get("id")
        table_data = update_lease_by_id(id, data)
        return jsonify( table_data) , 200
    except Exception as e:
            return jsonify(error=str(e)), 400



@lease_bp.route("/get_data_by_id",methods=["GET"])
def get_data_by_id():
     try:
          data = request.headers
          id = data.get("id")
          print(id)
          all_asset_data = get_lease_by_id(id)
          return jsonify( all_asset_data) , 200
     except Exception as e:
        return jsonify(error=str(e)), 400


@lease_bp.route("/delete",methods=["DELETE"])
def lets_delete():
     try:
        data = request.json
        id = data.get("id")
        print(id)
        table_data = delete_lease_by_id(id)
        return jsonify(msg=f"lease is deleted id : {table_data.id}") , 200
     except Exception as e:
        return jsonify(error=str(e)), 400
     
@lease_bp.route("/search",methods=["GET"])
def lets_search():
        try: 
                company_id = request.environ.get("company_security_id")
                data = get_lease_list_for_search(company_id)
                return data, 200
        except Exception as e:
                return jsonify(error=str(e)), 400

@lease_bp.route("/create-invoice", methods=["POST"])
def lets_create_invoice():
        try:
              company_id = request.environ.get("company_security_id")
              data = request.form
              document = request.files.getlist("document")
              resp = create_invoice(company_id, data, document=document[0])
              return resp, 201
        except Exception as e:
               print(e)
               return jsonify(error=str(e)), 400
        
@lease_bp.route("/get-invoice", methods=["GET"])
def lets_get_invoice():
        try:
              company_id = request.environ.get("company_security_id")
              lease_id = request.headers.get("lease-id")

              resp = get_invoice(company_id, lease_id)
              return resp, 200
        except Exception as e:
               print(e)
               return jsonify(error=str(e)), 400
        
@lease_bp.route("/update-invoice", methods=["PUT"])
def lets_update_invoice():
        try:
              company_id = request.environ.get("company_security_id")
              data = request.json
              resp = update_invoice(company_id, data)
              return resp, 200
        except Exception as e:
               print(e)
               return jsonify(error=str(e)), 400
        
@lease_bp.route("/delete-invoice", methods=["DELETE"])
def lets_delete_invoice():
        try:
              company_id = request.environ.get("company_security_id")
              invoice = request.headers.get("invoice-id")
              resp = delete_invoice(company_id, invoice)
              return resp, 200
        except Exception as e:
               print(e)
               return jsonify(error=str(e)), 400
        

@lease_bp.route("/assign-operator", methods=["POST"])
def lets_assign_operator():
        try:
                data = request.json
                company_id = request.environ.get("company_security_id")
                lease_id = data["lease_id"]
                operator_name = data["operator_name"]
                operator_id = data["operator_id"]
                resp = assign_operator(company_id=company_id, lease_id=lease_id, operator_id=operator_id, operator_name=operator_name)
                return resp, 201
        except Exception as e:
                return jsonify(error=str(e)), 400
        
@lease_bp.route("/get-operator-by-lease-id", methods=["GET"])
def let_get_all_operator_by_lease_id():
        try:
                company_id = request.environ.get("company_security_id")
                lease_id = request.headers.get("lease-id")
                resp = get_operator_by_lease_id(company_id=company_id, lease_id=lease_id)
                return resp, 200
        except Exception as e:
                return jsonify(error=str(e)), 400
        
@lease_bp.route("/delete-mapping-operator-by-id", methods=["DELETE"])
def delete_operator_by_id():
        try:
                company_id = request.environ.get("company_security_id")
                mapping_id = request.headers.get("mapping-id")
                resp = remove_lease_operator(company_id=company_id, mapping_id=mapping_id)
                return resp, 200
        except Exception as e:
                return jsonify(error=str(e)), 400
        

@lease_bp.route("/get-json-data", methods=["GET"])
def lets_get_json_data():
        try:
            company_id = request.environ.get("company_security_id")
            data =  get_all_json_data_in_lease_by_company(company_id=company_id)
            return data, 200
        except Exception as e:
              return jsonify(error=str(e)), 400
        
@lease_bp.route("/entry-excel-data", methods=["POST"])
def lets_entry_excel_data():
    try:
        data = request.files["excel"]
        action = request.form.to_dict(flat=True)
        # print(action)
        try:
            excel_data = pandas.read_excel(data, engine='xlrd')
        except:
            excel_data = pandas.read_excel(data, engine='openpyxl')
        class_func = main_odoo_function(func_type="entry_excel_data")
        json_data = class_func.vaildate_data(excel_data)
        if json_data:
            if action:
                resp = class_func.entry_excel_data(conflict_type=action["action"])
            else:
                resp = class_func.entry_excel_data()
        return resp , 200
    except Exception as e:
        print(e)
        return jsonify(error=str(e)), 400
    

@lease_bp.route("/get-time-sheet")
def get_time_sheet():
    try:
        rent_odoo_id = request.headers.get("rent-odoo-id")
        # print(rent_odoo_id)
        class_func = main_odoo_function(func_type="entry_excel_data")
        data = class_func.get_table_by_r_s_o_id(rent_odoo_id)
        # print(data)
        return data, 200
    except Exception as e:
          raise e   