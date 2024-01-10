import datetime


def get_part_list(models, db, uid, password):
    try:
        if models and db and uid and password:
            project_model_name = "product.template"
            search_domain = [("id", ">", 0)]
            project_ids = models.execute_kw(
                db, uid, password, project_model_name, "search", [search_domain]
            )
            projects = models.execute_kw(
                db,
                uid,
                password,
                project_model_name,
                "read",
                [project_ids],
                {"fields": ["name"]},
            )
            arr = []
            for project in projects:
                arr.append(
                    {
                        "id": project["id"],
                        "value": project["name"],
                        "label": project["name"],
                    }
                )
            return arr
        else:
            raise Exception("fuction call not completed poperly")
    except Exception as e:
        raise e


def get_update_asset_list(models, db, uid, password, check_day):
    try:
        if models and db and uid and password:
            today = datetime.datetime.now()
            project_model_name = "x_rmaster"
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
            arr = [
                "x_name",
                "x_studio_make",
                "x_studio_model",
                "activity_state",
                "x_studio_serial",
                "x_studio_purchase_ref",
                "x_studio_mac_location",
                "x_studio_yom",
                "create_date",
                "x_studio_condition",
                "x_studio_power_source",
                "x_studio_customised_accessories",
                "x_studio_purchase_ref",
                "x_studio_remittance",
                "x_studio_remit_date",
                "x_studio_exrate",
                "x_studio_clearance_port",
                "x_studio_insurance_expiry_date",
                "x_studio_landed_cost",
            ]
            assets = models.execute_kw(
                db,
                uid,
                password,
                project_model_name,
                "read",
                [project_ids],
                {"fields": arr},
            )
            data_list = []
            for asset in assets:
                data_list.append(
                    {
                        "asset_no": asset["x_name"],
                        "make": asset["x_studio_make"],
                        "model": asset["x_studio_model"],
                        "description": asset["activity_state"],
                        "serial_no": asset["x_studio_serial"],
                        "purchased_from": asset["x_studio_purchase_ref"],
                        "site_location": asset["x_studio_mac_location"],
                        "yom": asset["x_studio_yom"],
                        "created_at": asset["create_date"],
                        "used_or_new": asset["x_studio_condition"],
                        "battery_type": asset["x_studio_power_source"],
                        "accessories": asset["x_studio_customised_accessories"],
                        "purchase_order_no": asset["x_studio_purchase_ref"],
                        "amount_rem_to_oem": asset["x_studio_remittance"],
                        "date_of_rem_to_oem": asset["x_studio_remit_date"],
                        "exchange_rate_rem": asset["x_studio_exrate"],
                        "port_of_clearance": asset["x_studio_clearance_port"],
                        "insurance_renewal": asset["x_studio_insurance_expiry_date"],
                        "total_landed_cost": asset["x_studio_landed_cost"],
                    }
                )
            return data_list
        else:
            raise Exception("fuction call not completed poperly")
    except Exception as e:
        raise e


def get_lease_or_order_data(models, db, uid, password, check_day):
    try:
        if models and db and uid and password:
            today = datetime.datetime.now()
            project_model_name = "x_rservicereg"
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
            arr = [
                "id",
                "display_name",
                "create_date",
                # "write_date",
                "x_name",
                "x_studio_rental_start_date",  # Rental Start Date
                "x_studio_model_no",
                "x_studio_rental_end_date",  # Rental End Date
                "x_studio_working_days",
                "x_studio_customer",  # Customer
                "x_studio_asset_no",
                "x_currency_id",  # Cuerrency
                "x_studio_transportation",  # Transportation Charges
                "x_studio_serial",
                "x_studio_monthly_rental",
                "x_studio_rent_hour",
                "x_studio_contract_value",  # contract value
                "x_studio_nominal_hours",
                "x_studio_service_location",
                "x_studio_internal_ref_1",
                "x_studio_normal_amount",  # Normal Amount
                "x_studio_overtime_amount",  # Overtime Amount
                "x_studio_internal_ref",
                "x_studio_total_claimable",  # Total Claimable Amount
                "x_studio_company",
                "x_studio_reimbursements",  # Reimbursements
                "x_studio_remarks",  # Customer PO No
            ]
            leases = models.execute_kw(
                db,
                uid,
                password,
                project_model_name,
                "read",
                [project_ids],
                {"fields": arr},
            )
            data_list = []
            for lease in leases:
                x_studio_asset_no = ""
                x_currency_id = ""
                x_studio_customer =""
                if lease["x_studio_asset_no"]: 
                    x_studio_asset_no = str(lease["x_studio_asset_no"][1]).split("-")[1]
                if lease["x_currency_id"]:
                    x_currency_id = lease["x_currency_id"][1]
                if lease["x_studio_customer"]:
                   x_studio_customer = lease["x_studio_customer"][1]
                data_list.append({
                    "lease_type": "null",
                    "customer_po_no": lease["x_studio_remarks"] or "null",
                    "currency":  x_currency_id,
                    "rental_start_date": lease["x_studio_rental_start_date"] or "",
                    "rental_end_date": lease["x_studio_rental_end_date"] or "",
                    "customer":  x_studio_customer,
                    "sale_person": "null",
                    "lease_status": "",
                    "fild_id": "",
                    "asset_no":  x_studio_asset_no,
                    "contract_value": lease["x_studio_contract_value"] or "",
                    "transportation_charge": lease["x_studio_transportation"] or "",
                    "normal_amount": lease["x_studio_normal_amount"] or "",
                    "overtime_amount": lease["x_studio_overtime_amount"] or "",
                    "reimbursements": lease["x_studio_reimbursements"] or "",
                    "total_claimable_amount": lease["x_studio_total_claimable"] or "",
                    "asset_id": "",
                    "odoo_order_id": lease["x_name"] or "",
                    "odoo_mask_order_id": lease["id"],
                    "create_date": lease["create_date"] or "",
                })
            return data_list
    except Exception as e:
        print(e)

def get_all_operator(models, db, uid, password, check_day):
    try:
        if models and db and uid and password:
            today = datetime.datetime.now()
            project_model_name = "x_drmaster"
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
            # print(project_ids)
            arr = [
                   "id",
                   "x_name",
                   "x_studio_aadhar_number",
                   "x_studio_account_number",
                   "x_studio_contact_number",
                   "x_studio_employee_number",
                   "x_studio_ifsc_code",
                   "x_studio_gross_monthly",
                   "x_studio_uan_no"
                  ]
            operators = models.execute_kw(
                db,
                uid,
                password,
                project_model_name,
                "read",
                [project_ids],
                {"fields": arr},
            )
            all_operator_list = []
            # print(operators)
            for operator in operators:
                all_operator_list.append({
                    "odoo_operator_mask_id": operator["id"],
                    "odoo_operator_id": operator["x_studio_employee_number"] or "",
                    "name": operator["x_name"] or "",
                    "aadhar_no": operator["x_studio_uan_no"] or "",
                    "pf_account_no": "",
                    "ifsc_code": operator["x_studio_ifsc_code"] or "",
                    "net_inhand_salary":operator["x_studio_gross_monthly"] or "",
                    "account_no": operator["x_studio_account_number"] or "",
                    "phone_code": "+91",
                    "phone_no": operator["x_studio_contact_number"] or "",
                })
            return all_operator_list
    except Exception as e:
           print(e)
