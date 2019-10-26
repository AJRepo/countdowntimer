#!/usr/bin/python
"""This implements a graphical countdown timer

Copyright 2017 A. Ottenheimer - use of this code requires this comment to
be kept and aknowledgement sent to the author.
License: GPL 3. See LICENSE file.
"""

import time
#import threading
from Tkinter import Tk, Label, Canvas
#If add buttons do this
#from Tkinter import Button, Entry
#import tkMessageBox
import sys
import getopt

KILLWINDOW = 0
GLOBALWINDOW = Tk()

def setup_lables(this_widget_array, timeleft):
    """set the labels for the clock
    """
    top_label = int(timeleft/3600)*60
    #in python int() always rounds down
    this_widget_array[1].config(text=top_label)
    this_widget_array[2].config(text=top_label+15)
    this_widget_array[3].config(text=top_label+30)
    this_widget_array[4].config(text=top_label+45)

def print_m(this_seconds, quiet=0):
    """print minutes remaining
    """
    if quiet == 0: #if not quiet
        print("Minutes Remaining =" + str(round(this_seconds/60, 0)))

def runclock(this_topwindow, this_widget_array, arr_coord, start_time_seconds, quiet=0, terminal_beep=0):
    """Run the countdown clock
    if add buttons later the might need to import threading and use t=ThreadClass?
    """
    timeleft = start_time_seconds
    last_seconds_left = round(timeleft, 0)
    percent_left = timeleft/3600
    extent_degrees_left = 360 * percent_left
    elapsedtime = 0
    starttime = time.time()
    this_time_left_color = this_widget_array[5]

    #not >= 0 because we don't want @0 to execute
    #while timeleft > 0 and this_topwindow.winfo_exists():  #doesn't work
    #while timeleft > 0 and GLOBALWINDOW.winfo_exists():  #doesn't work
    while timeleft > 0 and KILLWINDOW == 0:
        elapsedtime = time.time() - starttime
        timeleft = start_time_seconds - elapsedtime
        seconds_left = round(timeleft, 0)
        setup_lables(this_widget_array, timeleft)

        #percent red can be > 100% but it is normalized to 360 deg as an extent
        if (timeleft > 3599) and (seconds_left%3600 == 0):
            percent_left = timeleft/3600
            setup_lables(this_widget_array, timeleft)
            print_m(timeleft, quiet)
            this_topwindow.after(1000)
        elif (timeleft > 300) and (seconds_left%300 == 0):
            percent_left = timeleft/3600
            print_m(timeleft, quiet)
            this_topwindow.after(1000)
        elif timeleft < 301 and seconds_left%60 == 0 and timeleft >= 60:
            percent_left = timeleft/3600
            print_m(timeleft, quiet)
            this_topwindow.after(1000)
        elif timeleft <= 60 and timeleft >= 20:
            percent_left = timeleft/60
            if quiet == 0 and last_seconds_left != seconds_left and seconds_left%5 == 0:
                print("Seconds remaining =" + str(seconds_left))
            this_topwindow.after(100)
        elif timeleft < 20:
            percent_left = timeleft/60
            if quiet == 0 and last_seconds_left != seconds_left:
                print("Seconds remaining =" + str(seconds_left))
            this_topwindow.after(50)
        else:
            percent_left = timeleft/3600
            this_topwindow.after(1000)

        extent_degrees_left = 360 * percent_left
        this_widget_array[0].create_oval(arr_coord, fill="white")
        this_widget_array[0].create_arc(arr_coord,
                                        start=90,
                                        extent=-extent_degrees_left,
                                        fill=this_time_left_color)

        this_topwindow.update()
        last_seconds_left = seconds_left

    if terminal_beep == 1:
        for _ in range(1,10):
            print('\a')
            time.sleep(1)

    #at t=0 set to an all white circle
    if KILLWINDOW == 0:
        this_widget_array[0].create_oval(arr_coord, fill="white")
        this_topwindow.update()

