from config import db, get_file
from models.asset import Asset
from models.photo import Photo
from models.maintenance import Maintenance
from models.attachment import Attachment
from models.asset_config import AssetConfig
from models.lease import Lease
import time
from models.asset_config import AssetConfig
from functions.asset_details import get_details, delete_details


def create_asset(data=None, company_id=None):
    try:
        if data != None:
            asset_check = Asset.query.with_entities(Asset.asset_no, Asset.id).filter(Asset.company_id == company_id, Asset.asset_no == data["asset_no"]).first()
            if not(asset_check):
                new_asset = Asset(
                    asset_no=data.get("asset_no", None) or " ",
                    make=data.get("make", None) or " ",
                    model=data.get("model", None) or " ",
                    yom=data.get("yom", None) or " ",
                    category=data.get("category", None) or "nill",
                    description=data.get("description", None) or " ",
                    serial_no=data.get("serial_no", None) or " ",
                    purchased_from=data.get("purchased_from") or " ",
                    rfid=data.get("rfid", None) or "nill",
                    device_id=data.get("device_id", None) or " ",
                    platform=data.get("platform", None) or " ",
                    group=data.get("group", None) or " ",
                    device_hash=data.get("device_hash", None) or "nill",
                    site_location=data.get("site_location", None) or " ",
                    created_at=time.time(),
                    company_id=company_id,
                )
                db.session.add(new_asset)
                db.session.commit()
                print(new_asset.id)
                return new_asset
            else:
                Exception("plese give asset no unique")
        else:
            print("Error creating")
            raise Exception("please give a valid parameter")

    except Exception as e:
        print(e)
        raise Exception(str(e))


def create_asset_config(data):
    try:
        new_asset_config = AssetConfig(
            used_or_new=data["used_or_new"],
            ansi_or_new=data["ansi_or_new"],
            machine_ownership_type=data["machine_ownership_type"],
            battery_type=data["battery_type"],
            engine_serial_no=data["engine_serial_no"],
            two_or_four_wd=data["two_or_four_wd"],
            accessories=data["accessories"],
            tyres=data["tyres"],
            asset_id=data["asset_id"],
        )
        db.session.add(new_asset_config)
        db.session.commit()

        return new_asset_config
    except Exception as e:
        raise e


def update_asset_config(id, data):
    try:
        asset_config = AssetConfig.query.filter_by(asset_id=id).first()
        asset_config.used_or_new = data.get("used_or_new") or asset_config.used_or_new
        asset_config.ansi_or_new = data.get("ansi_or_new") or asset_config.ansi_or_new
        asset_config.machine_ownership_type = (
            data.get("machine_ownership_type") or asset_config.machine_ownership_type
        )
        asset_config.battery_type = (
            data.get("battery_type") or asset_config.battery_type
        )
        asset_config.engine_serial_no = (
            data.get("engine_serial_no") or asset_config.engine_serial_no
        )
        asset_config.two_or_four_wd = (
            data.get("two_or_four_wd") or asset_config.two_or_four_wd
        )
        asset_config.accessories = data.get("accessories") or asset_config.accessories
        asset_config.tyres = data.get("tyres") or asset_config.tyres
        db.session.commit()
        return {
            "used_or_new": asset_config.used_or_new,
            "ansi_or_new": asset_config.ansi_or_new,
            "machine_ownership_type": asset_config.machine_ownership_type,
            "battery_type": asset_config.battery_type,
            "engine_serial_no": asset_config.engine_serial_no,
            "two_or_four_wd": asset_config.two_or_four_wd,
            "accessories": asset_config.accessories,
            "tyres": asset_config.tyres,
        }
    except Exception as e:
        print(e)
        raise e


