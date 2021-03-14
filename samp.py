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

#ask the user for number of nodes
nodes = int(input('Enter the number of nodes: '))
threshold_values = [int(value) for value in input('Enter the Water level threshold values(Min, Max): ').split()]
pressure_threshold = int(input('Enter the Pressure threshold value: '))

while True:
	water_levels, pressure_levels = [], []
	payload_string = ''
	#create dummy lists for water and pressure levels
	for i in range(nodes):
		water_levels.append(random.randint((threshold_values[0]-20), (threshold_values[1]+50)))
		pressure_levels.append(random.randint(pressure_threshold-70, pressure_threshold))
	#Create  the payload string
	for node in range(1, nodes+1):
		payload_string += f'N{node}/{water_levels[node-1]}/{pressure_levels[node-1]} '
	#add the threshold values to payload string
	threshold_str = ' '.join(str(item) for item in threshold_values)
	threshold_str += ' ' + str(pressure_threshold)
	payload_string += 'END ' + threshold_str + ' END '
	#create a random list containing 1s&0s  for willingness to provide water
	payload_string += ' '.join([str(random.randint(0, 1)) for i in  range(nodes)])
	#publish the value to the node
	(rc, mid) = client.publish("NODES", payload_string, qos=1)
	print(payload_string)
	'''#publish the threshold values
	threshold_str = ' '.join(str(item) for item in threshold_values)
	threshold_str += ' ' + str(pressure_threshold)
	(rc, mid) = client.publish("NODES_THRESHOLD", threshold_str, qos=1)
	#publish the surplus nodes which are willing to provide water
	(rc, mid) = client.publish("WILLING_NODES", ' '.join(willing_to_provide), qos=1)
	#stop execution for five seconds'''
	time.sleep(5)
