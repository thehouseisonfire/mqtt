import uuid, time, threading
import paho.mqtt.client as mqtt
#import dataclasses from dataclass

host="127.0.0.1"
port=1883
keepalive=60

status = {}
groups = set()
group_invites = {}
talk_invites = set()
 
class Group:
    
    name = ""
    leader = ""
    members = set()

    def __init__(self,name,leader):
        self.name = name
        self.leader = leader

    def add(self,member):
        self.members.add(member)

    def remove(self,member):
        self.members.remove(member)

    def isMember(self, member):
        if(member in self.members):
            return True
        else:
            return False


#userdata = None | Status | Group

def status_update(client):
    while(True):
        global stop_threads
        if stop_threads:
            break
        c = client._client_id.decode("utf-8")
        client.publish("clients/status", f"{c} ON",2, True)
        time.sleep(10)# sleep for 10 seconds         time.sleep(10)# sleep for 10 seconds 

def on_connect(client, clientdata, flags, rc):
    ##print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    
    client.subscribe("clients/status", 2)
    client.subscribe("groups/info", 2)
    c = client._client_id.decode("utf-8")
    client.subscribe("clients/"+c,2)
    client.publish("clients/status", f"{c} ON",2, True)



def on_message(client, userdata, msg):
    #print("Received message '" + str(msg.payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))
    #print(msg.payload)
    match msg.topic:
        case 'clients/status':
            payload = msg.payload.decode("utf-8")
            name, s = payload.split();
            status[name] = s
        case 'clients/wills':
            name = msg.payload.split()[0]
            status[name] = "OFF"
        case 'groups/info':
            payload = msg.payload.decode("utf-8")
            msg = payload.split()
            match msg[0]:
                case "CREATE":
                    print(msg)
                    groups.add(msg[1] +" "+ msg[2])
                case "DISBAND":
                    client.unsubscribe("groups/"+group)
                
        case _:
            if(msg.topic == ("clients/"+id)):
                payload = msg.payload.decode("utf-8")
                #print(payload)
                l = payload.split()
                match l[0]:
                    case 'GI':
                        group_invites[l[1]] = l[2];
                    case 'R':
                        talk_invites.add(l[1]);
                                

        


def new_client(id):
    client = mqtt.Client(client_id=id, clean_session=False, userdata=None, transport="tcp")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host, port, keepalive)
    s = f"{id} OFF"
    client.will_set("clients/status", s, qos=1, retain=False)
    client.loop_start()
    return client



id = str(input("Type your id: "))
client = new_client(id);

stop_threads = False
t_status = threading.Thread(target = status_update, args =(client,))
t_status.start();


while True:

    print("--- OPTIONS ---")
    print("1. List clients")
    print("2. Create group")
    print("3. List groups")
    print("4. Request talk with client")
    print("5. List all talk requests")
    #print("6. List all talk requests + info")
    print("0. Exit")


    option = int(input("\n select option: "))

    match option:

        case 1:
            print(status)
        case 2:
            i = input("Type the group name: ")
            group = Group(i,id)
            
            
            while True:
                for s in status:
                    if(status[s] == "ON" and s != id and not group.isMember(s)): 
                        print(s)
                
                member = input("type member name (type nothing to stop): ")
                if(member == ""):
                    break
                group.add(member)
            
            client.publish("groups/info",f"CREATE {group.name} {group.leader}")
            #client.publish("groups/info", f"{group} CREATE", 2, True)
            #client.publish("groups/info", f"{group} LEADER {id}", 2, True)
            #client.publish("groups/info", f"{group} MEMBER {member}", 2, True)

        case 3:
            print(groups)
        case 4:
            for s in status:
                if(status[s] == "ON" and s != id): 
                    print(s)
            
            i = input('Select the Client: ')
            if(i == ""):
                break

            if (status[i] == "ON" and i != id):
                client.publish(f"clients/{i}", f"R {id}",2,True)
            else:
                print("INVALID")

        case 5:
            print(talk_invites)
        case 0:
            print(id)
            stop_threads = True
            t_status.join()
            client.publish("clients/status", f"{id} OFF",2,True).wait_for_publish()
            client.disconnect()
            break