def get_asset_list(
    company_id=None,
    asset_no=None,
    category=None,
    limit=None,
    offset=None,
    yom=None,
    unassigned_asset=None,
    not_in_maintenance=None,
    inactive_asset=None,
    # rental_end_date=None,
    rental_start_date=None,
):
    data_obj = []
    lease_obj = {}
    if company_id is not None:
        normal_assets_company_wise = Asset.query.with_entities(
            Asset.id,
            Asset.model,
            Asset.asset_no,
            Asset.serial_no,
            Asset.yom,
            Asset.category,
            Asset.make,
            Asset.rfid,
            Asset.device_hash,
            Asset.created_at,
        ).filter_by(company_id=company_id)
        if asset_no != None:
            normal_assets_company_wise = normal_assets_company_wise.filter_by(
                asset_no=asset_no
            )
        elif category != None:
            normal_assets_company_wise = normal_assets_company_wise.filter_by(
                category=category
            )
        elif yom != None:
            normal_assets_company_wise = normal_assets_company_wise.filter_by(make=yom)
        # elif rental_end_date and rental_start_date:
        elif rental_start_date:
            normal_assets_company_wise = normal_assets_company_wise.join(Lease).filter(
                Lease.rental_end_date <= rental_start_date
            )
        if unassigned_asset != None:
            leases = (
                Lease.query.with_entities(Lease.asset_id, Lease.lease_status)
                .filter_by(company_id=company_id)
                .all()
            )
            for lease in leases:
                lease_obj[str(lease.asset_id)] = lease.lease_status
        if not_in_maintenance:
            maintenaces = (
                Maintenance.query.with_entities(
                    Maintenance.asset_id, Maintenance.asset_no
                )
                .filter(
                    Maintenance.company_id == company_id,
                    Maintenance.status != "complete",
                )
                .all()
            )
            maintenance_object = {}
            for maintenace in maintenaces:
                maintenance_object[str(maintenace.asset_id)] = str(maintenace.asset_no)

        data_count = len(normal_assets_company_wise.all())

        if limit != None and offset != None:
            assets = normal_assets_company_wise.offset(offset).limit(limit)
        elif limit != None:
            assets = normal_assets_company_wise.limit(limit)
        else:
            assets = normal_assets_company_wise.all()
    else:
        assets = Asset.query.with_entities(
            Asset.id,
            Asset.model,
            Asset.asset_no,
            Asset.serial_no,
            Asset.yom,
            Asset.category,
            Asset.make,
            Asset.created_at,
        ).all()

    for asset in assets:
        if unassigned_asset:
            if (
                lease_obj.get(str(asset.id)) == None
                or lease_obj.get(str(asset.id)) == "inactive"
            ):
                data_obj.append(
                    {
                        "id": str(asset.id),
                        "model": asset.model,
                        "yom": asset.yom,
                        "asset_no": asset.asset_no,
                        "serial_no": asset.serial_no,
                        "category": asset.category,
                        "lease_status": lease_obj.get(str(asset.id), "not assigned"),
                        "make": asset.make,
                        "created_at": asset.created_at,
                        "total_data": data_count,
                    }
                )
        elif not_in_maintenance:
            if maintenance_object.get(str(asset.id)) == None:
                data_obj.append(
                    {
                        "id": str(asset.id),
                        "model": asset.model,
                        "yom": asset.yom,
                        "asset_no": asset.asset_no,
                        "serial_no": asset.serial_no,
                        "category": asset.category,
                        "make": asset.make,
                        "created_at": asset.created_at,
                        "total_data": data_count,
                    }
                )
        elif unassigned_asset == None and inactive_asset:
            if rental_start_date:
                data_obj.append(
                    {
                        "id": str(asset.id),
                        "model": asset.model,
                        "yom": asset.yom,
                        "asset_no": asset.asset_no,
                        "serial_no": asset.serial_no,
                        "category": asset.category,
                        "make": asset.make,
                        "lease_status": "inactive",
                        "created_at": asset.created_at,
                        "total_data": data_count,
                    }
                )
            elif (
                lease_obj.get(str(asset.id)) == None
                or lease_obj.get(str(asset.id)) == "inactive"
            ):
                data_obj.append(
                    {
                        "id": str(asset.id),
                        "model": asset.model,
                        "yom": asset.yom,
                        "asset_no": asset.asset_no,
                        "serial_no": asset.serial_no,
                        "category": asset.category,
                        "make": asset.make,
                        "lease_status": lease_obj.get(str(asset.id)) or "not assigned",
                        "created_at": asset.created_at,
                        "total_data": data_count,
                    }
                )
        elif unassigned_asset == None:
            data_obj.append(
                {
                    "id": str(asset.id),
                    "model": asset.model,
                    "yom": asset.yom,
                    "asset_no": asset.asset_no,
                    "serial_no": asset.serial_no,
                    "category": asset.category,
                    "make": asset.make,
                    "created_at": asset.created_at,
                    "total_data": data_count,
                }
            )
        else:
            data_obj.append(
                {
                    "id": str(asset.id),
                    "model": asset.model,
                    "yom": asset.yom,
                    "asset_no": asset.asset_no,
                    "serial_no": asset.serial_no,
                    "category": asset.category,
                    "make": asset.make,
                    "lease_status": lease_obj.get(str(asset.id)) or "not assigned",
                    "created_at": asset.created_at,
                    "total_data": data_count,
                }
            )

    return data_obj


