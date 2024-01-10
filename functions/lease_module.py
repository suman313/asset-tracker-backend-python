from config import db, get_file
from models.lease import Lease
from models.asset import Asset
from models.photo import Photo
from models.attachment import Attachment
from models.lease_operator import Lease_Operator_Mapping
from models.lease_map import Lease_map
from models.operator import Operator
from functions.asset_module import get_asset_nos_and_ids
import datetime
import random


def check_lease_status(data):
        now_date = datetime.datetime.now()
        entry_start_date = datetime.datetime.strptime(str(data.get("rental_start_date")), '%Y-%m-%d')
        entry_end_date = datetime.datetime.strptime(str(data.get("rental_end_date")), '%Y-%m-%d')
        if entry_start_date <= now_date and  entry_end_date >= now_date:
            return "active"
        else:
            return "inactive"

def create_lease(data=None, company_id=None):
    try:
        asset_id = data.get("asset_id")
        check_status = Lease.query.filter_by(asset_id=asset_id).first()
        print(check_status.lease_status)
        if check_status is None or check_status.lease_status == "inactive" or check_status.lease_status == "expired":
            fild_id = gen_a_LeaseKey(company_id, asset_id=data.get("asset_id"))
            new_lease = Lease(
                lease_type=data.get("lease_type"),
                customer_po_no=data.get("customer_po_no"),
                currency=data.get("currency"),
                rental_start_date=data.get("rental_start_date"),
                rental_end_date=data.get("rental_end_date"),
                customer=data.get("customer"),
                lease_status=check_lease_status(data),
                contract_value=data.get("contract_value"),
                transportation_charge=data.get("transportation_charge"),
                normal_amount=data.get("normal_amount"),
                overtime_amount=data.get("overtime_amount"),
                reimbursements=data.get("reimbursements"),
                total_claimable_amount=data.get("total_claimable_amount"),
                asset_id=data.get("asset_id"),
                odoo_order_id = data.get("odoo_order_id"),
                fild_id=fild_id,
                company_id=company_id,
            )
            db.session.add(new_lease)
            db.session.commit()
            new_lease_map = Lease_map(
                sale_person = data.get("sale_person"),
                lease_id = new_lease.id
            )
            db.session.add(new_lease_map)
            db.session.commit()
            new_lease.sale_person = data.get("sale_person")
            return new_lease
        else:
            raise Exception(
                "one asset only have one acitve lease or one complete lease"
            )
    except Exception as e:
        raise e

def check_sale_person(data):
    try:  
        return  data.lease_map[0].sale_person
    except:  
        return None

def update_lease_by_id(lease_id, data):
    try:
        lease = Lease.query.filter_by(id=lease_id).first()
        if lease == None:
            raise Exception("lease not found")
        lease.lease_type = data.get("lease_type") or lease.lease_type
        lease.customer_po_no = data.get("customer_po_no") or lease.customer_po_no
        lease.currency = data.get("currency") or lease.currency
        lease.rental_start_date = data.get("rental_start_date") or lease.rental_start
        lease.odoo_order_id = data.get("odoo_order_id") or lease.odoo_order_id
        lease.rental_end_date = data.get("rental_end_date") or lease.rental_end_date
        lease.customer = data.get("customer") or lease.customer
        check_lease_sale_person = check_sale_person(lease)
        if check_lease_sale_person != None or check_lease_sale_person == "":
            lease.lease_map[0].sale_person = data.get("sale_person") or lease.lease_map[0].sale_person
        elif data.get("sale_person"):
            new_lease_map = Lease_map(
                sale_person = data.get("sale_person"),
                lease_id = lease_id
            )
            db.session.add(new_lease_map)

        lease.lease_status = check_lease_status({"rental_start_date": lease.rental_start_date, "rental_end_date": lease.rental_end_date})
        lease.contract_value = data.get("contract_value") or lease.contract_value
        lease.transportation_charge = (
            data.get("transportation_charge") or lease.transportation_charge
        )
        lease.normal_amount = data.get("normal_amount") or lease.normal_amount
        lease.overtime_amount = data.get("overtime_amount") or lease.overtime_amount
        lease.reimbursements = data.get("reimbursements") or lease.reimbursements
        lease.total_claimable_amount = (
            data.get("total_claimable_amount") or lease.total_claimable_amount
        )
        lease.asset_id = data.get("asset_id") or lease.asset_id
        db.session.commit()
        return {
            "id": lease.id,
            "lease_type": lease.lease_type,
            "customer_po_no": lease.customer_po_no,
            "currency": lease.currency,
            "rental_start_date": lease.rental_start_date,
            "rental_end_date": lease.rental_end_date,
            "customer": lease.customer,
            "sale_person": check_sale_person(lease),
            "lease_status": lease.lease_status,
            "contract_value": lease.contract_value,
            "transportation_charge": lease.transportation_charge,
            "normal_amount": lease.normal_amount,
            "overtime_amount": lease.overtime_amount,
            "reimbursements": lease.reimbursements,
            "odoo_order_id": lease.odoo_order_id,
            "total_claimable_amount": lease.total_claimable_amount,
            "asset_id": lease.asset_id,
        }
    except Exception as e:
        print(e)
        raise e


