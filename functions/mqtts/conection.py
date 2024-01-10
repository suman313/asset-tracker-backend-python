import paho.mqtt.client as mqtt
from functions.mqtts.socket import emit_message, get_mqtt_array
import requests
from analytical_db.DB import add_asset_tel_data

mqtt_arr = []

def initialize_mqtt_client():
    try:
        # MQTT Settings
        mqtt_broker = "mqtt-tests.durbin.live"
        mqtt_port = 8883  # or the appropriate port for your MQTT broker
        mqtt_topic = "#"
        mqtt_ca_cert = "./ca.crt"
        mqtt_username = "durbin"
        mqtt_password = "X.8mCK*kHV76-cw"

        # MQTT Client Setup
        mqtt_client = mqtt.Client()

        # Set TLS options
        mqtt_client.tls_set(mqtt_ca_cert)
        mqtt_client.username_pw_set(mqtt_username, mqtt_password)

        def get_location(ip_address):
            try:
                # Make a request to the ipinfo.io API
                response = requests.get(f"https://ipinfo.io/{ip_address}/json")
                
                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    # Parse the JSON response
                    data = response.json()
                    print(data)
                    # Print the location information
                    print(f"IP Address: {data['ip']}")
                    print(f"Location: {data['city']}, {data['region']}, {data['country']}")
                    print(f"Coordinates: {data['loc']}")
                else:
                    print(f"Failed to retrieve location. Status Code: {response.status_code}")

            except Exception as e:       
                print(e)
        def on_message(client, userdata, msg):
            try:
                topic = str(msg.topic)
                data = str(msg.payload.decode())
                datas = {}
                send_data = f"{topic} + {data}"
                check_topic = topic.find("/")
                # print(check_topic)
                if check_topic == -1:
                    Exception("Unknown device..")
                elif topic.split("/")[2] == "device-internal-battery":
                    datas = {
                        "device_id": topic.split("/")[3],
                        "tel_data" : data,
                        "type_data": "device-internal-battery"
                    }
                    call_success_callback(datas, send_data)
                elif topic.split("/")[2] == "vehicle-battery-voltage":
                    datas = {
                        "device_id": topic.split("/")[3],
                        "tel_data" : data,
                        "type_data": "vehicle-battery-voltage"
                    }
                    call_success_callback(datas, send_data)
                elif topic.split("/")[2] == "gps-push":
                    datas = {
                        "device_id": topic.split("/")[3],
                        "tel_data" : data,
                        "type_data": "gps-push"
                    }
                    call_success_callback(datas, send_data)
                elif topic.split("/")[2] == "remote-start-stop":
                    datas = {
                        "device_id": topic.split("/")[3],
                        "tel_data" : data,
                        "type_data": "remote-start-stop"
                    }
                    call_success_callback(datas, send_data)
                elif topic.split("/")[2] == "rfid-push":
                    datas = {
                        "device_id": topic.split("/")[3],
                        "tel_data" : data,
                        "type_data": "rfid-push"
                    }

                elif topic.split("/")[2] == "vehicle-engine-status":
                    datas = {
                        "device_id": topic.split("/")[3],
                        "tel_data" : data,
                        "type_data": "vehicle-engine-status"
                    }
                    call_success_callback(datas, send_data)
                else:
                    Exception("Unknown device..")

            except Exception as e:
                print(e)
        mqtt_client.on_message = on_message
        get_mqtt_array(mqtt_client)

        
        # Connect to MQTT Broker
        mqtt_client.connect(mqtt_broker, mqtt_port)
        mqtt_client.subscribe(mqtt_topic)
        mqtt_client.loop_start()
    except Exception as e:
        print(e)

def call_success_callback(datas, send_data):
    try:
        add_asset_tel_data(datas)
        emit_message(send_data)
    except Exception as e:
        print(e, "call_success_callback")