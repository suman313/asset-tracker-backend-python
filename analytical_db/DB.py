from pymongo import MongoClient
from uuid import UUID
import time
import datetime
from config import MONGO_URL, MONGODB_NAME, MONGO_COLLECTION
analytical_db = MongoClient(MONGO_URL)
db = analytical_db[MONGODB_NAME]
analysis_datas = db[MONGO_COLLECTION]
tele_data= db["telemetic"]
db_colection = db["test"]

def db_initializtion():
    try:
        analytical_db.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        obj = {
            "name": "testJsons",
            "mgs" : "test messages",
            "timestamp": time.time()
        }
    except Exception as e:
        print(e)

def add_analyticaldata(data):
    try:
        data["timestamp"] = time.time()
        data["date"] = str(datetime.datetime.now()).split(" ")[0]
        analysis_datas.insert_one(data)
    except Exception as e:
        print(e)

def check_datetime_of_entry(company_id):
    try:
        data_list = analysis_datas.find({"company_id":str(company_id)}).sort([("timestamp",-1)]).limit(1)
        for entry in data_list:
            date = str(datetime.datetime.fromtimestamp(entry.get("timestamp"))).split(" ")[0].split("-")
            today_date = str(datetime.datetime.now()).split(" ")[0].split("-")
            how_days_ago = (today_date[0] == date[0] and today_date[1] == date[1] and today_date[2] == date[2] )
            if how_days_ago:
                return False
        return True
    except Exception as e:
        print(e)
        return False

def add_asset_tel_data(data):
    try:
        # print(data)
        device_id = str(data["device_id"])
        tel_data = str(data["tel_data"])
        type_data = data["type_data"]
        time_now = datetime.datetime.now()
        tele_data.insert_one({"device_id": device_id, "tel_data" : tel_data, "time_now": time_now, "type_data": type_data})
    except Exception as e:
        print(e)


def find_by_device_id(device_id):
    data_obj = {}
    try: 
        device_internal_battery = tele_data.find( {"$and": [ {"type_data":"device-internal-battery", "device_id": str(device_id)}]}).sort([("time_now",-1)]).limit(1)
        vehicle_battery_voltage =tele_data.find({"$and":[{"type_data":"vehicle-battery-voltage", "device_id": str(device_id)}]}).sort([("time_now",-1)]).limit(1)
        gps_push = tele_data.find({"$and":[{"type_data": "gps-push", "device_id": str(device_id)}]}).sort([("time_now",-1)]).limit(1)
        remote_start_stop = tele_data.find({"$and":[{"device_id": device_id, "type_data":"remote-start-stop"}]}).sort([("time_now",-1)]).limit(1)
        rfid_push = tele_data.find({"$and":[{"type_data":"rfid-push", "device_id": str(device_id)}]}).sort([("time_now",-1)]).limit(1)
        # print(device_internal_battery[0], vehicle_battery_voltage[0], gps_push[0],rfid_push[0] )
        for d in device_internal_battery:
            # print(d["time_now"])
            data_obj["device_internal_battery"] = d["tel_data"]
        for v in vehicle_battery_voltage:
            data_obj["vehicle_battery_voltage"] = v["tel_data"]
        for g in gps_push: 
            data_obj["gps_push"] = g["tel_data"]
        for r in rfid_push:
            data_obj["rfid_push"] = r["tel_data"]
        for re in remote_start_stop: 
            data_obj["remote_start_stop"] = re["tel_data"]
        return data_obj
    except Exception as e:
        print(e)
        raise e