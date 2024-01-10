import xmlrpc.client

odoo_url = "https://maco.odoo.com/"
odoo_db = "dhaval-dhh-psin-macocorp-main-1872566"
odoo_username = 'info@macocorporation.com'
odoo_password = 'b595853eada9c9c361e23a8eec0fc53bd0619c95'

class Updated_ids:
    def __init__(self):
        username= odoo_username
        db = odoo_db
        password= odoo_password
        url = odoo_url
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        self.db = db
        self.models = models
        self.password = password
        self.uid = uid
        self.assets_objs = None


    def set_asset_no_ids_store(self):
        try:
            db = self.db
            uid = self.uid
            models = self.models
            password = self.password
            project_model_name = "x_rmaster"
            project_ids = models.execute_kw(
                    db, uid, password, project_model_name, "search", [[("id", ">", 0)]]
            )
            arr = ["id", "x_name"]
            assets = models.execute_kw(
                    db,
                    uid,
                    password,
                    project_model_name,
                    "read",
                    [project_ids],
                    {"fields": arr},
            )
            assets_obj = {}
            for asset in assets:
                assets_obj[asset["x_name"]] = asset["id"]

            self.assets_objs = assets_obj
        except Exception as e:
            raise e
    def set_operators_name_ids(self):
        try:
            db = self.db
            uid = self.uid
            models = self.models
            password = self.password
            project_model_name = "x_drmaster"
            project_ids = models.execute_kw(
                    db, uid, password, project_model_name, "search", [[("id", ">", 0)]]
            )
            arr = ["id", "x_name"]
            operators = models.execute_kw(
                    db,
                    uid,
                    password,
                    project_model_name,
                    "read",
                    [project_ids],
                    {"fields": arr},
            )
            operators_obj = {}
            for operator in operators:
                operators_obj[operator["x_name"]] = operator["id"]
            
            self.operators_obj = operators_obj

        except Exception as e:
            raise e
        
    def set_rentals_name_ids(self):
        try:
            db = self.db
            uid = self.uid
            models = self.models
            password = self.password
            project_model_name = "x_rservicereg"
            project_ids = models.execute_kw(
                    db, uid, password, project_model_name, "search", [[("id", ">", 0)]]
            )
            arr = ["id", "x_name"]
            rentals = models.execute_kw(
                    db,
                    uid,
                    password,
                    project_model_name,
                    "read",
                    [project_ids],
                    {"fields": arr},
            )
            rentals_obj = {}
            for rental in rentals:
                rentals_obj[rental["x_name"]] = rental["id"]

            self.rentals_obj = rentals_obj

        except Exception as e:
            raise e
     