import socketio
from config import SOCKET_URI

mqtt_arr = []

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")

@sio.event
def disconnect():
    print("Disconnected from server")

# @sio.on('message_from_server')
# def handle_message(data):
#     print(f"Received message from server: {data}")

def send_message(data):
    # print(f"Received message from server: {data}")
    send_client_data(data)

sio.on('clientmessage', send_message)



sio.connect(SOCKET_URI)  


def emit_message(data):
    try:
        # print(data)
        sio.emit('message',  data)
    except Exception as e:
        print(e)

def initialize_client_socket():
    try:
        sio.wait()
    except KeyboardInterrupt:
        sio.disconnect()

def get_mqtt_array(mqtt):
    try: 
        mqtt_arr.append(mqtt)
    except Exception as e:
        print(e)

def send_client_data(msg):
            try:
                if len(mqtt_arr):
                    mqtt_client = mqtt_arr[0]
                    # print(msg)
                    data_arr = msg.split("#")
                    topic = data_arr[0]
                    message = data_arr[1]
                    # print(mqtt_client)
                    mqtt_client.publish(topic, message)
                else:
                    Exception("Unable to send")
            except Exception as e:
                print(e)