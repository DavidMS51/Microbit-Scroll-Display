# microbit Scrolling Display application  - 1 of 3 applications
# David Saul copyright 2017 @david_ms, www.meanderingpi.wordpress.com
# Inspired by and utilising code by David Whale [@whaleygeek] 
# Available under MIT License via github.com/DavidMS51

# This code is for the display node microbits. This listens for messages addressed
# to it from the 'gateway' microbit, and respond accordingly 
# Arrange the microbits with address on the far left

# Set the address of the display node microbit at power up when you see '?' being displayed
# using the 'A' Button to increase the number and the 'B' button to confirm
# The value will be stored and automatically loaded thereafter - should work ok up to 99 microbits

from microbit import *
import radio

radio.config(channel = 56, group = 0) # channel 56 was chosen at randon to avoid clashing
radio.on()


#configure address
def conf_add():
    char_r = 0
    while True:
        if button_a.was_pressed():
            char_r = char_r + 1
            if char_r > 99:
                char_r = 1
            display.scroll(str(char_r), wait= False, loop = True)
            while button_a.is_pressed():
                sleep(100)
        elif button_b.was_pressed():
            with open('address.txt','w') as my_file:
               #pad node nos below 10 with leading zero
                if char_r <10:
                    char="0"+str(char_r)
                else:    
                    char=str(char_r)
                
                my_file.write(char)
            display.show(Image.YES)
            sleep(500)
            break 
    return char

# manual config if 'a' held down at reset
display.show('-')
sleep(500)
display.show('?')
if button_a.was_pressed():
    char = conf_add()

# try to get existing address
try:
    with open('address.txt') as my_file:
        char = my_file.read()
    display.show(Image.YES)
    sleep(500)
except:
    char = conf_add()

display.scroll(char, wait = False, loop = True)


#Main display loop
while True:
    try:
        msg = radio.receive()
        if msg is not None:
            if len(msg) > 0 and msg[:2] == char:
                display.show(msg[2:])
            
    except:
        display.show("X")
        radio.off()
        sleep(250)
        radio.on()
        display.show("-")
