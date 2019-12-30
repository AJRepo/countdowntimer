#!/usr/bin/python3
"""This implements a graphical countdown timer

Copyright 2017 A. Ottenheimer - use of this code requires this comment to
be kept and aknowledgement sent to the author.
License: GPL 3. See LICENSE file.
"""

import time
#import threading
from tkinter import Tk, Label, Canvas, Button, Entry
#If add buttons do this
#from tkinter import Button, Entry
#import tkMessageBox
import sys
import getopt

KILLWINDOW = 0
GLOBALWINDOW = Tk()

def setup_labels(this_widget_array, timeleft):
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

def runclock(this_topwindow, this_widget_array, arr_coord, start_seconds, clock_features):
    """Run the countdown clock
    if add buttons later the might need to import threading and use t=ThreadClass?
    """
    timeleft = start_seconds
    last_seconds_left = round(timeleft, 0)
    percent_left = timeleft/3600
    extent_degrees_left = 360 * percent_left
    elapsedtime = 0
    starttime = time.time()

    #not >= 0 because we don't want @0 to execute
    #while timeleft > 0 and this_topwindow.winfo_exists():  #doesn't work
    #while timeleft > 0 and GLOBALWINDOW.winfo_exists():  #doesn't work
    while timeleft > 0 and KILLWINDOW == 0:
        elapsedtime = time.time() - starttime
        timeleft = start_seconds - elapsedtime
        seconds_left = round(timeleft, 0)
        setup_labels(this_widget_array, timeleft)

        #percent red can be > 100% but it is normalized to 360 deg as an extent
        if (timeleft > 3599) and (seconds_left%3600 == 0):
            percent_left = timeleft/3600
            setup_labels(this_widget_array, timeleft)
            print_m(timeleft, clock_features['quiet'])
            this_topwindow.after(1000)
        elif (timeleft > 300) and (seconds_left%300 == 0):
            percent_left = timeleft/3600
            print_m(timeleft, clock_features['quiet'])
            this_topwindow.after(1000)
        elif 60 <= timeleft < 301 and seconds_left%60 == 0:
            percent_left = timeleft/3600
            print_m(timeleft, clock_features['quiet'])
            this_topwindow.after(1000)
        elif 20 <= timeleft <= 60:
            percent_left = timeleft/60
            if clock_features['quiet'] == 0 and last_seconds_left != seconds_left\
                                            and seconds_left%5 == 0:
                print("Seconds remaining =" + str(seconds_left))
            this_topwindow.after(100)
        elif timeleft < 20:
            percent_left = timeleft/60
            if clock_features['quiet'] == 0 and last_seconds_left != seconds_left:
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
                                        fill=clock_features['time_left_color'])

        this_topwindow.update()
        last_seconds_left = seconds_left

    if clock_features['terminal_beep'] == 1:
        for _ in range(1, 10):
            print('\a')
            time.sleep(1)

    #at t=0 set to an all white circle
    if KILLWINDOW == 0:
        this_widget_array[0].create_oval(arr_coord, fill="white")
        this_topwindow.update()

