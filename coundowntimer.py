#!/usr/bin/python
"""This implements a graphical countdown timer"""

import time
#import threading
from Tkinter import Tk, Label, Canvas
#If add buttons do this
#from Tkinter import Button, Entry
#import tkMessageBox
import sys
import getopt

def runclock(this_topwindow, this_canvas, arr_coord, start_time_seconds):
    """Run the countdown clock
    if add buttons later the might need to import threading and use t=ThreadClass?
    """
    timeleft = start_time_seconds
    percent_red = timeleft/3600
    extent_degrees_red = 360 * percent_red
    elapsedtime = 0
    starttime = round(time.time(), 2)

    while timeleft > 0: #not >= 0 because we don't want @0 to execute
        percent_red = timeleft/3600
        extent_degrees_red = 360 * percent_red
        elapsedtime = time.time() - starttime
        timeleft = round(start_time_seconds - elapsedtime, 0)
        if (timeleft > 300) and (timeleft%300 == 0):
            print "Minutes Remaining =", round(timeleft/60, 0)
        elif timeleft < 301 and timeleft%60 == 0:
            print "Minutes Remaining =", round(timeleft/60, 0)
        elif timeleft < 20:
            print "Seconds remaining =", timeleft
        this_canvas.create_oval(arr_coord, fill="white")
        this_canvas.create_arc(arr_coord, start=90, extent=-extent_degrees_red, fill="red")
        this_topwindow.after(1000)
        this_topwindow.update()

    #at t=0 set to an all white circle
    this_canvas.create_oval(arr_coord, fill="white")
    this_topwindow.update()

def setuptopwindow(self, int_xsize, int_ysize):
    """setup the timer window"""
    self.wm_attributes("-topmost", 1)
    self.title("Graphical Countdown Timer")

    # canvas for to display visualisation of percentage of time elapsed
    widget_0 = Label(self, text="0")
    widget_0.grid(row=4, column=1)
    widget_15 = Label(self, text="15")
    widget_15.grid(row=5, column=2)
    widget_30 = Label(self, text="30")
    widget_30.grid(row=6, column=1)
    widget_45 = Label(self, text="45")
    widget_45.grid(row=5, column=0, sticky="e")
    widget_c = Canvas(self, height=int_ysize, width=int_xsize)
    widget_c.grid(row=5, column=1)

    #todo: add buttons/fields interface for changing times, start/stop
    '''
    widget_label = Label(self, text="Break time:")
    widget_label.grid(row=0)

    string_delay = StringVar(master=self, value="1")
    widget_delay = Entry(self, width=3, textvariable=string_delay)
    widget_delay.grid(row=0, column=1)

    widget_label1 = Label(self, text="Sprint time:")
    widget_label1.grid(row=1)

    string_minutes = StringVar(master=self, value=float_minutes)
    widget_time_minutes = Entry(self, width=3, textvariable=string_minutes)
    widget_time_minutes.grid(row=1, column=1)

    widget_label2 = Label(self, text="No of loops:")
    widget_label2.grid(row=2)

    string_iterations = StringVar(master=self, value="3")
    widget_time1 = Entry(self, width=3, textvariable=string_iterations)
    widget_time1.grid(row=2, column=1)

    widget_button = Button(self, text="Start", command=lambda: starttimer())
    #widget_button = Button(self, text="Start", command=cdt_draw_timer_circle(self, 100))
    widget_button.grid(row=3)
    '''
    widget_c.create_oval(0, 0, int_xsize, int_ysize, fill="white", tag="base")

    return widget_c

def main(argv):
    """main run the stuff"""
    #setup the defaults
    float_seconds = 0
    float_minutes = 15
    float_hours = 0
    int_xsize = 200
    int_ysize = 200
    args = []
    opts = []
    try:
        opts, args = getopt.getopt(argv,
                                   "h:m:s:x:y:",
                                   ["hours=", "minutes=", "seconds=",
                                    "xsize=", "ysize="]
                                  )
    except getopt.GetoptError:
        print "Usage:\n countdowntimer.py [-h <#>] [--hours=<#>] "
        print "[-m <#>] [--minutes <#>] [-s <#>] [--seconds <#>]\n"
        print "[-x <xwidth>] [-y <yheight>]"
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--hours"):
            float_hours = float(arg)
        elif opt in ("-m", "--minutes"):
            float_minutes = float(arg)
        elif opt in ("-s", "--seconds"):
            float_seconds = float(arg)
        elif opt in ("-x", "--xsize"):
            int_xsize = int(arg)
        elif opt in ("-y", "--ysize"):
            int_ysize = int(arg)

    #debugging prints
    #print "H/M/S={0}/{1}/{2}".format(float_hours, float_minutes, float_seconds)
    #print "ARGS={0}".format(args)

    topwindow = Tk()
    widget_canvas = setuptopwindow(topwindow, int_xsize, int_ysize)
    arr_coord = 0, 0, int_xsize, int_ysize

    #Todo: move this into threaded function
    #def X...., obj_thread = threading.Thread(target=X)

    #The clock shows only red up to 60 minutes. But supports times > 60 minutes
    start_time_seconds = float_hours*3600 + float_minutes*60 + float_seconds
    runclock(topwindow, widget_canvas, arr_coord, start_time_seconds)

    topwindow.destroy()
    topwindow.mainloop()

if __name__ == "__main__":
    main(sys.argv[1:])