def update_by_id(id, data):
    # print(data)
    asset = Asset.query.filter_by(id=id).first()
    if asset != None:
        asset.asset_no = data.get("asset_no") or asset.asset_no
        asset.make = data.get("make") or asset.make
        asset.model = data.get("model") or asset.model
        asset.yom = data.get("yom") or asset.yom
        asset.category = data.get("category") or asset.category
        asset.description = data.get("description") or asset.description
        asset.serial_no = data.get("serial_no") or asset.serial_no
        asset.purchased_from = data.get("purchased_from") or asset.purchased_from
        asset.rfid = data.get("rfid") or asset.rfid
        asset.site_location = data.get("site_location") or asset.site_location
        asset.device_id = data.get("device_id", None) or asset.device_id
        asset.platform = data.get("platform", None) or asset.platform
        asset.group = data.get("group", None) or asset.group
        asset.device_hash = data.get("device_hash", None) or asset.device_hash
        db.session.commit()
        return {
            "asset_no": asset.asset_no,
            "make": asset.make,
            "model": asset.model,
            "yom": asset.yom,
            "category": asset.category,
            "description": asset.description,
            "serial_no": asset.serial_no,
            "purchased_from": asset.purchased_from,
            "rfid": asset.rfid,
            "device_hash": asset.device_hash,
            "device_id": asset.device_id,
            "platform": asset.platform,
            "group": asset.group,
        }
    else:
        raise Exception("Couldn't find asset")


def delete_by_id(id):
    asset = Asset.query.filter_by(id=id).first()
    if asset != None:
        db.session.delete(asset)
        db.session.commit()
        asset_config = AssetConfig.query.filter_by(asset_id=id).first()
        delete_details(id)
        if asset_config != None:
            db.session.delete(asset_config)
            db.session.commit()
        return asset
    else:
        raise Exception("Couldn't find asset")


def get_asset_by_id(id, company_id, permission=None):
    try:
        asset = Asset.query.filter(
            Asset.id == id, Asset.company_id == company_id
        ).first()
        photos = Photo.query.filter_by(asset_id=id).all()
        attachments = Attachment.query.filter_by(asset_id=id).all()
        assetConfig = AssetConfig.query.filter_by(asset_id=id).first()
        new_commercial_detail = get_details(id)
        if assetConfig:
            all_assetConfig = {
                "id": assetConfig.id,
                "used_or_new": assetConfig.used_or_new,
                "ansi_or_new": assetConfig.ansi_or_new,
                "machine_ownership_type": assetConfig.machine_ownership_type,
                "battery_type": assetConfig.battery_type,
                "engine_serial_no": assetConfig.engine_serial_no,
                "two_or_four_wd": assetConfig.two_or_four_wd,
                "accessories": assetConfig.accessories,
                "tyres": assetConfig.tyres,
            }
        else:
            all_assetConfig = {}

        all_photos = []
        all_attachments = []
        for photo in photos:
            url_data = (
                photo.image_uri.split("/")[1] + "/" + photo.image_uri.split("/")[2]
            )
            # print(url_data)
            url = get_file(url_data)
            # print(url)
            all_photos.append(
                {
                    "id": photo.id,
                    "asset_id": photo.asset_id,
                    "image_uri": url,
                }
            )

        for attachment in attachments:
            url_data = (
                attachment.doc_uri.split("/")[1]
                + "/"
                + attachment.doc_uri.split("/")[2]
            )
            # print(url_data)
            url = get_file(url_data)
            # print(url)
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

        if asset:
            if permission == "ADMIN.ALL":
                return {
                    "id": asset.id,
                    "asset_no": asset.asset_no,
                    "make": asset.make,
                    "yom": asset.yom,
                    "model": asset.model,
                    "category": asset.category,
                    "description": asset.description,
                    "serial_no": asset.serial_no,
                    "purchased_from": asset.purchased_from,
                    "rfid": asset.rfid,
                    "device_hash": asset.device_hash,
                    "site_location": asset.site_location,
                    "created_at": asset.created_at,
                    "photo_data": all_photos,
                    "attachment_data": all_attachments,
                    "config_data": all_assetConfig,
                    "commercial_detail": new_commercial_detail,
                    "rfid": asset.rfid,
                    "device_hash": asset.device_hash,
                    "device_id": asset.device_id,
                    "platform": asset.platform,
                    "group": asset.group,
                }
            else:
                return {
                    "id": asset.id,
                    "asset_no": asset.asset_no,
                    "make": asset.make,
                    "yom": asset.yom,
                    "model": asset.model,
                    "category": asset.category,
                    "description": asset.description,
                    "serial_no": asset.serial_no,
                    "purchased_from": asset.purchased_from,
                    "rfid": asset.rfid,
                    "device_hash": asset.device_hash,
                    "site_location": asset.site_location,
                    "created_at": asset.created_at,
                    "photo_data": all_photos,
                    "attachment_data": all_attachments,
                    "config_data": all_assetConfig,
                    "rfid": asset.rfid,
                    "device_hash": asset.device_hash,
                    "device_id": asset.device_id,
                    "platform": asset.platform,
                    "group": asset.group,
                }
        else:
            raise Exception("Couldn't find asset")
    except Exception as e:
        raise e


