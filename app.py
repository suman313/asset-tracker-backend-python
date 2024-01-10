from multiprocessing.util import debug
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from flask_migrate import Migrate
from config import db, SECRET_KEY, PRODUCTION
from os import environ, path, getcwd
from dotenv import load_dotenv
from models.super_admin import SuperAdmin
from models.company import Company
from models.employee import Employee
from models.permission import Permission
from models.asset import Asset
from models.asset_config import AssetConfig
from models.attachment import Attachment
from models.commercial_details import CommercialDetail
from models.bank_details import BankDetails
from models.lease import Lease
from models.maintenance import Maintenance
from models.operator import Operator
from models.parts import Parts
from models.time_sheet import TimeSheet
from models.permission import Permission
from models.phone import Phone
from models.photo import Photo
from models.autosycntime import AutoSycnTime
from routes.superadmin import superadmin_bp
from routes.company import company_bp
from routes.asset import asset_bp
from routes.lease import lease_bp
from routes.maintenance import maintenance_bp
from routes.operator import operator_bp
from routes.dashboard import dashboard_bp
from functions.utilities.mailSender import mailer
from functions.utilities.schedulers import start_scheduler
from analytical_db.DB import db_initializtion
from functions.mqtts.conection import initialize_mqtt_client
from functions.mqtts.socket import initialize_client_socket
import threading
from init_func import initialize_functions


load_dotenv(path.join(getcwd(), '.env'))



def create_app():
    global db 
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DB_URI') 
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_MAX_OVERFLOW"] = 1000
    app.config["SQLALCHEMY_POOL_SIZE"] = 100
    app.config['MAIL_SERVER'] = 'smtp.hostinger.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'admin@quinch.co.in'
    app.config['MAIL_PASSWORD'] = 'Quinch@2023'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.secret_key = SECRET_KEY
    db.init_app(app)
    mailer.init_app(app)
    migrate = Migrate(app, db)
    print("DB Initialized Successfully")

    CORS(app, cors_allowed_origins="*")
    
    with app.app_context():
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(superadmin_bp)
        app.register_blueprint(company_bp)
        app.register_blueprint(asset_bp,  url_prefix='/asset')
        app.register_blueprint(lease_bp,  url_prefix='/lease')
        app.register_blueprint(maintenance_bp,  url_prefix='/maintenance')
        app.register_blueprint(operator_bp,  url_prefix='/operator')

        # db.drop_all()
        migrate.init_app(app, db)
        db.create_all()
        db.session.commit()
        db_initializtion()
        start_scheduler(db, app)
        initialize_functions()
        return app


if __name__ == "__main__":
    app = create_app()
    print(app.url_map)
    background_thread1 = threading.Thread(target=initialize_mqtt_client)
    background_thread2 = threading.Thread(target=initialize_client_socket)
    background_thread1.start()
    background_thread2.start()
    if PRODUCTION:
        app.run(host="0.0.0.0", port="5000", debug=False)
    else: 
        app.run(host="0.0.0.0", port="5000", debug=True)
