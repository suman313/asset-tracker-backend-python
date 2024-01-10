from config import db, COMPANY
from models.time_sheet import TimeSheet

def bulk_create(data_arr):
    try:
        save_data_arr = []
        for data in data_arr:
            data["company_id"] = COMPANY
            print(data)
            new_time_sheet = TimeSheet(
                company_id = COMPANY,
                x_studio_asset_number = data["x_name"],
                x_studio_day_type = data["x_studio_day_type"],
                x_studio_time_in = data["x_studio_time_in"],
                x_studio_time_out = data["x_studio_time_out"],
                x_studio_rental_register_no = data["x_studio_rental_register_no"],
                x_studio_breakdown_time = data["x_studio_breakdown_time"],
                x_studio_overtime = data["x_studio_overtime"],
                x_studio_date = data["x_studio_date"],
                x_studio_reimbursements = data["x_studio_reimbursements"],
                x_studio_operator1 = data["x_studio_operator1"],
                x_studio_operator1_name = data["x_studio_operator1_name"],
                odoo_id = data["odoo_id"],
            )
            save_data_arr.append(new_time_sheet)
        print(save_data_arr)
        db.session.bulk_save_objects(save_data_arr)
        db.session.commit()
    except Exception as e:
        print(e)
        raise e
    

def bulk_delete(odoo_arr_id):
        try:
            for odoo_id in odoo_arr_id:
                sheets = TimeSheet.query.filter(TimeSheet.odoo_id == odoo_id).all()
                db.session.delete(sheets)
        except Exception as e:
            raise e