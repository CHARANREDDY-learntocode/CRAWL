#ask the user to input number of nodes
node_string = input('Enter the node node data string: ')
#ask the user to input threshold water levels
threshold_water_level = input('enter the threshold water_level rates: ').split()

if len(node_string) == 0: node_string = 'N1/235/95 N2/80/0 N3/30/98'
#split the string representing each node data	
node_data_list = [node.split('/') for node in node_string.split()]
#create empty lists for deficit and surplus nodes
deficit_nodes = []
surplus_nodes = []
#categorize the nodes depend on water threshold values
for node in node_data_list:
	if int(node[1]) < int(threshold_water_level[0]):
		deficit_nodes.append(node[0])
	elif int(node[1]) > int(threshold_water_level[1]):
		surplus_nodes.append(node[0])
	else:
		pass
#create an empty string for sending the response
payload_string = ''
#append the response of each node in string format
for node in node_data_list:
	if int(node[1]) < int(threshold_water_level[0]):
		payload_string += f'{node[0]}/V/ON/M/OFF '
	elif int(node[1]) > int(threshold_water_level[1]):
		payload_string += f'{node[0]}/V/ON/M/ON '
	else:
		payload_string += f'{node[0]}/V/OFF/M/OFF '
#print the payload_string
print(f'Response: {payload_string}')