﻿# Microbit-Scroll-Display
Files to support my scrolling display project

In simple terms a 'gateway micro:bit' communicates with up to 99 [ ok I have only tested with 10 so far ] using the radio function
microbit chopping the message up to create a scrolling message affect with micro:bits positioned in a line.
The gateway microbit runs a python app called 'gate_scroll_r3.py.py'
The 'display micro:bits' a second app called 'node_scroll_show3.py

The gateway micro:bit is linked to a RaspberryPi via a USB connection. So far I have
included a couple of basic demo apps for the Raspberry Pi end one that display massages entered [gateway1.py]
on the keyboard the other listens for tweets with the prefix #m:bitrocks and displaying the twitter text [tweepy8a_microbit1.py]

Do to  
- clean up raspberry pi s/w
- buy more micro:bits
- build a dedicarted Pi / micro:bit box

I will produce a better write up of the project shortly
