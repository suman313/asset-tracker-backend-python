import xmlrpc.client
from functions.utilities.odoo_funtions.view_list import *
from functions.utilities.odoo_funtions.timeline_entry import AllTimeEntryFuction

def main_odoo_function(func_type, check_date=None):
    try: 
        url = "https://maco.odoo.com/"
        db = "dhaval-dhh-psin-macocorp-main-1872566"
        username = 'info@macocorporation.com'
        password = 'b595853eada9c9c361e23a8eec0fc53bd0619c95'
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        models.execute_kw(db, uid, password, 'res.partner', 'check_access_rights', ['read'], {'raise_exception': False})
        if func_type == "get_part_list":
            data = get_part_list(db=db, models=models, password=password, uid=uid)
            return data
        elif func_type == "get_update_asset_list":
            data = get_update_asset_list(db=db, models=models, password=password, uid=uid, check_day=check_date)
            return data
        elif func_type == "get_lease_or_order_data":
            data = get_lease_or_order_data(db=db, models=models, password=password, uid=uid, check_day=check_date)
            return data
        elif func_type == "get_all_operator":
            data = get_all_operator(db=db, models=models, password=password, uid=uid, check_day=check_date)
            return data
        elif func_type == "entry_excel_data":
            timesheet = AllTimeEntryFuction(db=db, models=models, password=password, uid=uid, check_day=check_date)
            return timesheet
    except Exception as e:
        raise e 
    
