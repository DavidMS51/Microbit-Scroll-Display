# Microbit-Scroll-Display
Files to support my scrolling display project

In simple terms a 'gateway micro:bit' communicates with up to 99 [ ok I have only tested with 10 so far ] using the radio function
microbit chopping the message up to create a scrolling message affect with micro:bits positioned in a line.
The gateway microbit runs a python app called 'gate_scroll_rx.py'
The 'display micro:bits' a second app called 'node_scroll_showx.py

The gateway micro:bit is linked to a RaspberryPi via a USB connection. So far I have
included a 4 of basic demo apps for the Raspberry Pi end 
- A simple program to display a user inputted string,  [gateway1.py]
- A clock demo [gatewaytime_date.py]
- A Tweepy application which will scroll any messages with a specific prefix. [tweepy8a_microbitxx.py]
- A basic GUI that allows you to scroll / show strings or display time in a range of formats [scroll_GUIx.pyw]

An x in the s/w name indicates a rev number which is likely to change in the future.

Do to  
- clean up raspberry pi s/w
- buy more micro:bits
- build a dedicated Pi / micro:bit box

You can find a detailed write up of the project on my block https://meanderingpi.wordpress.com/2017/09/16/bbc-microbit-scrolling-display/