def get_asset_data_list(company_id=None):
    try:
        assets = (
            Asset.query.filter_by(company_id=company_id)
            .with_entities(
                Asset.asset_no,
                Asset.category,
                Asset.yom,
                Asset.model,
                Asset.id,
                Asset.rfid,
                Asset.device_hash,
            )
            .all()
        )
        category_list = []
        category_counter = []
        YOM_list = []
        YOM_counter = []
        model_list = []
        model_counter = []
        asset_no_list = []
        unlinked_assets_list = []
        asset_no_counter = 0

        empty_dic_for_category = {}
        empty_dic_for_make = {}
        empty_dic_for_model = {}

        for asset in assets:
            if (
                asset.rfid == ""
                or asset.rfid == None
                and asset.device_hash == ""
                or asset.device_hash == None
            ):
                unlinked_assets_list.append(asset.asset_no)

            asset_no_counter += 1
            asset_no_list.append({"id": asset.id, "asset_no": asset.asset_no})

            if empty_dic_for_category.get(asset.category) != None:
                empty_dic_for_category[asset.category] = (
                    int(empty_dic_for_category[asset.category]) + 1
                )
            else:
                empty_dic_for_category[asset.category] = 1
            if empty_dic_for_make.get(asset.yom) != None:
                empty_dic_for_make[asset.yom] = int(empty_dic_for_make[asset.yom]) + 1
            else:
                empty_dic_for_make[asset.yom] = 1
            if empty_dic_for_model.get(asset.model) != None:
                empty_dic_for_model[asset.model] = (
                    int(empty_dic_for_model[asset.model]) + 1
                )
            else:
                empty_dic_for_model[asset.model] = 1

        for key, value in empty_dic_for_category.items():
            category_counter.append({key: value})
            category_list.append(key)

        for key, value in empty_dic_for_make.items():
            YOM_counter.append({key: value})
            YOM_list.append(key)

        for key, value in empty_dic_for_model.items():
            model_counter.append({key: value})
            model_list.append(key)

        return {
            "category": category_list,
            "YOM": YOM_list,
            "model": model_list,
            "asset_data": asset_no_list,
            "unlinked_assets": unlinked_assets_list,
            "count": {
                "category": category_counter,
                "asset_data": asset_no_counter,
                "YOM": YOM_counter,
                "model": model_counter,
            },
        }

    except Exception as e:
        print(e)
        raise e


def get_asset_nos_and_ids(company_id):
    try:
        assets = (
            Asset.query.with_entities(Asset.id, Asset.asset_no)
            .filter_by(company_id=company_id)
            .all()
        )
        assets_data = []
        for asset in assets:
            assets_data.append({"id": asset.id, "no": asset.asset_no})
        return assets_data
    except Exception:
        raise Exception("Error getting asset object")


