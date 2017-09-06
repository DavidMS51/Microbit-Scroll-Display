# microbit Scrolling Display application
# David Saul copyright 2017 @david_ms, www.meanderingpi.wordpress.com
# Inspired by and utilising code by David Whale [@whaleygeek] 
# Available under MIT License via github.com/DavidMS51

# This code is for the gate-way microbit. which 'talks' to a number of 'display node' microbits [up to 99]
# running the demo_scroll_show application

# Set the number of 'display' node microbits at power up when you see 'D' being displayed
# using the 'A' Button to increase the number and the 'B' button to confirm
# the value will be sorted and automatically loaded thereafter

# The application works with a 3rd application running on the raspberry pi called gateway_scroll
# for installation instructions see Github

from microbit import *
import radio



radio.config(group=0)
radio.on()

uart.init(baudrate=115200)

def print(*args, **kwargs):
    pass # disable print function


#configure no of displays
def conf_nd():
    d_no = 0
    while True:
        if button_a.was_pressed():
            d_no = d_no + 1
            if d_no > 9:
                d_no = 1
            display.scroll(str(d_no), wait= False, loop = True)
            while button_a.is_pressed():
                sleep(100)
        elif button_b.was_pressed():
            with open('node_total.txt','w') as my_file:
                my_file.write(str(d_no))
            display.show(Image.YES)
            sleep(500)
            break       
    return d_no

#show a complete message
# if message longer than number of display nodes message is truncated from the left
# ie you lose the right hand end of the message
def disp_show(msg):
    global d_no
    
    #pad short messages and truncate long ones
    if d_no-len(msg)>0:
        msg = msg+(" "*(d_no-len(msg)))
    else:
        msg = msg[0:d_no]
        
    for x in range(1,d_no+1):
        radio.send(str(x)+msg[x-1:x])
        sleep(40)

def disp_scroll(msg):
    global d_no
    #format message for scrolling
    m_len=len(msg)
    m_len_o=m_len       # save a copy of original length message
    gap = 0
    
    #for short messages pad with leading spaces to number of display nodes
    if m_len < d_no:
        gap = d_no - m_len
        msg = (" "*((gap)+1))+msg
        m_len=len(msg)  # update message length
    
    #build final message    
    pack = (" "*d_no) + msg + (" "*m_len)
     
    #display full scrolled message
    for x in range (1+gap,(m_len+d_no)+1):  
            msg_s = pack[x:x+(m_len)]
            for y in range (1,d_no+1):
                radio.send(str(y)+msg_s[y-1:y])
                sleep(40)
            sleep(250)

# manual config if 'a' held down at reset
display.show('-')
sleep(500)
display.show('D')
if button_a.was_pressed():
    char = conf_nd()

# try to get existing address
try:
    with open('node_total.txt') as my_file:
        d_no = int(my_file.read())
    display.show(Image.YES)
    sleep(500)
except:
    d_no = conf_nd()

if int(d_no)>9:
    display.scroll(str(d_no), wait = False, loop = True)
else:
    display.show(str(d_no))

sleep(500)

msg = " "
new = True
while True:
    msg_r = uart.readline()
    if msg_r is not None:
        display.show("^")
       #display.scroll(msg)   
        msg = msg_r # update  message
        new = False
    else:
        display.show("-")
    
    if new is not True:
       # display.scroll(str(msg)[2:3])
        #sleep(4000)
        
        if str(msg)[2:3]=='1':
        #if new is not True:  
            disp_show(str(msg)[3:-1]) # display the message as a 'show'
        elif str(msg)[2:3]=='2':
            disp_scroll(str(msg)[3:-1]) # display the message as a 'scroll'
        else:
            new = False   