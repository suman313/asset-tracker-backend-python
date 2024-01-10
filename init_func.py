from functions.utilities.odoo_funtions.upadate_after_sync import Updated_ids


updated_odoo_init =  Updated_ids()

def initialize_functions():
    try:
        updated_odoo_init.set_asset_no_ids_store()
        updated_odoo_init.set_operators_name_ids()
        updated_odoo_init.set_rentals_name_ids()
        return "all services running ...."
    except Exception as e:
        print(e)
        raise e
    
