from apscheduler.schedulers.background import BackgroundScheduler
from models.lease import Lease
from models.asset import Asset
from models.asset_config import AssetConfig
from models.commercial_details import CommercialDetail
import datetime
from models.operator import Operator
from models.lease_operator import Lease_Operator_Mapping
from analytical_db.DB import add_analyticaldata, check_datetime_of_entry
from models.company import Company
from models.employee import Employee
from models.autosycntime import AutoSycnTime
from functions.dashboard_module import get_all_overview
from functions.utilities.odoo_funtions.main import main_odoo_function
from functions.asset_details import create_details, update_details
from functions.asset_module import create_asset, update_by_id
from functions.lease_module import update_lease_by_id, create_lease
from sqlalchemy import or_
from config import COMPANY, PRODUCTION
from functions.operator_module import create_operator, update_operator


database = []
sched = BackgroundScheduler(daemon=True)


def start_scheduler(db, app):
    database.append(db)
    database.append(app)
    try:
        if PRODUCTION != 0:  
           sched.add_job(complete_and_inactive,'interval',hours=3)
        else:
           sched.add_job(complete_and_inactive, "interval", seconds=10, max_instances=2)
        sched.start()
        print("Starting scheduler")
    except Exception as e:
        raise e


# def start_scheduler (db, app):

#         database.append(db)
#         database.append(app)
#         try:
#                 sched.add_job(complete_and_inactive,'interval',seconds=10 )
#                 sched.start()
#         except Exception as e:
#                 raise e


def complete_and_inactive():
    current_db = None or database[0]
    current_app = None or database[1]
    if current_db != None and current_app != None:
        with current_app.app_context():
            try:
                today = datetime.datetime.now()
                change_for_inactive_leases(current_db, today)
                change_lease_status_after_15_days(current_db, today)
                change_after_0_days(current_db, today)
                leave_from_lease(current_db)
                add_once_data_in_db()
                autosychronize_assets(current_db)
                autosychronize_lease(current_db)
                autosychronize_operators(current_db)
                # check_datetime_of_entry()
            except Exception as e:
                raise e


# here start the function -->


def leave_from_lease(current_db):
    try:
        today = str(datetime.datetime.now()).split(" ")[0]
        all_Operators = (
            Operator.query.with_entities(Operator.id, Operator.termination_date)
            .filter(Operator.termination_date == today)
            .all()
        )
        if len(all_Operators) >= 1:
            for operator in all_Operators:
                Lease_Operator_Mapping.query.filter(
                    Lease_Operator_Mapping.operator_id == operator.id
                ).delete()
            current_db.session.commit()
    except Exception as e:
        raise e


def change_lease_status_after_15_days(current_db, today):
    try:
        one_15days_latter_date = str(today + datetime.timedelta(days=15)).split(" ")[0]
        expiring_warning_leases = Lease.query.filter(
            Lease.rental_end_date <= one_15days_latter_date,
            Lease.rental_end_date >= str(today).split(" ")[0],
        ).all()
        if len(expiring_warning_leases) >= 1:
            for lease in expiring_warning_leases:
                date_array = lease.rental_end_date.split("-")
                due_date = today - datetime.datetime(
                    int(date_array[0]), int(date_array[1]), int(date_array[2])
                )
                set_date = str(due_date).split(",")[0]
                if set_date.find("-") != -1:
                    set_date = set_date.split("-")[1]
                    lease.lease_status = f"expiring in {set_date}"
                else:
                    lease.lease_status = "expiring in 0 day"
            current_db.session.commit()
    except Exception as e:
        raise e


def change_after_0_days(current_db, today):
    try:
        date = str(today - datetime.timedelta(days=1)).split(" ")[0]
        update_for_expired_leases = Lease.query.filter(
            Lease.rental_end_date <= date, Lease.lease_status != "inactive"
        ).all()
        if len(update_for_expired_leases) >= 1:
            for lease in update_for_expired_leases:
                lease.lease_status = "expired"
            current_db.session.commit()
    except Exception as e:
        raise e