def setuptopwindow(self, int_xsize, int_ysize, time_left_color):
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

    return widget_c, widget_0, widget_15, widget_30, widget_45, time_left_color

def main(argv):
    """main run the stuff"""
    #setup the defaults
    quiet = 0
    terminal_beep = 0
    float_seconds = 0
    float_minutes = 0
    float_hours = 0
    int_xsize = 0
    int_ysize = 0
    time_left_color = "red"
    #If need args uncomment below and replace _ with args
    #args = []
    opts = []
    try:
        opts, _ = getopt.getopt(argv,
                                "tqh:m:s:x:y:c:",
                                ["terminal_beep", "quiet", "hours=", "minutes=", "seconds=",
                                 "xsize=", "ysize=", "color="]
                               )
    except getopt.GetoptError:
        print("Usage:\n countdowntimer.py [-h <#>] [--hours=<#>] ")
        print("[-m <#>] [--minutes <#>] [-s <#>] [--seconds <#>]\n")
        print("[-x <xwidth>] [-y <yheight>]\n")
        print("[-q or --quiet]\n")
        print("[-t or --terminal_beep]\n")
        print("[--color]\n")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--hours"):
            float_hours = float(arg)
        elif opt in ("-m", "--minutes"):
            float_minutes = float(arg)
        elif opt in ("-s", "--seconds"):
            float_seconds = float(arg)
        elif opt in ("-x", "--xsize"):
            if arg == '%':
                width_px = .5 * GLOBALWINDOW.winfo_screenwidth()
                int_xsize = int(width_px)
            else:
                int_xsize = int(arg)
        elif opt in ("-c", "--color"):
            time_left_color = arg
        elif opt in ("-y", "--ysize"):
            if arg == '%':
                height_px = .5 * GLOBALWINDOW.winfo_screenheight()
                int_ysize = int(height_px)
            else:
                int_ysize = int(arg)
        elif opt in ("-t", "--terminal_beep"):
            terminal_beep = 1
        elif opt in ("-q", "--quiet"):
            quiet = 1

    #Set xsize.
    if int_xsize == 0:
        if int_ysize != 0: 
            int_xsize = int_ysize
        else:
            int_xsize = 200
    #Set Ysize. In theory you'd never need fallback = 200 since xsize is set above
    if int_ysize == 0:
        if int_xsize != 0: 
            int_ysize = int_xsize
        else:
            int_ysize = 200
      


    if float_hours == 0 and float_minutes == 0 and float_seconds == 0:
        float_minutes = 15
    #debugging prints
    #print "H/M/S={0}/{1}/{2}".format(float_hours, float_minutes, float_seconds)
    #print "ARGS={0}".format(args)

    topwindow = GLOBALWINDOW
    #topwindow = Tk()
    #Note: on_closing() actually calls the function on_closing (no paren) defines it.
    #    so you can't pass arguments with WM_DELETE_WINDOW
    topwindow.protocol("WM_DELETE_WINDOW", on_closing)
    widget_array = []
    widget_array = setuptopwindow(topwindow, int_xsize, int_ysize, time_left_color)
    arr_coord = 0, 0, int_xsize, int_ysize

    #Todo: move this into threaded function
    #def X...., obj_thread = threading.Thread(target=X)

    #The clock shows only time left up to 60 minutes. But supports times > 60 minutes
    start_time_seconds = float_hours*3600 + float_minutes*60 + float_seconds
    runclock(topwindow, widget_array, arr_coord, start_time_seconds, quiet, terminal_beep)

    if KILLWINDOW == 0:
        topwindow.destroy()  #don't use .destroy() with WM_DELETE_WINDOW
    else:
        topwindow.quit()

    topwindow.mainloop()

def on_closing():
    """End the program gracefully if user clicks the X"""
    global KILLWINDOW
    KILLWINDOW = 1
    GLOBALWINDOW.eval('::ttk::CancelRepeat')
    GLOBALWINDOW.quit()
    GLOBALWINDOW.destroy()


if __name__ == "__main__":
    main(sys.argv[1:])
