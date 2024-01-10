from config import db, get_file
from models.maintenance import Maintenance
from models.asset import Asset
from models.photo import Photo
from models.attachment import Attachment
from models.parts import Parts
import datetime
from functions.lease_module import get_lease_no_and_ids
from functions.asset_module import get_asset_nos_and_ids


def create_maintenance(data=None, company_id=None):
    try:
        asset_id = data.get("asset_id")
        scheduled_date = data.get("scheduled_date")
        maintenance_by_asset_id = Maintenance.query.filter_by(asset_id=asset_id).first()
        asset = Asset.query.with_entities(Asset.asset_no).filter_by(id=asset_id).first()
        if (
            maintenance_by_asset_id is None
            or maintenance_by_asset_id.status == "complete"
            and datetime.datetime.strptime(scheduled_date, "%Y-%m-%d")
            - datetime.datetime.strptime(
                maintenance_by_asset_id.scheduled_date, "%Y-%m-%d"
            )
            >= 1
        ):
            new_maintenace = Maintenance(
                status=data.get("status"),
                description=data.get("description"),
                asset_no= asset.asset_no,
                scheduled_date=data.get("scheduled_date"),
                types=data.get("types"),
                asset_name=data.get("asset_name"),
                asset_id=data.get("asset_id"),
                lease_id=data.get("lease_id"),
                company_id=company_id,
            )
            db.session.add(new_maintenace)
            db.session.commit()

            for part in data.get("parts"):
                new_parts = Parts(
                    part_no=part.get("part_no"),
                    quantity=part.get("quantity"),
                    price=part.get("price") or "",
                    installation=part.get("installation") or False,
                    maintenance_id=new_maintenace.id,
                )
                db.session.add(new_parts)

            db.session.commit()
            return new_maintenace
        else:
            print(maintenance_by_asset_id)
            raise Exception("please check your input data and try again")
    except Exception as e:
        print(e)
        raise e


def get_maintenance_list(
    asset_id=None,
    lease_id=None,
    company_id=None,
    limit=None,
    offset=None,
    scheduled_date_to=None,
    scheduled_date_from=None,
):
    try:
        if company_id != None:
            normal_maintenaces_for_company = Maintenance.query.with_entities(
                Maintenance.id,
                Maintenance.asset_no,
                Maintenance.status,
                Maintenance.scheduled_date,
                Maintenance.types,
                Maintenance.asset_id,
                Maintenance.lease_id,
            ).filter_by(company_id=company_id)

        else:
            normal_maintenaces_for_company = Maintenance.query.with_entities(
                Maintenance.id,
                Maintenance.asset_no,
                Maintenance.status,
                Maintenance.scheduled_date,
                Maintenance.types,
                Maintenance.asset_id,
                Maintenance.lease_id,
            )

        if lease_id != None:
            normal_maintenaces_for_company = normal_maintenaces_for_company.filter_by(
                lease_id=lease_id
            )
        elif asset_id != None:
            normal_maintenaces_for_company = normal_maintenaces_for_company.filter_by(
                asset_id=asset_id
            )

        data_count = len(normal_maintenaces_for_company.all())

        if limit != None and offset != None:
            maintenances = normal_maintenaces_for_company.limit(limit).offset(offset)
        elif limit != None:
            maintenances = normal_maintenaces_for_company.limit(limit)
        else:
            maintenances = normal_maintenaces_for_company.all()

        if scheduled_date_from != None and scheduled_date_to != None:
            data_list = []
            for mainte in maintenances:
                maintenance_start_date_in_time = datetime.datetime(
                    int(mainte.scheduled_date.split("-")[2]),
                    int(mainte.scheduled_date.split("-")[1]),
                    int(mainte.scheduled_date.split("-")[0]),
                    0,
                    0,
                )
                request_start_time = datetime.datetime(
                    int(scheduled_date_to.split("-")[2]),
                    int(scheduled_date_to.split("-")[1]),
                    int(scheduled_date_to.split("-")[0]),
                )
                request_end_time = datetime.datetime(
                    int(scheduled_date_from.split("-")[2]),
                    int(scheduled_date_from.split("-")[1]),
                    int(scheduled_date_from.split("-")[0]),
                )
                if (
                    maintenance_start_date_in_time >= request_start_time
                    and maintenance_start_date_in_time <= request_end_time
                ):
                    data_list.append(mainte)
            maintenances = data_list

        # print(maintenances)
        maintenance_list = []
        for maintenance in maintenances:
            maintenance_list.append(
                {
                    "id": maintenance.id,
                    "asset_no": maintenance.asset_no,
                    "status": maintenance.status,
                    "scheduled_date": maintenance.scheduled_date,
                    "types": maintenance.types,
                    "asset_id": maintenance.asset_id,
                    "lease_id": maintenance.lease_id,
                    "total_data": data_count,
                }
            )

        return maintenance_list
    except Exception as e:
        print(e)
        raise Exception("not found maintenance")


