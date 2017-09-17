# microbit Scrolling Display application 3 of 3 application  - GUI  DISPLAY VERSION
# David Saul 2017 @david_ms, www.meanderingpi.wordpress.com
# Inspired by and utilising code by David Whale [@whaleygeek] 
# Available under MIT License via github.com/DavidMS51

# This code is for the Raspberry Pi - with is communicating with a
# gateway micro:bit connected via a USB port


# requires microbit module in same directory as this applicaion

# see www.meanderingpi.wordpress.com for setup details

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import microbit
import Tkinter

import time
from time import sleep
import datetime
from datetime import datetime

from multiprocessing import Process

ck = False

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

def clock(type):
    global ck
    count = 0
    temp_sec = "00"
    	
    while True:
#	print 'ck',ck
	hour = datetime.now().strftime('%I')
        min =datetime.now().strftime('%M')
        sec = datetime.now().strftime('%S')
        day = datetime.now().strftime('%a')
        h24 = datetime.now().strftime('%H')

        if int(hour)<10:
        	hour = ' '+hour[1:2]

        if int(h24)>=12:
                ap = 'p'
        else:
                ap = 'a'


        if int(sec) %2 ==1:
                col=':'
        else:
                col=' '

        if sec != temp_sec:
                temp_sec = sec
		if type == 1:
	                process_outgoing('1'+h24+col+min)
		elif type ==2:
	                process_outgoing('1'+h24+":"+min+":"+sec)
		elif type ==3:
	                process_outgoing('1'+hour+col+min+ap+" "+day)
#                print (hour+col+min+col+sec+ap+" "+day)
        sleep(.5)

    p.terminate()



class simpleapp_tk(Tkinter.Tk):


    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
#	global ck
 #       global p
        self.grid()

        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter message text here.")
	self.geometry("500x50")

        button1 = Tkinter.Button(self,text=u"Scroll",
                                command=self.OnButton1Click)
        button1.grid(column=1,row=0)

	button2 = Tkinter.Button(self,text=u"Show ", command=self.OnButton2Click)
#	button2 = Tkinter.Button(self,text=u"Show ", command=self.create_window)
        button2.grid(column=2,row=0)

	button3 = Tkinter.Button(self,text=u"Clock ",
                                command=self.OnButton3Click)
        button3.grid(column=3,row=0)


        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVariable,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=1,columnspan=4,sticky='EW')
        self.labelVariable.set(u"Waiting for first message !")

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())       
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
	self.protocol("WM_DELETE_WINDOW", self.on_closing)


    def OnButton1Click(self):
	global p
	global ck
	global t
	
	try:
		t.destroy()
		p.terminate()
		p.join()
		ck = False
	except:
		pass

        self.labelVariable.set( "Scrolling - "+ self.entryVariable.get())
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
	process_outgoing('2'+self.entryVariable.get())

    def OnButton2Click(self):
        global p
        global ck
	global t 

	try:
                t.destroy()
                p.terminate()
                p.join()
                ck = False
        except:
                pass

        self.labelVariable.set( "Showing - "+self.entryVariable.get())
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
	process_outgoing('1'+self.entryVariable.get())

    def create_window(self):
	global v
	global t
        v = Tkinter.IntVar()
	t = Tkinter.Toplevel(self)
	t.wm_title("Clock")
	l= Tkinter.Label(t,text = "Chose a clock display option")
	l.pack(side="top", fill='both', expand=True, padx=20)

	Tkinter.Radiobutton(t,text="HH:MM",padx=20,variable=v,value=1,command=self.sel).pack(anchor="w")
	Tkinter.Radiobutton(t,text="HH:MM:SS",padx=20,variable=v,value=2,command=self.sel).pack(anchor="w")
	Tkinter.Radiobutton(t,text="HH:MMp DDD",padx=20,variable=v,value=3,command=self.sel).pack(anchor="w")

    def sel(self):
	global p
	global t
	t.destroy()
	p=Process(target = clock, args = (v.get(),))
        p.start()


    def OnButton3Click(self):
        self.labelVariable.set( "Showing - Clock")
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
	global v
	global ck
	global p
	global t
#	print "CK",ck
	if ck == False:
		ck = True
		self.create_window()
	else:
		try:
			p.terminate()
			p.join()
		except:
			pass
		
		t.destroy()
		ck = False
			

    def OnPressEnter(self,event):
        self.labelVariable.set( self.entryVariable.get()+" (You pressed ENTER)" )
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def on_closing(self):
	global p 
	try:
		p.terminate()
		p.join()
		self.destroy()
        except:
		self.destroy()


if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('Micro:bit Scroll Display')
    app.mainloop()
    