def delete_lease_by_id(lease_id):
    try:
        lease = Lease.query.filter_by(id=lease_id).first()
        lease_operator_mapping = Lease_Operator_Mapping.query.filter_by(lease_id=lease_id).all()
        if len(lease_operator_mapping) >= 1:
            for lease_operator in lease_operator_mapping:
                db.session.delete(lease_operator)
        if check_sale_person(lease):
            lease_map = Lease_map.query.filter_by(lease_id=lease_id).first()
            db.session.delete(lease_map)
        db.session.delete(lease)
        db.session.commit()
        return lease
    except Exception as e:
        raise e


def get_lease_by_id(lease_id):
    try:
        lease = Lease.query.filter_by(id=lease_id).first()
        attachments = Attachment.query.filter_by(lease_id=lease_id).all()
        photos = Photo.query.filter_by(lease_id=lease_id).all()
        all_photos = []
        all_attachments = []
        for photo in photos:
            url_data = photo.image_uri.split("/")[1] + "/" + photo.image_uri.split("/")[2]
            url = get_file(url_data)
            all_photos.append(
                {
                    "id": photo.id,
                    "asset_id": photo.asset_id,
                    "image_uri": url,
                }
            )

        for attachment in attachments:
            url_data = attachment.doc_uri.split("/")[1] + "/" + attachment.doc_uri.split("/")[2]
            url = get_file(url_data)
            all_attachments.append(
                {
                    "id": attachment.id,
                    "serial_no": attachment.serial_no,
                    "types": attachment.types,
                    "doc_uri": url,
                    "doc_expiry_date": attachment.doc_expiry_date,
                    "archive_flag": attachment.archive_flag,
                }
            )

        return {
            "id": lease.id,
            "lease_type": lease.lease_type,
            "customer_po_no": lease.customer_po_no,
            "currency": lease.currency,
            "rental_start_date": lease.rental_start_date,
            "rental_end_date": lease.rental_end_date,
            "customer": lease.customer,
            "sale_person": check_sale_person(lease),
            "lease_status": lease.lease_status,
            "fild_id": lease.fild_id,
            "contract_value": lease.contract_value,
            "transportation_charge": lease.transportation_charge,
            "normal_amount": lease.normal_amount,
            "overtime_amount": lease.overtime_amount,
            "reimbursements": lease.reimbursements,
            "total_claimable_amount": lease.total_claimable_amount,
            "asset_id": lease.asset_id,
            "odoo_order_id": lease.odoo_order_id,
            "photos": all_photos,
            "attachments": all_attachments,
        }
    except Exception as e:
        raise e