def change_for_inactive_leases(current_db, today):
    try:
        date = str(today).split(" ")[0]
        today_inactive_leases = Lease.query.filter(
            Lease.lease_status == "inactive", Lease.rental_start_date == date
        ).all()
        if len(today_inactive_leases) >= 1:
            for lease in today_inactive_leases:
                lease.lease_status = "active"
            current_db.session.commit()
    except Exception as e:
        raise e


def add_once_data_in_db():
    company_ids = Company.query.join(Employee).all()
    for data in company_ids:
        checker = check_datetime_of_entry(data.id)
        if checker:
            overview_data = get_all_overview(data.id)
            add_analyticaldata(overview_data)


def autosychronize_assets(db):
    try:
        now_date = str(datetime.datetime.now())
        condition_date = AutoSycnTime.query.filter(
            AutoSycnTime.date <= now_date, AutoSycnTime.section == "asset"
        ).first()
        if condition_date:
            check_date = condition_date.date
        else:
            check_date = None

        updated_assets_list = main_odoo_function("get_update_asset_list", check_date)
        if len(updated_assets_list) >= 1:
            company_ids = Company.query.join(Employee).all()
            company_ids_arr = []
            company_id_asset_obj = {}
            for data in company_ids:
                company_ids_arr.append(str(data.id))
            for company_id in company_ids_arr:
                assets_objs = (
                    Asset.query.with_entities(Asset.id, Asset.asset_no)
                    .filter(Asset.company_id == company_id)
                    .all()
                )
                company_id_asset_obj[company_id] = {}
                for assets_obj in assets_objs:
                    company_id_asset_obj[company_id][assets_obj.asset_no] = str(
                        assets_obj.id
                    )
            for company_id in company_ids_arr:
                asset_no_obj = company_id_asset_obj.get(company_id)
                update_assets_by_company_id(
                    asset_no_obj, updated_assets_list, company_id
                )
            new_entry = AutoSycnTime(date=now_date, section="asset")
            db.session.add(new_entry)
            db.session.commit()
    except Exception as e:
        print(e)


def update_assets_by_company_id(asset_no_obj, updated_assets_list, company_id):
    try:
        for asset in updated_assets_list:
            if asset["asset_no"]:
                asset_no = str(asset["asset_no"]).split("-")
            if len(asset_no) >= 2:
                asset_no_condition = check_object(asset_no_obj, asset_no)
                update_or_create_asset(
                    asset_no_condition, asset, asset_no, asset_no_obj, company_id
                )
    except Exception as e:
        print("error :", e)


def check_object(obj, arr):
    """it is written for validation the aseet in the DB or Not"""
    for a in arr:
        if obj.get(a, None):
            return a
    return None


def update_or_create_asset(
    asset_no_condition, asset, asset_no, asset_no_obj, company_id
):
    try:
        if asset_no_condition:
            asset_for_update = asset
            asset_for_update["asset_no"] = asset_no[1]
            update_by_id(asset_no_obj[asset_no_condition], data=asset_for_update)
            asset["asset_id"] = asset_no_obj[asset_no_condition]
            update_details(asset)
        else:
            if COMPANY == company_id:
                """I don't think all company are using odoo
                so I make this static or futue we can product pipeline"""
                asset["asset_no"] = asset_no[1]
                data = create_asset(asset, company_id)
                asset["asset_id"] = data.id
                create_details(asset)
    except Exception as e:
        print(e)


def autosychronize_lease(db):
    """here we start auto syncing in the lease"""
    try:
        now_date = str(datetime.datetime.now())
        condition_date = AutoSycnTime.query.filter(
            AutoSycnTime.date <= now_date, AutoSycnTime.section == "lease"
        ).first()
        if condition_date:
            check_date = condition_date.date
        else:
            check_date = None
        updated_leases_list = main_odoo_function("get_lease_or_order_data", check_date)
        """now start update and create new lease start"""
        lease_id_order_id = (
            Lease.query.with_entities(Lease.id, Lease.odoo_order_id)
            .filter(Lease.company_id == COMPANY)
            .all()
        )
        asset_no_ids = (
            Asset.query.with_entities(Asset.id, Asset.asset_no)
            .filter(Asset.company_id == COMPANY)
            .all()
        )
        lease_id_obj = {}
        asset_id_obj = {}
        for le in lease_id_order_id:
            if le.odoo_order_id:
                lease_id_obj[le.odoo_order_id] = str(le.id)
        for aset in asset_no_ids:
            if aset.asset_no:
                asset_id_obj[str(aset.asset_no)] = str(aset.id)
        # print(aset.asset_no)
        update_or_create_lease(
            updated_leases_list, lease_id_obj, check_date, asset_id_obj
        )
        new_entry = AutoSycnTime(date=now_date, section="lease")
        db.session.add(new_entry)
        db.session.commit()
    except Exception as e:
        print(e, "error creating lease")


