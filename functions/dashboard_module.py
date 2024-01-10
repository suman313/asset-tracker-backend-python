from models.asset import Asset
from models.maintenance import Maintenance
from models.lease import Lease
from models.lease_operator import Lease_Operator_Mapping
from models.operator import Operator
import datetime 
from sqlalchemy import or_
from functions.asset_module import get_asset_list


def get_all_overview(company_id):
    try:
        today = str(datetime.datetime.now()).split(" ")[0]
        list_object = {}
        number_assets =  Asset.query.filter(Asset.company_id == company_id).count()
        number_active_assets_in_lease = Asset.query.filter(Asset.company_id == company_id).join(Lease).filter(or_(Lease.lease_status != "expired", Lease.lease_status != "inactive")).count()
        number_asset_in_maintenance = Asset.query.filter(Asset.company_id == company_id).join(Maintenance).filter( or_(Maintenance.status == "breakdown", Maintenance.status == "in_progress", Maintenance.status == "scheduled")).count()
        number_asset_breack_down_in_maintenance = Asset.query.filter(Asset.company_id == company_id).join(Maintenance).filter(Maintenance.status == "breakdown").count()
        number_of_operator = Operator.query.filter(Operator.company_id == company_id).count()
        active_operators = Lease_Operator_Mapping.query.filter(Lease_Operator_Mapping.company_id == company_id).join(Operator).filter(or_(Operator.termination_date < today, Operator.termination_date == "" , Operator.termination_date == None )).all()
        for operator in active_operators:
            number = list_object.get(operator.operator_id)
            if number:
                list_object[operator.operator_id] = number + 1
            else :
                list_object[operator.operator_id] = 1 
            
        number_of_active_operators = len(list_object)
        print(number_active_assets_in_lease, number_asset_in_maintenance, number_assets, number_of_operator, number_of_active_operators)
        return {
            "total_assets" : number_assets,
            "total_assets_active_in_lease" : number_active_assets_in_lease,
            "total_assets_in_maintenance" : number_asset_in_maintenance,
            "total_number_operator" : number_of_operator,
            "total_number_active_operator" : number_of_active_operators,
            "number_asset_breack_down_in_maintenance": number_asset_breack_down_in_maintenance,
            "company_id" : str(company_id)
        }
    except Exception as e:
        raise e
    

def get_all_data_by_category(category=None, company_id=None):
    try:
        obj = {}
        if not(company_id):
            raise Exception("bad argument to get data")
        all_assets = Asset.query.filter(Asset.company_id == company_id)
        main_arr = []
        lease_arr = []
        
        in_maintenance = all_assets.filter(Asset.category == category).join(Maintenance).all()
        in_lease = all_assets.filter(Asset.category == category).join(Lease).all()
        for main in in_maintenance:
                main_arr.append({
                        "id": str(main.id),
                        "model": main.model,
                        "yom": main.yom,
                        "asset_no": main.asset_no,
                        "serial_no": main.serial_no,
                        "category": main.category,
                        "maintenance": main.maintenance[0].status,
                        "make": main.make,
                        "created_at": main.created_at,
                })
                    
        for lease in in_lease:
                lease_arr.append({
                        "id": str(lease.id),
                        "model": lease.model,
                        "yom": lease.yom,
                        "asset_no": lease.asset_no,
                        "lease_status": lease.lease[0].lease_status,
                        "serial_no": lease.serial_no,
                        "category": lease.category,
                        "make": lease.make,
                        "created_at": lease.created_at,
                })
            
        unlink_asset =  get_asset_list(company_id, category=category, unassigned_asset=True)
        obj["lease"] = lease_arr
        obj["maintenance"] = main_arr
        obj["unlink_asset"] = unlink_asset
        return obj
    except Exception as e:
        print(e)
        raise e


def get_all_data_by_all_category(company_id=None):
    try:
        if company_id:
            data_arr = []
            category_obj = {}
            category_arr = []
            all_category = Asset.query.with_entities(Asset.id, Asset.category).filter(Asset.company_id == company_id).all()
            for c in all_category:
                if category_obj.get(c.category, None) is None:
                    category_obj[c.category] = c.category
                    category_arr.append(c.category)
            for category in category_arr:
                data = get_all_data_by_category(category, company_id)
                data_arr.append({category: data})
            return data_arr
        else:
            Exception("somthing wrong with sesasion id")
    except Exception as e:
         raise e