def get_lease_list(
    asset_id=None,
    company_id=None,
    limit=None,
    offset=None,
    lease_genarated_id=None,
    start_date=None,
    end_date=None,
):
    try:
        if company_id != None:
            normal_leases_for_company = Lease.query.filter_by(company_id=company_id)
        else:
            normal_leases_for_company = Lease.query

        if asset_id != None:
            normal_leases_for_company = normal_leases_for_company.filter_by(
                asset_id=asset_id
            )
        elif lease_genarated_id != None:
            nonlocal_leases_for_company = nonlocal_leases_for_company.filter_by(
                fild_id=lease_genarated_id
            )
        full_data = normal_leases_for_company.all()
        count_data = len(full_data)

        if offset != None and limit != None:
            leases = normal_leases_for_company.offset(offset).limit(limit)
        elif limit != None:
            leases = normal_leases_for_company.limit(limit)
        else:
            leases = normal_leases_for_company.all()
        if start_date != None and end_date != None:
            data = []
            data_for_count = []
            request_start_time = datetime.datetime(
                int(start_date.split("-")[2]),
                int(start_date.split("-")[1]),
                int(start_date.split("-")[0]),
            ).timestamp()
            request_end_time = datetime.datetime(
                int(end_date.split("-")[2]),
                int(end_date.split("-")[1]),
                int(end_date.split("-")[0]),
            ).timestamp()
            for lease in full_data:
                print(lease)
                # year = 2018, month = 7, day = 12, hour = 7, minute = 9, second = 33
                lease_start_date_in_time = datetime.datetime(
                    int(lease.rental_start_date.split("-")[0]),
                    int(lease.rental_start_date.split("-")[1]),
                    int(lease.rental_start_date.split("-")[2]),
                ).timestamp()
                # print(lease_start_date_in_time)
                lease_end_date_in_time = datetime.datetime(
                    year=int(lease.rental_end_date.split("-")[0]),
                    month=int(lease.rental_end_date.split("-")[1]),
                    day=int(lease.rental_end_date.split("-")[2]),
                    hour=0,
                    minute=0,
                    second=0,
                ).timestamp()
                # print(lease_end_date_in_time)
                if (
                    lease_start_date_in_time >= request_start_time
                    and lease_end_date_in_time <= request_end_time
                ):
                    data_for_count.append(lease)
            for lease in leases:
                # print(lease)
                lease_start_date_in_time = datetime.datetime(
                    year=int(lease.rental_start_date.split("-")[0]),
                    month=int(lease.rental_start_date.split("-")[1]),
                    day=int(lease.rental_start_date.split("-")[2]),
                    hour=0,
                    minute=0,
                    second=0,
                ).timestamp()
                lease_end_date_in_time = datetime.datetime(
                    year=int(lease.rental_end_date.split("-")[0]),
                    month=int(lease.rental_end_date.split("-")[1]),
                    day=int(lease.rental_end_date.split("-")[2]),
                    hour=0,
                    minute=0,
                    second=0,
                ).timestamp()
                if (
                    lease_start_date_in_time >= request_start_time
                    and lease_end_date_in_time <= request_end_time
                ):
                    data.append(lease)
            leases = data
            count_data = len(data_for_count)

        lease_list = []
        list_of_assets = Asset.query.with_entities(Asset.asset_no, Asset.id).filter(Asset.company_id==company_id).all()
        asset_no_object = {}
        for asset in list_of_assets:
            asset_no_object[asset.id] = asset.asset_no
        # print (asset_no_object)
        for lease in leases:
            asset_no_for_lease = asset_no_object.get(lease.asset_id, "")

                
            lease_list.append(
                {
                    "id": lease.id,
                    "lease_type": lease.lease_type,
                    "rental_start_date": lease.rental_start_date,
                    "rental_end_date": lease.rental_end_date,
                    "lease_status": lease.lease_status,
                    "customer_po_no": lease.customer_po_no,
                    "customer": lease.customer,
                    "odoo_order_id": lease.odoo_order_id,
                    "sale_person": check_sale_person(lease),
                    "total_claimable_amount": lease.total_claimable_amount,
                    "asset_id": lease.asset_id,
                    "asset_no": asset_no_for_lease,
                    "total_data": count_data,
                }
            )
        return lease_list

    except Exception as e:
        print(e)
        raise e


def get_lease_no_and_ids(company_id):
    try:
        leases = (
            Lease.query.with_entities(Lease.id, Lease.fild_id)
            .filter_by(company_id=company_id)
            .all()
        )
        leases_data = []
        for lease in leases:
            leases_data.append({"id": lease.id, "no": lease.fild_id})
        return leases_data
    except Exception as e:
        print(e)
        raise Exception("Lease object problem")


def get_lease_list_for_search(company_id):
    try:
        leases = (
            Lease.query.with_entities(
                Lease.fild_id, Lease.lease_status, Lease.lease_type
            )
            .filter_by(company_id=company_id)
            .all()
        )
        asset_nos = get_asset_nos_and_ids(company_id=company_id)
        lease_nos = []
        lease_status_obj = {}
        lease_type_obj = {}
        lease_status_list = []
        lease_type_list = []

        for lease in leases:
            lease_nos.append(lease.fild_id)
            if lease_status_obj.get(lease.lease_status) != None:
                lease_status_obj[lease.lease_status] += 1
            else:
                lease_status_obj[lease.lease_status] = 1
            if lease_type_obj.get(lease.lease_type) != None:
                lease_type_obj[lease.lease_type] += 1
            else:
                lease_type_obj[lease.lease_type] = 1
        for key, value in lease_status_obj.items():
            lease_status_list.append(key)
        for key, value in lease_type_obj.items():
            lease_type_list.append(key)

        return {
            "asset_no": asset_nos,
            "lease_type": lease_type_list,
            "lease_status": lease_status_list,
            "lease_no": lease_nos,
        }

    except Exception as e:
        raise e


def gen_a_LeaseKey(company_id, asset_id):
    try:
        pre_text = "MAC"
        copm_Array = list(str(company_id))
        asse_Array = list(str(asset_id))
        first_num = copm_Array[0] + copm_Array[1] + copm_Array[2] + copm_Array[3]
        asset_num = asse_Array[0] + asse_Array[1] + asse_Array[2] + asse_Array[3]
        random_string = "1234567890469007865294806S780956839025968O342502543"
        arrange_string = (
            random_string[int(random.random() * 30)]
            + random_string[int(random.random() * 30)]
            + random_string[int(random.random() * 30)]
            + random_string[int(random.random() * 30)]
            + random_string[int(random.random() * 34)]
        )
        main_string = f"{pre_text}-{first_num}{asset_num}{arrange_string}".upper()
        # print(main_string)
        data = Lease.query.filter_by(fild_id=main_string).first()
        if data is None:
            # print(main_string1, main_string2)
            return main_string
        else:
            gen_a_LeaseKey(company_id, asset_id)
    except Exception as e:
        raise e


def assign_operator(company_id, lease_id, operator_id, operator_name):
    try:
        in_codition = Lease_Operator_Mapping.query.filter(
            Lease_Operator_Mapping.company_id == company_id,
            Lease_Operator_Mapping.lease_id == lease_id,
        ).count()
        if in_codition <= 2:
            new_lease_operator_mapping = Lease_Operator_Mapping(
                operator_id=operator_id,
                operator_name=operator_name,
                company_id=company_id,
                lease_id=lease_id,
            )
            db.session.add(new_lease_operator_mapping)
            db.session.commit()
            return {
                "id": new_lease_operator_mapping.id,
                "operator_id": new_lease_operator_mapping.operator_id,
                "operator_name": new_lease_operator_mapping.operator_name,
                "company_id": new_lease_operator_mapping.company_id,
                "lease_id": new_lease_operator_mapping.lease_id,
            }
        else:
            raise Exception("max value for operator number reached")

    except Exception as e:
        raise e


def get_operator_by_lease_id(lease_id, company_id):
    try:
        array_operator = []
        all_operator = Lease_Operator_Mapping.query.filter(
            Lease_Operator_Mapping.company_id == company_id,
            Lease_Operator_Mapping.lease_id == lease_id,
        ).all()
        for operator in all_operator:
            array_operator.append(
                {
                    "id": operator.id,
                    "operator_id": operator.operator_id,
                    "operator_name": operator.operator_name,
                    "company_id": operator.company_id,
                    "lease_id": operator.lease_id,
                }
            )
        return array_operator

    except Exception as e:
        raise e


def remove_lease_operator(company_id, mapping_id):
    try:
        lease_operator = Lease_Operator_Mapping.query.filter(
            Lease_Operator_Mapping.company_id == company_id,
            Lease_Operator_Mapping.id == mapping_id,
        ).first()
        db.session.delete(lease_operator)
        db.session.commit()
        return f"{lease_operator.id} deleted from Lease-Operator-Mapping successfully"
    except Exception as e:
        raise e


def get_all_json_data_in_lease_by_company(company_id):
    try:
        all_leases = (
            Lease.query.filter(Lease.company_id == company_id) 
            .all()
        )
        list_of_assets = (
            Asset.query.with_entities(Asset.asset_no, Asset.id)
                .filter(Asset.company_id==company_id).all()
            )
        asset_no_object = {}
        for asset in list_of_assets:
            asset_no_object[f"{asset.id}"] = asset.asset_no

        leases_data = []
        for lease in all_leases:
            asset_no_for_lease = asset_no_object.get(f"{lease.asset_id}", "")
            leases_data.append(
                {
                    "id": lease.id,
                    "lease_type": lease.lease_type,
                    "customer_po_no": lease.customer_po_no,
                    "currency": lease.currency,
                    "rental_start_date": lease.rental_start_date,
                    "rental_end_date": lease.rental_end_date,
                    "customer": lease.customer,
                    "sale_person": check_sale_person(lease),
                    "lease_status": lease.lease_status,
                    "field_id": lease.fild_id,
                    "contract_value": lease.contract_value,
                    "transportation_charge": lease.transportation_charge,
                    "normal_amount": lease.normal_amount,
                    "overtime_amount": lease.overtime_amount,
                    "reimbursements": lease.reimbursements,
                    "total_claimable_amount": lease.total_claimable_amount,
                    "asset_no": asset_no_for_lease,
                }
            )
        return leases_data
    except Exception as e:
        print(e)
        raise e