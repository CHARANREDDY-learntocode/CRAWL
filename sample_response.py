import time
import random

import paho.mqtt.client as paho

def on_publish(client, userdata, mid):
	print("mid: "+str(mid))

client = paho.Client()
client.on_publish = on_publish
client.username_pw_set("318624ea71ff415090c4c24ee85dc568")
client.connect("broker.hivemq.com",1883)
client.loop_start()
while True:
	payload_string = 'N1/235/95/V/OFF/M/OFF N2/235/95/V/OFF/M/ON N3/235/95/V/OFF/M/ON N4/235/95/V/OFF/M/OFF N5/235/95/V/ON/M/OFF N6/235/95/V/OFF/M/OFF N7/235/95/V/OFF/M/OFF N8/235/95/V/OFF/M/OFF N9/235/95/V/ON/M/OFF N10/235/95/V/OFF/M/OFF N11/235/95/V/OFF/M/OFF N12/235/95/V/OFF/M/OFF N13/235/95/V/OFF/M/OFF N14/235/95/V/OFF/M/OFF N15/235/95/V/ON/M/OFF N16/235/95/V/OFF/M/OFF N17/235/95/V/OFF/M/OFF N18/235/95/V/OFF/M/OFF N19/235/95/V/OFF/M/OFF N20/235/95/V/ON/M/OFF N21/235/95/V/ON/M/OFF N22/235/95/V/ON/M/OFF N23/235/95/V/ON/M/OFF N24/235/95/V/OFF/M/OFF N25/235/95/V/OFF/M/OFF N26/235/95/V/ON/M/OFF N27/235/95/V/OFF/M/OFF N28/235/95/V/OFF/M/OFF N29/235/95/V/OFF/M/OFF N30/235/95/V/ON/M/OFF'
	(rc, mid) = client.publish("NODE RESPONSE", payload_string, qos=1)
	time.sleep(10)
