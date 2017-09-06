# microbit Scrolling Display application 3 of 3 application  - BASIC DISPLAY VERSION
# David Saul 2017 @david_ms, www.meanderingpi.wordpress.com
# Inspired by and utilising code by David Whale [@whaleygeek] 
# Available under MIT License via github.com/DavidMS51

# This code is for the Raspberry Pi - with is communicating with a gateway micro:bit connected via a USB port


# requires microbit module in same directory as this applicaion


import microbit
import time
import os

SEND_RATE = 1.0

def process_incoming(msg):
    print("rx:%s" % str(msg))
    #Add your incoming message processing here
    #any radio message sent by any microbit, will arrive here

def process_outgoing(msg):
    # Example of sending a message on a timer
    # Just call microbit.send_message whenever you have new data
    # this will be sent to the gateway micro:bit which will then
    # broadcast it to all listening micro:bit devices
   #  print("tx:%s" % str(msg))
    microbit.send_message(msg)

next_send = time.time() + SEND_RATE

print("gateway running")

count = 0
while True:
#    msg = microbit.get_next_message()
#    if msg is not None:
#        process_incoming(msg)
#
#    now = time.time()
#    if now >= next_send:
#       next_send = now + SEND_RATE
#       process_outgoing(str(count))
#       count = (count + 1) % 10

     type = raw_input('1=Show, 2=Scroll ? ')	
     msg = raw_input("Message ?  ")
     process_outgoing(type+msg)
     os.system('clear')
	
	