def setup_topwindow(self, int_xsize, int_ysize, argv):
    """setup the timer window
    Starts at row=3 (top of clock) and goes to row=5(bottom of clock)"""
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

    #add buttons/fields interface for changing times, start/stop
    widget_buttons = Button(self, text="Restart", command=lambda: main(argv))
    widget_buttons.grid(row=7, column=0)
    widget_buttons = Button(self, text="Pause", command=lambda: main(argv))
    widget_buttons.grid(row=7, column=1)
    widget_buttons = Button(self, text="Adj. Time", command=lambda: main(argv))
    widget_buttons.grid(row=7, column=3)

    #widget_label = Label(self, text="Break time:")
    #widget_label.grid(row=3)

    '''
    string_delay = StringVar(master=self, value="1")
    widget_delay = Entry(self, width=3, textvariable=string_delay)
    widget_delay.grid(row=0, column=1)

    widget_label1 = Label(self, text="Sprint time:")
    widget_label1.grid(row=1)

    string_minutes = StringVar(master=self, value=dict_time['minutes'])
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

    return widget_c, widget_0, widget_15, widget_30, widget_45

def main(argv):
    """main run the stuff"""
    #setup the defaults
    quiet = 0
    terminal_beep = 0
    dict_time = {'seconds': 0, 'minutes': 0, 'hours': 0}
    int_xsize = 0
    int_ysize = 0
    time_left_color = "red"
    int_xsize, int_ysize, quiet, terminal_beep, time_left_color, dict_time = get_arguments(argv)
    #Set xsize.
    if int_xsize == 0 and int_ysize != 0:
        int_xsize = int_ysize
    elif int_xsize == 0:
        int_xsize = 200
    #Set Ysize. In theory you'd never need fallback = 200 since xsize is set above
    if int_ysize == 0 and int_xsize != 0:
        int_ysize = int_xsize
    elif int_ysize == 0:
        int_ysize = 200

    #debugging prints
    #print "ARGS={0}".format(args)

    topwindow = GLOBALWINDOW
    #topwindow = Tk()
    #Note: on_closing() actually calls the function on_closing (no paren) defines it.
    #    so you can't pass arguments with WM_DELETE_WINDOW
    topwindow.protocol("WM_DELETE_WINDOW", on_closing)

    #widget_array = []
    #widget_array = setup_top_window(topwindow, int_xsize, int_ysize, time_left_color)
    #arr_coord = 0, 0, int_xsize, int_ysize

    #Todo: move this into threaded function
    #def X...., obj_thread = threading.Thread(target=X)

    #The clock shows only time left up to 60 minutes. But supports times > 60 minutes

    runclock(topwindow,
             setup_topwindow(topwindow, int_xsize, int_ysize, argv), #widget_array
             (0, 0, int_xsize, int_ysize), #arr_cord
             set_start_seconds(dict_time), #start_seconds
             {'quiet': quiet, 'terminal_beep': terminal_beep, 'time_left_color': time_left_color}
             )

    if KILLWINDOW == 0:
        topwindow.destroy()  #don't use .destroy() with WM_DELETE_WINDOW
    else:
        topwindow.quit()

    topwindow.mainloop()

def get_arguments(argv):
    """Setup parameters from command line"""
    #setup the defaults
    quiet = 0
    terminal_beep = 0
    dict_time = {'seconds': 0, 'minutes': 0, 'hours': 0}
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
        print("Usage:\n countdowntimer.py [Arguments]\n")
        print("Arguments:")
        print("  [--color=<color>] [-c <color>]")
        print("  [--help ]   Print Help (this message) and exit")
        print("  [-h <#>] [--hours=<#>]")
        print("  [-m <#>] [--minutes=<#>]")
        print("  [-s <#>] [--secondss=<#>]")
        print("  [-q or --quiet]  Do not print time left in terminal")
        print("  [-t or --terminal_beep]")
        print("  [-x <#xwidth>] [--xsize=<#xwidth>]")
        print("  [-y <#yheight>] [--ysize=<#yheight>]")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--hours"):
            dict_time['hours'] = float(arg)
        elif opt in ("-m", "--minutes"):
            dict_time['minutes'] = float(arg)
        elif opt in ("-s", "--seconds"):
            dict_time['seconds'] = float(arg)
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

    return int_xsize, int_ysize, quiet, terminal_beep, time_left_color, dict_time

def set_start_seconds(dict_time):
    """Convert start time parameters to seconds"""
    if dict_time['hours'] == 0 and dict_time['minutes'] == 0 and dict_time['seconds'] == 0:
        dict_time['minutes'] = 15
    start_seconds = dict_time['hours']*3600 + dict_time['minutes']*60 + dict_time['seconds']
    return start_seconds

def on_closing():
    """End the program gracefully if user clicks the X"""
    global KILLWINDOW
    KILLWINDOW = 1
    GLOBALWINDOW.eval('::ttk::CancelRepeat')
    GLOBALWINDOW.quit()
    GLOBALWINDOW.destroy()


if __name__ == "__main__":
    main(sys.argv[1:])
