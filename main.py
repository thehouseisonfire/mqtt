import uuid, time
import paho.mqtt.client as mqtt


host="127.0.0.1"
port=1883
keepalive=60

status = []
groups = []

# class Status:
#     status = "ON"
#     clean = True
#     time = int(time.time())

class Group:
    name = ""
    leader = ""
    members = []


def on_connect(client, clientdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("clients/#", 2)

    # basic setup
    client.publish("clients/status", "ON")

def on_message(client, userdata, msg):
    print("new message on topic "+ msg.topic+": "+str(msg.payload))
    match msg.topic:
        case 'clients/status':
            (name, s) = msg.payload.split()
            status[name] = s
        case 'clients/wills':
            name = msg.payload.split()[0]
            status[name] = "OFF"
        case 'groups/news':
            (group, cmd) = msg.payload.split()
            match cmd:
                case "CREATE":
                    client.subscribe("groups/"+group)
                case "DISBAND":
                    client.unsubscribe("groups/"+group)



def new_client(id: str):
    client = mqtt.Client(client_id=id, clean_session=True, userdata=None, transport="tcp")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host, port, keepalive)
    client.will_set("clients/wills", "DEAD", qos=2, retain=True)
    client.loop_forever()
    return client



id = str(uuid.uuid4())
client = new_client(id)

print("--- OPTIONS ---")
print("1. List clients")
print("2. Create group")
print("3. List groups")
print("4. Request talk with client")
print("5. List all talk requests")
print("6. List all talk requests + info")

option = int(input("\n select option: "))

match option:

    case 1:
        print(status)
    case 2:
        print(groups)

