import paho.mqtt.client as mqttclient
import time


def on_connect(client,userdata,flags,rc):
	if rc==0:
		print("client is connected")
		global connected
		connected=True
	else:
		print("connection failed")

connected = False

broker_address ="maqiatto.com"
port = 1883
user = "rajini.my98@gmail.com"
password = "poojabhagavan"

client=mqttclient.Client("MQTT")
client.username_pw_set(user,password=password)

client.on_connect=on_connect
client.connect(broker_address,port=port)

client.loop_start()
while connected!=True:
	time.sleep(0.2)

client.publish("rajini.my98@gmail.com/test1","Hello World")
client.loop_stop()