def update_or_create_lease(updated_leases_list, lease_id_obj, check_date, asset_id_obj):
    try:
        for lease in updated_leases_list:
            if lease_id_obj.get(lease.get("odoo_order_id", None), None):
                lease_id = lease_id_obj.get(lease["odoo_order_id"])
                update_lease_by_id(lease_id, lease)
            else:
                if check_date:
                    """here we need asset_no to create a new lease and run after checking date"""
                    if lease["create_date"] >= check_date:
                        asset_id = asset_id_obj.get(lease.get("asset_no", None), None)
                        if asset_id:
                            lease["asset_id"] = asset_id
                            create_lease(data=lease, company_id=COMPANY)
                            print("lease created")
                        else:
                            Exception("please update the asset_no in odoo order id")
    except Exception as e:
        raise e


def autosychronize_operators(db):
    try:
        now_date = str(datetime.datetime.now())
        condition_date = AutoSycnTime.query.filter(
            AutoSycnTime.date <= now_date, AutoSycnTime.section == "operator"
        ).first()
        if condition_date:
            check_date = condition_date.date
        else:
            check_date = None
        updated_operator_list = main_odoo_function("get_all_operator", check_date)
        operator_ids = (
            Operator.query.with_entities(Operator.id, Operator.odoo_employee_no)
            .filter(Operator.company_id == COMPANY)
            .all()
        )
        operator_obj_ids = {}
        for oper in operator_ids:
            # print(oper)
            if oper.odoo_employee_no:
                operator_obj_ids[str(oper.odoo_employee_no)] = oper.id
        update_or_operator(
            updated_operator_list=updated_operator_list,
            operator_obj_ids=operator_obj_ids,
        )
        new_entry = AutoSycnTime(date=now_date, section="operator")
        db.session.add(new_entry)
        db.session.commit()
        # print(updated_operator_list)
    except Exception as e:
        print(e, "Error updating operator")


def update_or_operator(updated_operator_list, operator_obj_ids):
    try:
        for operator in updated_operator_list:
            if operator.get("odoo_employee_no", None):
                if operator_obj_ids.get(operator.odoo_employee_no, None):
                    id = operator_obj_ids[operator.odoo_employee_no]
                    operat = {
                        "name": operator["name"],
                        "aadhar_no": operator["aadhar_no"],
                        "net_inhand_salary": operator["net_inhand_salary"],
                        "leaving_date": operator["termination_date"],
                        "pf_account_no": operator["pf_account_no"],
                        "phone": {
                            "phone_no": operator["phone_no"],
                            "phone_code": operator["phone_code"],
                        },
                        "bank_details": {
                            "ifsc_code": operator["ifsc_code"],
                            "account_no": operator["account_no"],
                        },
                    }
                    update_operator(id=id, data=operat)
            else: 
                '''here I write create operator code'''

    except Exception as e:
        print(e)


'''here I write auto sync for operator'''
# def all_time_sheet_sync(db):
#     try:
#         now_date = str(datetime.datetime.now())
#         condition_date = AutoSycnTime.query.filter(
#             AutoSycnTime.date <= now_date, AutoSycnTime.section == "timesheet" 
#         ).first()
#         if condition_date:
#             check_date = condition_date.date
#         else:
#             check_date = None
#         updated_time_shee_list = main_odoo_function("entry_excel_data", check_date)

#         new_entry = AutoSycnTime(date=now_date, section="timesheet")
#         db.session.add(new_entry)
#         db.session.commit()
#     except Exception as e:
#         print(e)


# def update_or_create_time_sheet():
#     try:

#     except Exception as e:
