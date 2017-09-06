# microbit Scrolling Display application 3 of 3 application  - TWITTER VERSION
# David Saul 2017 @david_ms, www.meanderingpi.wordpress.com
# Inspired by and utilising code by David Whale [@whaleygeek] 
# Available under MIT License via github.com/DavidMS51

# This code is for the Raspberry Pi - with is communicating with a gateway micro:bit connected via a USB port

# cut and paste of Christmas jumper code and @whaleygeek gateway app
# requires microbit module in same directory as this applicaion

# you need to add your own twitter consumer keys etc in the relevant place below

import microbit
import time
import os


import argparse
import urllib2

from time import sleep
import tweepy

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

import json

#this is currently not used, but allow trigger text to be set in command line
def parse_cmd_line():
	parser = argparse.ArgumentParser()
	parser.add_argument("echo")
	args = parser.parse_args()
	print(args.echo)
	return args.echo

def process_outgoing(msg):
  	# basic send to gateway microbit
    	# this message will be sent to the gateway micro:bit which will then
    	# broadcast it to all listening micro:bit devices as a scrolled message
	# The s/w will try to access the last used USB port, if this does not work
	# you may have to re-start the Pi
	# If no known USB port s/w will take you through a config exercise first
  
	microbit.send_message(msg)



global count		# records number of matting tweets recieved
global errcnt   	# used to manage back off process if err420 recieved
count = 0
errcnt = 0   

SEND_RATE = 1.0


#search phase  
sphase = "#m:bitrocks"


# Consumer keys and access tokens, used for OAuth
# add your consumer key data here  
consumer_key = 'aaaaaaaaaaaaaaaaaa'  
consumer_secret = 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'  
access_token = 'cccccccccccccccccccccccccccccccccc'  
access_token_secret = 'ddddddddddddddddddddddddddddddd'  

class StdOutListener(StreamListener):
    ''' Handles data received from the stream. '''

    def on_data(self, data):
	# Twitter returns data in JSON format - we need to decode it first
	decoded = json.loads(data)

        # flashes LED on Arduino
	global count
	count = count+1
	print count," from  ", 
	# sort out who tweet was from
	# Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
#        print '@%s' % (decoded['user']['screen_name'])
	print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore')),

	stint = decoded['text'].encode('ascii', 'ignore')

	# test to see if this is retweet, if so ignore 
	if ' RT ' in stint:
 		print " Retweet, ignore"
	else:
		print
		print
		#clean up tweet to lose any ref to external graphics and search phase
		stint_tmp1 = stint.split(sphase)
		stint_len = len(stint_tmp1)
		stint_tmp2 = stint_tmp1[stint_len-1].split('https')

		print 'orginal ',stint
		print 'trimed',stint_tmp2[0]
		process_outgoing('2'+stint_tmp2[0])
	return


# These are used to try and manage error code 420, you will see often if you restart the code a
# number of time
    def on_error(self, status_code):
	global errcnt
        print('Got an error with status code: ' + str(status_code))," total backoff factor = ", errcnt
	if status_code == 420:
#		tw_led.blink(background = True)
		#back off for a while
		print "waiting for ",(60*(2 ** errcnt))," Seconds"
		sleep(60*(2 ** errcnt))		# start with 60 second delay  then mult by  2 to power xx for further failures	
		errcnt=errcnt+1
		print "now re-trying"
#		tw_led.off()
        return True # To continue listening
 
    def on_timeout(self):
        print('Timeout...')
        return True # To continue listening

#main

#parse input string arguments to get trigger string
#sphase = parse_cmd_line()


print
print
print
print "Starting - search phase is "+sphase
print
listener = StdOutListener()
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
	
print "running"
stream = Stream(auth, listener)
stream.filter(track=[ sphase ])