def check_obj_available(data):
    try:
        data[0].id
        return True
    except:
        return False


def get_all_asset_json_data(company_id, permission=None):
    try:
        assets = Asset.query.filter_by(company_id=company_id).all()
        # print(assets)
        total_json_data = []
        for asset in assets:
            if check_obj_available(asset.asset_config) and check_obj_available(
                asset.commercial_details
            ):
                main_data = {
                    "id": asset.id,
                    "asset_no": asset.asset_no,
                    "make": asset.make,
                    "yom": asset.yom,
                    "model": asset.model,
                    "category": asset.category,
                    "description": asset.description,
                    "serial_no": asset.serial_no,
                    "purchased_from": asset.purchased_from,
                    "rfid": asset.rfid,
                    "device_hash": asset.device_hash,
                    "site_location": asset.site_location,
                    "created_at": asset.created_at,
                    "used_or_new": asset.asset_config[0].used_or_new,
                    "ansi_or_new": asset.asset_config[0].ansi_or_new,
                    "machine_ownership_type": asset.asset_config[
                        0
                    ].machine_ownership_type,
                    "battery_type": asset.asset_config[0].battery_type,
                    "engine_serial_no": asset.asset_config[0].engine_serial_no,
                    "two_or_four_wd": asset.asset_config[0].two_or_four_wd,
                    "accessories": asset.asset_config[0].accessories,
                    "tyres": asset.asset_config[0].tyres,
                }
                if permission == "ADMIN.ALL":
                    main_data["purchase_order_no"] = asset.commercial_details[
                        0
                    ].purchase_order_no
                    main_data["purchase_order_date"] = asset.commercial_details[
                        0
                    ].purchase_order_date
                    main_data["invoice_no"] = asset.commercial_details[0].invoice_no
                    main_data["invoice_date"] = asset.commercial_details[0].invoice_date
                    main_data["payment_terms"] = asset.commercial_details[
                        0
                    ].payment_terms
                    main_data["amount_rem_to_oem"] = asset.commercial_details[
                        0
                    ].amount_rem_to_oem
                    main_data["date_of_rem_to_oem"] = asset.commercial_details[
                        0
                    ].date_of_rem_to_oem
                    main_data["exchange_rate_rem"] = asset.commercial_details[
                        0
                    ].exchange_rate_rem
                    main_data["custom_duty_payment"] = asset.commercial_details[
                        0
                    ].custom_duty_payment
                    main_data["exworks_price"] = asset.commercial_details[
                        0
                    ].exworks_price
                    main_data["cif_charges"] = asset.commercial_details[0].cif_charges
                    main_data["total_cost"] = asset.commercial_details[0].total_cost
                    main_data["boe_no"] = asset.commercial_details[0].boe_no
                    main_data["custom_duty_value"] = asset.commercial_details[
                        0
                    ].custom_duty_value
                    main_data["gst_amount"] = asset.commercial_details[0].gst_amount
                    main_data["exrate_boe"] = asset.commercial_details[0].exrate_boe
                    main_data["clearing_charges"] = asset.commercial_details[
                        0
                    ].clearing_charges
                    main_data["cha_charges"] = asset.commercial_details[0].cha_charges
                    main_data["transportation_charges"] = asset.commercial_details[
                        0
                    ].transportation_charges
                    main_data["port_of_dispatch"] = asset.commercial_details[
                        0
                    ].port_of_dispatch
                    main_data["port_of_clearance"] = asset.commercial_details[
                        0
                    ].port_of_clearance
                    main_data["period_of_insurance"] = asset.commercial_details[
                        0
                    ].period_of_insurance
                    main_data["insurance_renewal"] = asset.commercial_details[
                        0
                    ].insurance_renewal
                    main_data["total_landed_cost"] = asset.commercial_details[
                        0
                    ].total_landed_cost
                    main_data["total_landed_cost_with_gst"] = asset.commercial_details[
                        0
                    ].total_landed_cost_with_gst
                total_json_data.append(main_data)
            elif check_obj_available(asset.asset_config):
                total_json_data.append(
                    {
                        "id": asset.id,
                        "asset_no": asset.asset_no,
                        "make": asset.make,
                        "yom": asset.yom,
                        "model": asset.model,
                        "category": asset.category,
                        "description": asset.description,
                        "serial_no": asset.serial_no,
                        "purchased_from": asset.purchased_from,
                        "rfid": asset.rfid,
                        "device_hash": asset.device_hash,
                        "site_location": asset.site_location,
                        "created_at": asset.created_at,
                        "used_or_new": asset.asset_config[0].used_or_new,
                        "ansi_or_new": asset.asset_config[0].ansi_or_new,
                        "machine_ownership_type": asset.asset_config[
                            0
                        ].machine_ownership_type,
                        "battery_type": asset.asset_config[0].battery_type,
                        "engine_serial_no": asset.asset_config[0].engine_serial_no,
                        "two_or_four_wd": asset.asset_config[0].two_or_four_wd,
                        "accessories": asset.asset_config[0].accessories,
                        "tyres": asset.asset_config[0].tyres,
                    }
                )
            elif check_obj_available(asset.commercial_details):
                total_json_data.append(
                    {
                        "id": asset.id,
                        "asset_no": asset.asset_no,
                        "make": asset.make,
                        "yom": asset.yom,
                        "model": asset.model,
                        "category": asset.category,
                        "description": asset.description,
                        "serial_no": asset.serial_no,
                        "purchased_from": asset.purchased_from,
                        "rfid": asset.rfid,
                        "device_hash": asset.device_hash,
                        "site_location": asset.site_location,
                        "created_at": asset.created_at,
                        "purchase_order_no": asset.commercial_details[
                            0
                        ].purchase_order_no,
                        "purchase_order_date": asset.commercial_details[
                            0
                        ].purchase_order_date,
                        "invoice_no": asset.commercial_details[0].invoice_no,
                        "invoice_date": asset.commercial_details[0].invoice_date,
                        "payment_terms": asset.commercial_details[0].payment_terms,
                        "amount_rem_to_oem": asset.commercial_details[
                            0
                        ].amount_rem_to_oem,
                        "date_of_rem_to_oem": asset.commercial_details[
                            0
                        ].date_of_rem_to_oem,
                        "exchange_rate_rem": asset.commercial_details[
                            0
                        ].exchange_rate_rem,
                        "custom_duty_payment": asset.commercial_details[
                            0
                        ].custom_duty_payment,
                        "exworks_price": asset.commercial_details[0].exworks_price,
                        "cif_charges": asset.commercial_details[0].cif_charges,
                        "total_cost": asset.commercial_details[0].total_cost,
                        "boe_no": asset.commercial_details[0].boe_no,
                        "custom_duty_value": asset.commercial_details[
                            0
                        ].custom_duty_value,
                        "gst_amount": asset.commercial_details[0].gst_amount,
                        "exrate_boe": asset.commercial_details[0].exrate_boe,
                        "clearing_charges": asset.commercial_details[
                            0
                        ].clearing_charges,
                        "cha_charges": asset.commercial_details[0].cha_charges,
                        "transportation_charges": asset.commercial_details[
                            0
                        ].transportation_charges,
                        "port_of_dispatch": asset.commercial_details[
                            0
                        ].port_of_dispatch,
                        "port_of_clearance": asset.commercial_details[
                            0
                        ].port_of_clearance,
                        "period_of_insurance": asset.commercial_details[
                            0
                        ].period_of_insurance,
                        "insurance_renewal": asset.commercial_details[
                            0
                        ].insurance_renewal,
                        "total_landed_cost": asset.commercial_details[
                            0
                        ].total_landed_cost,
                        "total_landed_cost_with_gst": asset.commercial_details[
                            0
                        ].total_landed_cost_with_gst,
                    }
                )
            else:
                total_json_data.append(
                    {
                        "id": asset.id,
                        "asset_no": asset.asset_no,
                        "make": asset.make,
                        "yom": asset.yom,
                        "model": asset.model,
                        "category": asset.category,
                        "description": asset.description,
                        "serial_no": asset.serial_no,
                        "purchased_from": asset.purchased_from,
                        "rfid": asset.rfid,
                        "device_hash": asset.device_hash,
                        "site_location": asset.site_location,
                        "created_at": asset.created_at,
                    }
                )

        return total_json_data

    except Exception as e:
        print(e)
        raise Exception(e)
