import tkinter
import random
import threading

import paho.mqtt.client as paho

def extract_data(data_string):
    nodes = [node.split('/') for node in data_string.strip().split(' ')]
    node_numbers = [node[0] for node in nodes]
    water_levels = [node[1] for node in nodes]
    valve_status = [node[4] for node in nodes]
    motor_status = [node[6] for node in nodes]
    return node_numbers,water_levels, valve_status, motor_status

def create_common_pipe():
    x1, y1, x2, y2 = 40, (height//2-30), (width-40), (height//2-30)
    x3, y3, x4, y4 = 40, (height//2+30), (width-40), (height//2+30)
    my_canvas.create_line(x1, y1, x2, y2, fill='black', width=5)
    my_canvas.create_line(x3, y3, x4, y4, fill='black', width=5)
    my_canvas.create_oval(x1-15, y1, x1+15, y3, width=3, fill='red')
    my_canvas.create_oval(x4-15, y1, x4+15, y3, width=3, fill='red')

def create_well(nodes):
    def mark_water_level(my_canvas, i, x, y):
        if i%2 == 0: my_canvas.create_text(x, y - 80, fill='blue', font='arial 12  bold', text=node_numbers[i])
        else: my_canvas.create_text(x, y + 80, fill='blue', font='arial 12  bold', text=node_numbers[i])
        my_canvas.create_text(x, y, fill='blue', font='arial 12  bold', text=water_levels[i])

    #for ovals upper, lower
    x1, y1, x2, y2 = 80, (height//2 - height * 0.4), 120, (height//2 - height*0.35)
    x3, y3, x4, y4 = 80, (height//2 - height * 0.3), 120, (height//2 - height * 0.25)
    center_height = 20
    large_wells = True
    
    for i in range(nodes):
        if i<5:
            if i%2 == 0:
                my_canvas.create_line(x1, y1 + center_height, x3, y3+center_height, fill='black', width=5)
                my_canvas.create_line(x2+40, y2 - center_height, x4+40, y4 - center_height, fill='black', width=5)
                my_canvas.create_oval(x1, y1, x2+40, y2, width=5, fill='skyblue')
                my_canvas.create_oval(x3, y3, x4+40, y4, width=5)
                mark_water_level(my_canvas, i, x1 + (x4+40-x1)//2, y1+center_height - (y1-y4+40)//2)
                
            else:
                temp_y1 = (height//2 + height * 0.35)
                temp_y2 = (height//2 + height*0.4)
                temp_y3 = (height//2 + height*0.25)
                temp_y4 = (height//2 + height*0.3)
                my_canvas.create_line(x1, temp_y1 + center_height, x3, temp_y3+center_height, fill='black', width=5)
                my_canvas.create_line(x2+40, temp_y2 - center_height, x4+40, temp_y4-center_height, fill='black', width=5)
                my_canvas.create_oval(x1, temp_y1, x2+40, temp_y2, width=5, fill='skyblue')
                my_canvas.create_oval(x3, temp_y3, x4+40, temp_y4, width=5)
                mark_water_level(my_canvas, i, x1 + (x4+40-x1)//2, temp_y1+center_height - (temp_y1-temp_y4+40)//2)
            if nodes <= 5:
                spacing_for_5 = width//nodes
                #calculate the space to place the nodes at equidistant from each other
                x1 += spacing_for_5
                x2 += spacing_for_5
                x3 += spacing_for_5
                x4 += spacing_for_5
            else:
                x1 += 55
                x2 += 55
                x3 += 55
                x4 += 55
            
        else:
            if large_wells:
                spacing = ((width - 420)//(nodes - 5))
                large_wells = False
                x1 += 15
                x2 += 15
                x3 += 15
                x4 += 15
            if i%2 == 0:
                my_canvas.create_line(x1, y1 + center_height, x3, y3 + center_height, fill='black', width=5)
                my_canvas.create_line(x2, y2 - center_height, x4, y4 - center_height, fill='black', width=5)
                my_canvas.create_oval(x1, y1, x2, y2, width=5, fill='skyblue')
                my_canvas.create_oval(x3, y3, x4, y4, width=5)
                mark_water_level(my_canvas, i, x1 + (x4-x1)//2, y1+center_height - (y1-y4+40)//2)
                
            else:
                my_canvas.create_line(x1, temp_y1 + center_height, x3, temp_y3 + center_height, fill='black', width=5)
                my_canvas.create_line(x2, temp_y2 - center_height, x4, temp_y4 - center_height, fill='black', width=5)
                my_canvas.create_oval(x1, temp_y1, x2, temp_y2, width=5, fill='skyblue')
                my_canvas.create_oval(x3, temp_y3, x4, temp_y4, width=5)
                mark_water_level(my_canvas, i, x1 + (x4-x1)//2, temp_y1+center_height - (temp_y1-temp_y4+40)//2)
                
            #calculate the space to place the nodes at equidistant from each other
            x1 += spacing
            x2 += spacing
            x3 += spacing
            x4 += spacing

def create_connection_pipe(my_canvas, nodes):
    def place_valve(my_canvas, i, down, x, y):
        if down:
            my_canvas.create_rectangle(x-15,y-120, x+30, y-160, fill='white')
            my_canvas.create_text(x+10, y-150, fill='darkblue', font='arial 10  bold', text='Valve')
            if valve_status[i] == 'OFF': my_canvas.create_text(x+10, y-130,  fill='red', font='arial 14  bold', text=valve_status[i])
            else: my_canvas.create_text(x+10, y-130,  fill='green', font='arial 14  bold', text=valve_status[i])
        else:
            my_canvas.create_rectangle(x-15,y+120, x+30, y+160, fill='white')
            my_canvas.create_text(x+10, y+130, fill='darkblue', font='arial 10  bold', text='Valve')
            if valve_status[i] == 'OFF': my_canvas.create_text(x+10, y+150,  fill='red', font='arial 14  bold', text=valve_status[i])
            else: my_canvas.create_text(x+10, y+150,  fill='green', font='arial 14  bold', text=valve_status[i])
    
    def place_motor(my_canvas,i, down, x, y):
        if down:
            my_canvas.create_rectangle(x-15,y-50, x+30, y-90, fill='white')
            my_canvas.create_text(x+10, y-80, fill='darkblue', font='arial 10  bold', text='Motor')
            if motor_status[i] == 'OFF': my_canvas.create_text(x+10, y-60,  fill='red', font='arial 14  bold', text=motor_status[i])
            else: my_canvas.create_text(x+10, y-60,  fill='green', font='arial 14  bold', text=motor_status[i])
        else:
            my_canvas.create_rectangle(x-15,y+50, x+30, y+90, fill='white')
            my_canvas.create_text(x+10, y+60, fill='darkblue', font='arial 10  bold', text='Motor')
            if motor_status[i] == 'OFF': my_canvas.create_text(x+10, y+80,  fill='red', font='arial 14  bold', text=motor_status[i])
            else: my_canvas.create_text(x+10, y+80,  fill='green', font='arial 14  bold', text=motor_status[i])

    #for lines left & right
    x1, y1, x2, y2 = 110, (height//2 - int(height * 0.275)), 110, (height//2 - 30)
    x3, y3, x4, y4 = 130, (height//2 - int(height * 0.275)), 130, (height//2 - 30)
    large_wells = True


    for i in range(nodes):
        if i < 5:
            if i%2 == 0:
                my_canvas.create_line(x1, y1, x2, y2, fill='blue', width=2)
                my_canvas.create_line(x3, y3, x4, y4, fill='blue', width=2)
                my_canvas.create_oval(x2, y2-7.5, x4, y4+7.5, fill='white', width=5)
                my_canvas.create_oval(x1, y1-7.5, x3, y3+7.5, fill='white', width=5)
                place_valve(my_canvas, i, False, x1, y1)
                place_motor(my_canvas, i, False, x1, y1)
                
            else:
                temp_y1 = (height//2+30)
                temp_y2 = y2 + height*0.275+30
                temp_y3 = (height//2+30)
                temp_y4 = y4 + height*0.275+30
                my_canvas.create_line(x1, temp_y1, x2, temp_y2, fill='blue', width=2)
                my_canvas.create_line(x3, temp_y3, x4, temp_y4, fill='blue', width=2)
                my_canvas.create_oval(x2, temp_y2 - 7.5, x4, temp_y4 + 7.5, fill='white', width=5)
                my_canvas.create_oval(x1, temp_y1-7.5, x3, temp_y3+7.5, fill='white', width=5)
                place_valve(my_canvas, i, True, x2, temp_y2)
                place_motor(my_canvas, i, True, x2, temp_y2)
            if nodes <= 5:
                spacing_for_5 = width//nodes
                #calculate the space to place the nodes at equidistant from each other
                x1 += spacing_for_5
                x2 += spacing_for_5
                x3 += spacing_for_5
                x4 += spacing_for_5
            else:
                x1 += 55
                x2 += 55
                x3 += 55
                x4 += 55
        else:
            if large_wells:
                spacing = ((width - 420)//(nodes - 5))
                large_wells = False
                x1 -= 5
                x2 -= 5
                x3 -= 5
                x4 -= 5
            if i%2 == 0:
                my_canvas.create_line(x1, y1, x2, y2, fill='blue', width=2)
                my_canvas.create_line(x3, y3, x4, y4, fill='blue', width=2)
                my_canvas.create_oval(x2, y2-7.5, x4, y4+7.5, fill='white', width=5)
                my_canvas.create_oval(x1, y1-7.5, x3, y3+7.5, fill='white', width=5)
                place_valve(my_canvas, i, False, x1, y1)
                place_motor(my_canvas, i, False, x1, y1)
            else:
                temp_y1 = (height//2+30)
                temp_y2 = y2 + height*0.275+30
                temp_y3 = (height//2+30)
                temp_y4 = y4 + height*0.275+30

                my_canvas.create_line(x1, temp_y1, x2, temp_y2, fill='blue', width=2)
                my_canvas.create_line(x3, temp_y3, x4, temp_y4, fill='blue', width=2)
                my_canvas.create_oval(x2, temp_y2 - 7.5, x4, temp_y4 + 7.5, fill='white', width=5)
                my_canvas.create_oval(x1, temp_y1-7.5, x3, temp_y3+7.5, fill='white', width=5)
                place_valve(my_canvas, i, True, x2, temp_y2)
                place_motor(my_canvas, i, True, x2, temp_y2)
            #calculate the space to place the nodes at equidistant from each other
            x1 += spacing
            x2 += spacing
            x3 += spacing
            x4 += spacing

def on_subscribe(client, userdata, mid, granted_qos):
    print('subscribed')

def on_message(client, userdata, msg):
    global node_numbers, water_levels, valve_status, motor_status
    data_string = msg.payload.decode('utf-8')
    print(msg.payload.decode('utf-8'))
    my_canvas.delete('all')
    create_common_pipe()
    node_numbers, water_levels, valve_status, motor_status = extract_data(data_string)
    create_well(len(water_levels))
    create_connection_pipe(my_canvas, len(water_levels))
    
def connect():
    client = paho.Client()
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.username_pw_set("318624ea71ff415090c4c24ee85dc568")
    client.connect("broker.hivemq.com",1883)
    client.subscribe("STABLE NODE RESPONSE", qos=1)
    client.loop_forever()

connection_thread = threading.Thread(target=connect, daemon=True)
connection_thread.start()
root = tkinter.Tk()
root.title('CRAWL')
root.iconbitmap('logo.ico')
#calculate the screen width and height
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
#create canvas widget
my_canvas = tkinter.Canvas(root, width=width, height=height, bg='#bce8e0')
my_canvas.pack(fill=tkinter.BOTH, expand=1)
tkinter.Label(text='Cloud based Real-time interconnections of agricultural Water Resources using LoRa', fg='#346eeb', bg='#bce8e0', font='Arial 23 bold underline').place(x=30, y=0)
create_common_pipe()
root.mainloop()