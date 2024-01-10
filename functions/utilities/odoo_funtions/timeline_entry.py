from init_func import updated_odoo_init
import datetime
import json
from functions.entry_time_line import bulk_create, bulk_delete


class AllTimeEntryFuction:
    def __init__(
        self,
        db,
        models,
        password,
        uid,
        check_day=None,
    ):
        self.db = db
        self.models = models
        self.password = password
        self.uid = uid
        self.check_day = check_day
        today = datetime.datetime.now()
        self.today = today
        self.input_data_arr = None
        self.rent_odoo_id = None
        ideal_arr = [
            "id",
            "x_studio_day_type",  #
            "x_studio_customer",  #
            "x_studio_asset_number",  #
            "x_studio_time_adjust",  #
            "x_studio_serial_no",  #
            "x_studio_rental_register_no",  #
            "x_studio_total_time",  #
            "x_studio_nominal_hours",  #
            "x_studio_time_in",  #
            "x_studio_time_out",  #
            "x_studio_breakdown_time",  #
            "x_studio_normal_billing_time",  #
            "x_studio_overtime",  #
            "x_studio_date",  #
            "x_studio_model",  #
            "x_studio_remarks",  #
            "x_studio_normal_bill_amount",  #
            "x_studio_overtime_amount",  #
            "x_studio_reimbursements",  #
            "x_studio_operator",  #
            "x_studio_operator1",  #
        ]
        self.ideal_arr = ideal_arr
        self.updated_odoo_init = updated_odoo_init
    def get_all_data_autosycn(self):
        try:
            models = self.models
            db = self.db
            uid = self.uid
            password = self.password
            check_day = self.check_day
            today = self.today
            arr = self.ideal_arr

            if models and db and uid and password:
                project_model_name = "x_rtsheet"
                if check_day:
                    search_domain = [
                        ("id", ">", 0),
                        ("write_date", "<=", today),
                        ("write_date", ">=", check_day),
                    ]
                else:
                    search_domain = [("id", ">", 0)]
                project_ids = models.execute_kw(
                    db, uid, password, project_model_name, "search", [search_domain]
                )

                timesheet_list = models.execute_kw(
                    db,
                    uid,
                    password,
                    project_model_name,
                    "read",
                    [project_ids],
                    {"fields": arr},
                )
                data_arr = []
                for time in timesheet_list:
                    odoo_id = time["id"]
                    del time["id"]
                    time["odoo_id"] = odoo_id
                    data_arr.append(json.dumps(time))
                return data_arr
            else:
                Exception("Invalid input")
        except Exception as e:
            print(e)

    def vaildate_data(self,data):
        try:
            excel_data = []
            data["Date"] = data['Date'].astype(str)
            for d in data:
                excel_data.append(str(d))
            if (
                ("Day Type" in excel_data) and
                ("Time In" in excel_data) and
                ("Time Out" in excel_data) and
                ("Rental Register No" in excel_data) and
                ("Breakdown Time" in excel_data) and
                ("Overtime" in excel_data) and
                ("Date" in excel_data) and
                ("Operator Main" in excel_data) and
                ("Operator" in excel_data) and
                ("Reimbursements" in excel_data) and
                ("Asset No" in excel_data)
                ):
                data = data.rename(columns={
                    "Day Type": "x_studio_day_type",
                    "Time In": "x_studio_time_in",
                    "Time Out": "x_studio_time_out",
                    "Rental Register No": "x_studio_rental_register_no",
                    "Breakdown Time": "x_studio_breakdown_time",
                    "Overtime": "x_studio_overtime",
                    "Date" : "x_studio_date",
                    "Operator Main": "x_studio_operator1",
                    "Operator": "x_studio_operator",
                    "Reimbursements": "x_studio_reimbursements",
                    "Asset No" : "x_name",
                 })
                json_data = data.to_json(orient='records')
                self.input_data_arr = json.loads(json_data)
                return True
        except Exception as e:
            print("Error")
            raise e

    def __get_excel_data_by_asset_odoo_id_retrun_date(self, rent_odoo_id):
        try:
            models = self.models
            db = self.db
            uid = self.uid
            password = self.password
            check_day = self.check_day
            today = self.today

            if models and db and uid and password and rent_odoo_id:
                project_model_name = "x_rtsheet"
                if check_day:
                    search_domain = [
                        ("id", ">", 0),
                        ("write_date", "<=", today),
                        ("write_date", ">=", check_day),
                        ("x_studio_rental_register_no", "=", rent_odoo_id),
                    ]
                else:
                    search_domain = [
                        ("id", ">", 0),
                        ("x_studio_rental_register_no", "=", rent_odoo_id),
                    ]
                project_ids = models.execute_kw(
                    db, uid, password, project_model_name, "search", [search_domain]
                )
                arr = ["id", "x_studio_date"]
                timesheet_list = models.execute_kw(
                    db,
                    uid,
                    password,
                    project_model_name,
                    "read",
                    [project_ids],
                    {"fields": arr},
                )
                data_obj = {}
                for time in timesheet_list:
                    if time.get("x_studio_date", None):
                        data_obj[time["x_studio_date"]] = time["id"]
                return data_obj
            else:
                Exception("Invalid Information")
        except Exception as e:
            print(e)

    def __get_data_by_odoo_id(self, data_arr):
        models = self.models
        db = self.db
        uid = self.uid
        password = self.password
        project_model_name = "x_rtsheet"
        arr = self.ideal_arr

        try:
            if models and db and uid and password:
                timesheet_list = models.execute_kw(
                    db,
                    uid,
                    password,
                    project_model_name,
                    "read",
                    [data_arr],
                    {"fields": arr},
                )
                data_arr = []
                for time in timesheet_list:
                    odoo_id = time["id"]
                    del time["id"]
                    time["odoo_id"] = odoo_id
                    data_arr.append(time)
                return data_arr
        except Exception as e:
            print(e, "Exception")

    def entry_excel_data(self, conflict_type=None):
        models = self.models
        db = self.db
        uid = self.uid
        password = self.password
        project_model_name = "x_rtsheet"
        input_data_arr = self.input_data_arr
        updated_odoo_init =  self.updated_odoo_init
        try:
            if input_data_arr:
                rent_odoo_id = input_data_arr[0]["x_studio_rental_register_no"]
                self.rent_odoo_id = rent_odoo_id
            else:
                raise Exception("Please initialize vaildate_data class")
        except Exception as e:
            raise e
        # print(rent_odoo_id)
        try:
            if models and db and uid and password and rent_odoo_id:
                date_obj = self.__get_excel_data_by_asset_odoo_id_retrun_date(rent_odoo_id)
                conflict_id_list = []
                # replace_data = []
                if not (conflict_type):
                    for data in input_data_arr:
                        if date_obj.get(data.get("x_studio_date", None), None):
                            conflict_id_list.append(date_obj.get(data["x_studio_date"]))

                def hit_on_odoo(in_arr):
                    try:
                        rent_no_arr = []
                        operator_name_arr = []
                        assets_obj = updated_odoo_init.assets_objs
                        rentals_obj = updated_odoo_init.rentals_obj
                        operator_obj = updated_odoo_init.operators_obj
                        for data in in_arr:
                            asset_no = data["x_name"]
                            operator_name = data["x_studio_operator1"]
                            rental_name = data["x_studio_rental_register_no"]
                            if not(assets_obj.get(asset_no, None)):
                               raise Exception("No asset with name please sheets")
                            if not(operator_obj.get(operator_name, None)):
                               raise Exception("No operator with name please sheets")
                            if not(rentals_obj.get(rental_name, None)):
                               raise Exception("No rental no with name please sheets")
                            rent_no_arr.append(data["x_studio_rental_register_no"])
                            operator_name_arr.append(data["x_studio_operator1"])
                            data["x_name"] = int(assets_obj.get(asset_no))
                            data["x_studio_operator1"] = int(operator_obj.get(operator_name))
                            data["x_studio_rental_register_no"] = int(rentals_obj.get(rental_name))
                            if not(data["x_studio_operator"]):
                               del data["x_studio_operator"]
                        id_create = models.execute_kw(
                            db, uid, password, project_model_name, "create", [in_arr]
                        )
                        # print(in_arr, id_create)
                        for i in range(len(id_create)):
                            in_arr[i]["odoo_id"] = id_create[i]
                            in_arr[i]["x_studio_rental_register_no"] = rent_no_arr[i]
                            in_arr[i]["x_studio_operator1_name"] = operator_name_arr[i]
                        # print(in_arr)
                        bulk_create(in_arr)
                        return in_arr
                    except Exception as e:
                        # print(e)
                        raise e
                
                def replace_and_hit(conflict_id_list, in_arr):
                    try:
                        id_delete = models.execute_kw(
                            db, uid, password, project_model_name, "unlink", [conflict_id_list]
                        )
                        print(id_delete)
                        bulk_delete(conflict_id_list)
                        data = hit_on_odoo(in_arr)
                        return data
                    except Exception as e:
                        print(e, "replace_and_hit")
                        
                if len(conflict_id_list) >= 1 and conflict_type == None:
                    '''retrun list of conflict data'''
                    print(conflict_id_list)
                    return {
                        "type": "conflict",
                        "data": self.__get_data_by_odoo_id(conflict_id_list),
                    }
                elif conflict_type == "replace":
                    '''update by replacement'''
                    print("working on it....")
                    on_data = replace_and_hit(conflict_id_list=conflict_id_list ,in_arr=input_data_arr)
                    return {"type": "replace", "data": on_data}
                elif conflict_type == "keep":
                    '''keep both'''
                    on_data = hit_on_odoo(in_arr=input_data_arr)
                    print(on_data, "keep both")
                    return {"type": "keep", "data": on_data}
                elif len(conflict_id_list) == 0:
                    '''run without conflict'''
                    # print(" I am here already", input_data_arr)
                    on_data = hit_on_odoo(in_arr=input_data_arr)
                    return {
                        "type": "success",
                        "data": on_data,
                    }
            else:
                raise Exception("Initilization failed")
        except Exception as e:
            print(e)
            raise e


    def get_table_by_r_s_o_id(self, rent_odoo_id):
        # print(rent_odoo_id)
        try:
            models = self.models
            db = self.db
            uid = self.uid
            password = self.password
            project_model_name = "x_rtsheet"
            ideal_arr = self.ideal_arr
            if models and db and uid and password and rent_odoo_id:
                search_domain = [
                        ("id", ">", 0),
                        ("x_studio_rental_register_no", "=", rent_odoo_id),
                    ]
                project_ids = models.execute_kw(
                    db, uid, password, project_model_name, "search", [search_domain]
                )
                timesheet_list = models.execute_kw(
                    db,
                    uid,
                    password,
                    project_model_name,
                    "read",
                    [project_ids],
                    {"fields": ideal_arr},
                )
                return timesheet_list
        except Exception as e:
                print(e)
                raise e