def get_maintenance_by_id(id):
    try:
        maintenance = Maintenance.query.filter_by(id=id).first()
        photos = Photo.query.filter(Photo.maintenance_id==id).all()
        attachments = Attachment.query.filter_by(maintenance_id=id).all()
        parts_s = Parts.query.filter_by(maintenance_id=id).all()
        parts_list = []
        photo_list = []
        attachments_list = []
        for photo in photos:
            url_data = photo.image_uri.split("/")[1] + "/" + photo.image_uri.split("/")[2]
            url = get_file(url_data)
            photo_list.append(
                {
                    "id": photo.id,
                    "asset_id": photo.asset_id,
                    "image_uri": photo.image_uri,
                }
            )
        for attachment in attachments:
            url_data = attachment.doc_uri.split("/")[1] + "/" + attachment.doc_uri.split("/")[2]
            url = get_file(url_data)
            attachments_list.append(
                {
                    "id": attachment.id,
                    "asset_id": attachment.asset_id,
                    "doc_uri": url,
                }
            )
        for part in parts_s:
            parts_list.append(
                {
                    "id": part.id,
                    "part_no": part.part_no,
                    "quantity": part.quantity,
                    "price": part.price,
                    "installation": part.installation,
                    "maintenance_id": part.maintenance_id,
                }
            )

        return {
            "id": maintenance.id,
            "asset_no": maintenance.asset_no,
            "status": maintenance.status,
            "description": maintenance.description,
            "scheduled_date": maintenance.scheduled_date,
            "types": maintenance.types,
            "asset_id": maintenance.asset_id,
            "lease_id": maintenance.lease_id,
            "photos": photo_list,
            "attachments": attachments_list,
            "parts": parts_list,
        }
    except Exception as e:
        raise e


def update_maintenance(id, data):
    try:
        maintenance = Maintenance.query.filter_by(id=id).first()
        if maintenance:
            maintenance.status = data.get("status") or maintenance.status
            maintenance.description = data.get("description") or maintenance.description
            maintenance.scheduled_date = (
                data.get("scheduled_date") or maintenance.scheduled_date
            )
            maintenance.types = data.get("types") or maintenance.types
            maintenance.asset_no = data.get("asset_no") or maintenance.asset_no
            maintenance.asset_id = data.get("asset_id") or maintenance.asset_id
            maintenance.lease_id = data.get("lease_id") or maintenance.lease_id
            db.session.commit()
            return {
                "id": maintenance.id,
                "status": maintenance.status,
                "description": maintenance.description,
                "scheduled_date": maintenance.scheduled_date,
                "types": maintenance.types,
                "asset_no": maintenance.asset_no,
                "asset_id": maintenance.asset_id,
                "lease_id": maintenance.lease_id,
            }
        raise Exception("please provide correct information")
    except Exception as e:
        raise e


def delete_maintenance(id):
    try:
        maintenance = Maintenance.query.filter_by(id=id).first()
        parts_array = Parts.query.filter_by(maintenance_id=maintenance.id).all()
        part_id_list = []
        for part in parts_array:
            part_id_list.append({"id": part.id})
            db.session.delete(part)

        db.session.delete(maintenance)
        db.session.commit()
        return {"id": maintenance.id, "parts": part_id_list}
    except Exception as e:
        raise e


def update_parts(id=None,data=None,):
    print(id, data.get("id"))
    try:
        parts = (
            Parts.query.filter_by(maintenance_id=id)
            .filter_by(id=data.get("id"))
            .first()
        )
        if parts is None or data.get("id") is None:
            new_parts = Parts(
                part_no=data.get("part_no"),
                quantity=data.get("quantity"),
                price=data.get("price"),
                installation=data.get("installation"),
                maintenance_id=id,
            )
            db.session.add(new_parts)
            db.session.commit()
            return {
                "id": new_parts.id,
                "part_no": new_parts.part_no,
                "quantity": new_parts.quantity,
                "price": new_parts.price,
                "installation": new_parts.installation,
                "maintenance_id": new_parts.maintenance_id,
            }
        else:
            parts_update = Parts.query.filter_by(id=data.get("id")).first()
            parts_update.part_no = data.get("part_no") or parts_update.part_no
            parts_update.quantity = data.get("quantity") or parts_update.quantity
            parts_update.price = data.get("price") or parts_update.price
            if parts_update.installation is not None:
                parts_update.installation = data.get("installation")
            db.session.commit()
            return {
                "id": parts_update.id,
                "part_no": parts_update.part_no,
                "quantity": parts_update.quantity,
                "price": parts_update.price,
                "installation": parts_update.installation,
                "maintenance_id": parts_update.maintenance_id,
            }

    except Exception as e:
        print("part")
        raise e


