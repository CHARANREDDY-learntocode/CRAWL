import threading
import time
import random

import paho.mqtt.client as paho

def on_subscribe(client, userdata, mid, granted_qos):

    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    node_data_list_string = msg.payload.decode('utf-8')
    print(f'node_data_list_string: {node_data_list_string}')
    #call the analyze to return the response
    analyze_thread = threading.Thread(target=analyze, args=[node_data_list_string])
    analyze_thread.start()

def analyze(node_data_list_string):
    #split the string using END
    data_list = node_data_list_string.split('END')
    #assign the items to corresponding variables
    node_string = data_list[0].strip()
    threshold_water_level = data_list[1].strip().split()[:2]
    willing_nodes = data_list[2].strip()
    #split the string representing each node data
    node_data_list = [node.split('/') for node in node_string.split()]
    #create empty lists for deficit and surplus nodes
    deficit_nodes, surplus_nodes = [], []
    deficit_nodes_index, surplus_nodes_index, sufficient_nodes_index = [], [], []
    #categorize the nodes depend on water threshold values
    for index, node in enumerate(node_data_list):
        if int(node[1]) < int(threshold_water_level[0]):
            deficit_nodes.append(node[0])
            deficit_nodes_index.append(index)
        elif int(node[1]) > int(threshold_water_level[1]):
            surplus_nodes.append(node[0])
            surplus_nodes_index.append(index)
        else:
            sufficient_nodes_index.append(index)
    #get the nodes willing to supply the water
    willing_nodes = [int(i) for i in willing_nodes.split(' ')]
    #get the random distances between the nodes
    distances = [random.randint(50, 600) for i in range(len(node_data_list))]
    print(distances)
    #set the number of motors in running to Zero
    active_motors = 0
    #check if there are any deficit nodes
    if len(deficit_nodes) > 0 and len(deficit_nodes) != len(node_data_list):
        #create empty payload string
        payload_string = ''
        #write the condition to turn on motor which is near to the deficit node
        quotients = [0.7*100//distances[i]+0.3*willing_nodes[i] for i in range(len(node_data_list))]
        print(quotients)
        #check for surplus nodes
        if len(surplus_nodes) > 0:
            print('Response from surplus nodes: ')
            surplus_quotients = [[surplus_nodes_index[i], quotients[surplus_nodes_index[i]]] for i in range(len(surplus_nodes_index))]
            sorted_quotients = sorted(surplus_quotients, reverse=True, key= lambda lst:lst[1])
            #calculate the index of highest quotients index
            willing_node_quotients = []
            unwilling_node_quotients = []
            for i in range(len(sorted_quotients)):
                if willing_nodes[i] == 1:
                    willing_node_quotients.append((i, sorted_quotients[i]))
                else:
                    unwilling_node_quotients.append((i, sorted_quotients[i]))
            willing_node_quotients.sort(key = lambda lst:lst[1])
            unwilling_node_quotients.sort(key = lambda lst:lst[1])
            highest_quotient_index = sorted_quotients[0][0]
            try:
                second_highest_quotient_index = sorted_quotients[1][0]
            except:
                second_highest_quotient_index = -1
            #make the list of highest surplus quotients index
            highest_surplus_quotients_index = [highest_quotient_index, second_highest_quotient_index]
            #form the payload string
            #calculate the total deficit of water
            deficit_level = 0
            for index, node in enumerate(deficit_nodes): deficit_level += (int(threshold_water_level[0]) - int(node_data_list[deficit_nodes_index[index]][1]))
            surplus_level = 0
            for node in surplus_nodes_index:
                surplus_level += (int(node_data_list[node][1]) - int(threshold_water_level[0]))
            for node_index in range(len(node_data_list)):   
                if node_index in sufficient_nodes_index:
                    sub_string = f' N{node_index+1}/{node_data_list[node_index][1]}/{node_data_list[node_index][2]}/V/OFF/M/OFF'
                elif node_index in surplus_nodes_index:
                    if node_index in highest_surplus_quotients_index:
                        if active_motors < 3:
                            active_motors += 1
                    water_to_pump_list = []
                    for node_index_no in highest_surplus_quotients_index:
                        if highest_surplus_quotients_index[1] == -1:
                            if len(highest_surplus_quotients_index) >= 2 and highest_surplus_quotients_index[1] != -1 and int(node_data_list[highest_surplus_quotients_index[1]][1]) > int(threshold_water_level[0]):
                                water_down  = deficit_level/2
                            else:
                                water_down = deficit_level
                            x = (int(node_data_list[node_index_no][1]) - int(threshold_water_level[0]))
                            if water_down < x:
                                water_to_pump = water_down
                            else:
                                water_to_pump = x
                            water_to_pump_list.append([node_index_no, water_to_pump])
                            break
                        else:
                            if len(highest_surplus_quotients_index) >= 2 and int(node_data_list[highest_surplus_quotients_index[1]][1]) > int(threshold_water_level[0]):
                                water_down  = deficit_level/2
                            else:
                                water_down = deficit_level
                            x = (int(node_data_list[node_index_no][1]) - int(threshold_water_level[0]))
                            if water_down < x:
                                water_to_pump = water_down
                            else:
                                water_to_pump = x
                            water_to_pump_list.append([node_index_no, water_to_pump])
                    counter = 0
                    if node_index in highest_surplus_quotients_index:
                        if active_motors < 3:
                            for node_number in water_to_pump_list:
                                if node_number[0] == node_index:
                                    water_decrease = node_number[1]
                            sub_string = f' N{node_index+1}/{int(node_data_list[node_index][1])-water_decrease}/{node_data_list[node_index][2]}/V/OFF/M/OFF'
                            counter += 1
                        else:
                            sub_string = f' N{node_index+1}/{node_data_list[node_index][1]}/{node_data_list[node_index][2]}/V/OFF/M/OFF'
                    else:
                        sub_string = f' N{node_index+1}/{node_data_list[node_index][1]}/{node_data_list[node_index][2]}/V/OFF/M/OFF'
                elif node_index in deficit_nodes_index:
                    water_to_draw = (int(threshold_water_level[0]) - int(node_data_list[node_index][1]))
                    if surplus_level > water_to_draw:
                            deficit_level_up = int(node_data_list[node_index][1]) + water_to_draw
                            surplus_level -= water_to_draw
                    elif surplus_level > 0:
                        deficit_level_up = int(node_data_list[node_index][1]) + surplus_level
                        surplus_level = 0
                    else:
                        deficit_level_up = int(node_data_list[node_index][1])
                    sub_string = f' N{node_index+1}/{deficit_level_up}/{node_data_list[node_index][2]}/V/OFF/M/OFF'
                else:
                    print('Hey an error occured, please check')
                print(sub_string)
                payload_string += sub_string
                    
            publish(payload_string)

        else:
            #write the condition to turn on motor which is near to the deficit node when no suplus nodes exist
            sufficient_quotients = [[sufficient_nodes_index[i], quotients[sufficient_nodes_index[i]]] for i in range(len(sufficient_nodes_index))]
            sorted_quotients = sorted(sufficient_quotients, reverse=True, key= lambda lst:lst[1])
            #calculate the index of highest quotients index
            highest_quotient_index = sorted_quotients[0][0]
            try:
                second_highest_quotient_index = sorted_quotients[1][0]
            except:
                second_highest_quotient_index = -1
            #make the list of highest surplus quotients index
            highest_sufficient_quotients_index = [highest_quotient_index, second_highest_quotient_index]
            print('quotients: ', node_data_list[highest_quotient_index], node_data_list[second_highest_quotient_index])
            #calculate the total deficit of water
            deficit_level = 0
            surplus_level = 0
            for index, node in enumerate(deficit_nodes): deficit_level += (int(threshold_water_level[0]) - int(node_data_list[deficit_nodes_index[index]][1]))
            for node in sufficient_nodes_index:
                surplus_level += (int(node_data_list[node][1]) - int(threshold_water_level[0]))
            #form the payload string
            for node_index in range(len(node_data_list)):
                if node_index in sufficient_nodes_index:
                    if node_index in highest_sufficient_quotients_index:
                        if active_motors < 3:    
                            active_motors += 1
            water_to_pump_list = []
            for node_index_no in highest_sufficient_quotients_index:
                if highest_sufficient_quotients_index[1] == -1:
                    print('len of highest surplus quotients index:', highest_sufficient_quotients_index)
                    if len(highest_sufficient_quotients_index) >= 2 and highest_sufficient_quotients_index[1] != -1 and int(node_data_list[highest_sufficient_quotients_index[1]][1]) > int(threshold_water_level[0]):
                        water_down  = deficit_level/2
                    else:
                        water_down = deficit_level
                    x = (int(node_data_list[node_index_no][1]) - int(threshold_water_level[0]))
                    if water_down < x:
                        water_to_pump = water_down
                    else:
                        water_to_pump = x
                    water_to_pump_list.append([node_index_no, water_to_pump])
                    break
                else:
                    if len(highest_sufficient_quotients_index) >= 2 and int(node_data_list[highest_sufficient_quotients_index[1]][1]) > int(threshold_water_level[0]):
                        water_down  = deficit_level/2
                    else:
                        water_down = deficit_level
                    x = (int(node_data_list[node_index_no][1]) - int(threshold_water_level[0]))
                    if water_down < x:
                        water_to_pump = water_down
                    else:
                        water_to_pump = x
                    water_to_pump_list.append([node_index_no, water_to_pump])
                    
            print('water to pump list', water_to_pump_list)
            counter = 0
            for node_index in range(len(node_data_list)):
                if node_index in sufficient_nodes_index:
                    if node_index in highest_sufficient_quotients_index:
                        if active_motors < 3:
                            for node_number in water_to_pump_list:
                                    if node_number[0] == node_index:
                                        water_decrease = node_number[1]
                            sub_string = f' N{node_index+1}/{int(node_data_list[node_index][1])-water_decrease}/{node_data_list[node_index][2]}/V/OFF/M/OFF'
                            counter += 1
                        else:
                            sub_string = f' N{node_index+1}/{node_data_list[node_index][1]}/{node_data_list[node_index][2]}/V/OFF/M/OFF'
                    else:
                        sub_string = f' N{node_index+1}/{node_data_list[node_index][1]}/{node_data_list[node_index][2]}/V/OFF/M/OFF'
                elif node_index in deficit_nodes_index:
                    water_to_draw = (int(threshold_water_level[0]) - int(node_data_list[node_index][1]))
                    if surplus_level > water_to_draw:
                            deficit_level_up = int(node_data_list[node_index][1]) + water_to_draw
                            surplus_level -= water_to_draw
                    elif surplus_level > 0:
                        deficit_level_up = int(node_data_list[node_index][1]) + surplus_level
                        surplus_level = 0
                    else:
                        deficit_level_up = int(node_data_list[node_index][1])

                    sub_string = f' N{node_index+1}/{deficit_level_up}/{node_data_list[node_index][2]}/V/OFF/M/OFF'
                else:
                    print('Hae something is wrong')
                print(sub_string)
                payload_string += sub_string
            publish(payload_string)
            
    elif len(deficit_nodes) == 0 or len(deficit_nodes) == len(node_data_list):
        #create an empty string for sending the response
        print(f'Response from no deficit: ')
        payload_string = ''
        #append the response of each node in string format
        for node in node_data_list:
            payload_string += f'{node[0]}/{node[1]}/{node[2]}/V/OFF/M/OFF '
            print(f'{node[0]}/{node[1]}/{node[2]}/V/OFF/M/OFF ')
        #print the payload_string
        publish(payload_string)
    else:
        pass
    
    print()

def on_publish(client, userdata, mid):
	print("Published")

def publish(payload_string):
    client.publish('STABLE NODE RESPONSE', payload_string, qos=1)

def connect():
    global client
    client = paho.Client()
    client.on_subscribe = on_subscribe
    client.on_message =on_message
    client.on_publish = on_publish
    client.username_pw_set("318624ea71ff415090c4c24ee85dc568")
    client.connect("broker.hivemq.com",1883)
    client.subscribe("NODES", qos=1)
    client.loop_forever()

connect()
