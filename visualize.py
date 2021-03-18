import tkinter
import random

def extract_data(data_string):
    nodes = [node_string.split('/') for node_string in data_string.split(' ')]
    water_levels = [node[1] for node in nodes]
    valve_status = [node[4] for node in nodes]
    motor_status = [node[6] for node in nodes]
    return water_levels, valve_status, motor_status

def create_common_pipe():
    x1, y1, x2, y2 = 40, (height//2-30), (width-40), (height//2-30)
    x3, y3, x4, y4 = 40, (height//2+30), (width-40), (height//2+30)
    my_canvas.create_line(x1, y1, x2, y2, fill='black', width=5)
    my_canvas.create_line(x3, y3, x4, y4, fill='black', width=5)
    my_canvas.create_oval(x1-15, y1, x1+15, y3, width=3, fill='red')
    my_canvas.create_oval(x4-15, y1, x4+15, y3, width=3, fill='red')

def create_well(nodes):
    def mark_water_level(my_canvas, i, x, y):
        if i%2 == 0: my_canvas.create_text(x, y - 80, fill='blue', font='arial 12  bold', text=f'N{i+1}')
        else: my_canvas.create_text(x, y + 80, fill='blue', font='arial 12  bold', text=f'N{i+1}')
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
                spacing = ((width - 420)//(nodes - 3))
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
            my_canvas.create_rectangle(x-15,y-50, x+30, y-90, fill='white')
            my_canvas.create_text(x+10, y-80, fill='darkblue', font='arial 10  bold', text='Valve')
            if valve_status[i] == 'OFF': my_canvas.create_text(x+10, y-60,  fill='red', font='arial 14  bold', text=valve_status[i])
            else: my_canvas.create_text(x+10, y-60,  fill='green', font='arial 14  bold', text=valve_status[i])
        else:
            my_canvas.create_rectangle(x-15,y+50, x+30, y+90, fill='white')
            my_canvas.create_text(x+10, y+60, fill='darkblue', font='arial 10  bold', text='Motor')
            if valve_status[i] == 'OFF': my_canvas.create_text(x+10, y+80,  fill='red', font='arial 14  bold', text=valve_status[i])
            else: my_canvas.create_text(x+10, y+80,  fill='green', font='arial 14  bold', text=valve_status[i])
    
    def place_motor(my_canvas,i, down, x, y):
        if down:
            my_canvas.create_rectangle(x-15,y-120, x+30, y-160, fill='white')
            my_canvas.create_text(x+10, y-150, fill='darkblue', font='arial 10  bold', text='Valve')
            if motor_status[i] == 'OFF': my_canvas.create_text(x+10, y-130,  fill='red', font='arial 14  bold', text=motor_status[i])
            else: my_canvas.create_text(x+10, y-130,  fill='green', font='arial 14  bold', text=motor_status[i])
        else:
            my_canvas.create_rectangle(x-15,y+120, x+30, y+160, fill='white')
            my_canvas.create_text(x+10, y+130, fill='darkblue', font='arial 10  bold', text='Motor')
            if motor_status[i] == 'OFF': my_canvas.create_text(x+10, y+150,  fill='red', font='arial 14  bold', text=motor_status[i])
            else: my_canvas.create_text(x+10, y+150,  fill='green', font='arial 14  bold', text=motor_status[i])

    #for lines left & right
    x1, y1, x2, y2 = 110, (height//2 - int(height * 0.275)), 110, (height//2 - 30)
    x3, y3, x4, y4 = 130, (height//2 - int(height * 0.275)), 130, (height//2 - 30)
    large_wells = True


    for i in range(nodes):
        '''my_canvas.create_text(x1-10, y1+10,fill="darkblue",font="arial 14  bold",text=i)
        
        my_canvas.create_text(x2 +(((x4-x2)//2)-10), y4+80,fill="darkblue",font="arial 14  bold",text=f'N{i}')
        my_canvas.create_text(x2 +(((x4-x2)//2)-10), y4+120,fill="darkblue",font="arial 14  bold",text=f'Water\nLevel: {random.randint(20, 100)}')'''
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
                spacing = ((width - 420)//(nodes - 3))
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

root = tkinter.Tk()
#calculate the screen width and height
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
#create canvas widget
my_canvas = tkinter.Canvas(root, width=width, height=height, bg='#bce8e0')
my_canvas.pack(fill=tkinter.BOTH, expand=1)
tkinter.Label(text='Cloud based Real-time interconnections of agricultural Water Resources using LoRa', fg='#346eeb', bg='#bce8e0', font='Arial 25 bold').place(x=100, y=20)

data_string = '''N1/235/95/V/OFF/M/OFF N2/55/95/V/OFF/M/ON N3/95/95/V/OFF/M/ON N4/105/95/V/OFF/M/OFF N5/25/95/V/ON/M/OFF N6/235/95/V/OFF/M/OFF N7/55/95/V/OFF/M/OFF N8/97/95/V/OFF/M/OFF N9/100/95/V/ON/M/OFF N10/110/95/V/OFF/M/OFF N11/210/95/V/OFF/M/OFF N12/155/95/V/OFF/M/OFF N13/136/95/V/OFF/M/OFF N14/145/95/V/OFF/M/OFF N15/189/95/V/ON/M/OFF N1/235/95/V/OFF/M/OFF N2/55/95/V/OFF/M/ON N3/95/95/V/OFF/M/ON N4/105/95/V/OFF/M/OFF N5/25/95/V/ON/M/OFF N6/235/95/V/OFF/M/OFF N7/55/95/V/OFF/M/OFF N8/97/95/V/OFF/M/OFF N9/100/95/V/ON/M/OFF N10/110/95/V/OFF/M/OFF N11/210/95/V/OFF/M/OFF N12/155/95/V/OFF/M/OFF N13/136/95/V/OFF/M/OFF N14/145/95/V/OFF/M/OFF N15/189/95/V/ON/M/OFF'''
water_levels, valve_status, motor_status = extract_data(data_string)
create_common_pipe()
create_well(len(water_levels))
create_connection_pipe(my_canvas, len(water_levels))

#my_canvas.create_line(0, 0, 200, 200, width=10, fill='blue')
root.mainloop()