def delete_parts(id):
    try:
        parts = Parts.query.filter_by(id=id).first()
        db.session.delete(parts)
        db.session.commit()
        return parts
    except Exception as e:
        raise e


def get_data_list_for_search(company_id: str or None):
    try:
        new_maintenance_search_data = (
            Maintenance.query.with_entities(
                Maintenance.asset_id,
                Maintenance.scheduled_date,
                Maintenance.status,
                Maintenance.lease_id,
            )
            .filter_by(company_id=company_id)
            .all()
        )
        list_scheduled_date = []
        list_status = []
        list_scheduled_date_counter = []
        list_status_counter = []

        dict_for_asset = {}
        dict_for_scheduled_date = {}
        dict_for_lease_id = {}
        dict_for_asset_status = {}
        count_maintenance = 0
        for maintenance in new_maintenance_search_data:
            count_maintenance += 1
            if dict_for_asset.get(maintenance.asset_id) != None:
                dict_for_asset[maintenance.asset_id] = (
                    int(dict_for_asset[maintenance.asset_id]) + 1
                )
            else:
                dict_for_asset[maintenance.asset_id] = 1
            if dict_for_scheduled_date.get(maintenance.scheduled_date) != None:
                dict_for_scheduled_date[maintenance.scheduled_date] = (
                    int(dict_for_scheduled_date[maintenance.scheduled_date]) + 1
                )
            else:
                dict_for_scheduled_date[maintenance.scheduled_date] = 1
            if dict_for_lease_id.get(maintenance.lease_id) != None:
                dict_for_lease_id[maintenance.lease_id] = (
                    int(dict_for_lease_id[maintenance.lease_id]) + 1
                )
            else:
                dict_for_lease_id[maintenance.lease_id] = 1
            if dict_for_asset_status.get(maintenance.status) != None:
                dict_for_asset_status[maintenance.status] = (
                    int(dict_for_asset_status[maintenance.status]) + 1
                )
            else:
                dict_for_asset_status[maintenance.status] = 1

        for key, value in dict_for_asset_status.items():
            list_status.append(str(key))
            list_status_counter.append({str(key): value})

        for key, value in dict_for_scheduled_date.items():
            list_scheduled_date.append(str(key))
            list_scheduled_date_counter.append({str(key): value})

        asset_nos = get_asset_nos_and_ids(company_id=company_id)
        lease_nos = get_lease_no_and_ids(company_id=company_id)

        return {
            "status": list_status,
            "scheduled_date": list_scheduled_date,
            "asset_no": asset_nos,
            "lease_no": lease_nos,
            "counter": {
                "maintenance": count_maintenance,
                "status": list_status_counter,
                "scheduled_date": list_scheduled_date_counter,
            },
        }
    except Exception as e:
        print(e)
        raise e


def get_all_json_data_in_maintenance_by_company(company_id):
    try:
        all_maintenances = (
            Maintenance.query.filter(Maintenance.company_id == company_id)
            .join(Parts)
            .all()
        )
        all_maintenance_list = []
        for maintenance in all_maintenances:
            parts_list = []
            for part in maintenance.part:
                parts_list.append(
                    {
                        "id": part.id,
                        "part_no": part.part_no,
                        "quantity": part.quantity,
                        "price": part.price,
                        "installation": part.installation,
                        "maintenance_id": part.maintenance_id,
                    }
                )
            all_maintenance_list.append(
                {
                    "id": maintenance.id,
                    "asset_name": maintenance.asset_name,
                    "status": maintenance.status,
                    "description": maintenance.description,
                    "scheduled_date": maintenance.scheduled_date,
                    "types": maintenance.types,
                    "asset_id": maintenance.asset_id,
                    "lease_id": maintenance.lease_id,
                    "parts": parts_list,
                }
            )
        return all_maintenance_list
    except Exception as e:
        raise e
