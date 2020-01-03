#!/usr/bin/python3
"""This implements a graphical countdown timer

Copyright 2017 A. Ottenheimer - use of this code requires this comment to
be kept and aknowledgement sent to the author.
License: GPL 3. See LICENSE file.
"""


import time
from tkinter import Tk, Label, Canvas, Button
import sys
import getopt


class Countdowntimer:
    """Countdowntimer Class"""
    def __init__(self, sys_args):
        self.args = sys_args  #pass args to Class variable
        self.timeleft = 0  #Not seconds left, could be microtime left
        self.running = True

        self.root_window = Tk()
        self.root_window.title("Countdown Timer")

        self.clock_features = self.setup_args()

        self.set_start_seconds()

        self.setup_topwindow()
        self.runclock()

        self.root_window.mainloop()

        print(self.clock_features)
        #print(self.clock_features['dict_time'])
        #print(self.clock_features['dict_time']['minutes'])
        print("Program Exited Ok")

    def setup_labels(self):
        """set the labels for the clock
        """
        top_label = int(self.timeleft/3600)*60
        #in python int() always rounds down
        self.widget_dict['widget_0'].config(text=top_label)
        self.widget_dict['widget_15'].config(text=top_label+15)
        self.widget_dict['widget_30'].config(text=top_label+30)
        self.widget_dict['widget_45'].config(text=top_label+45)

    def print_m(self):
        """print minutes remaining
        """
        if self.clock_features['quiet'] == 0: #if not quiet
            print("Minutes Remaining =" + str(round(self.timeleft/60, 0)))

    def runclock(self):
        """Run the countdown clock
        """
        arr_coord = (0, 0, self.clock_features['x_size'], self.clock_features['y_size'])
        start_seconds = self.timeleft
        last_seconds_left = round(self.timeleft, 0)
        percent_left = self.timeleft/3600
        extent_degrees_left = 360 * percent_left
        #elapsedtime = 0
        starttime = time.time()

        #not >= 0 because we don't want @0 to execute
        while self.timeleft > 0 and self.running:
            elapsedtime = time.time() - starttime
            self.timeleft = start_seconds - elapsedtime
            seconds_left = round(self.timeleft, 0)
            self.setup_labels()

            #percent red can be > 100% but it is normalized to 360 deg as an extent
            if (self.timeleft > 3599) and (seconds_left%3600 == 0):
                percent_left = self.timeleft/3600
                self.setup_labels()
                self.print_m()
                self.root_window.after(1000)
            elif (self.timeleft > 300) and (seconds_left%300 == 0):
                percent_left = self.timeleft/3600
                self.print_m()
                self.root_window.after(1000)
            elif 60 <= self.timeleft < 301 and seconds_left%60 == 0:
                percent_left = self.timeleft/3600
                self.print_m()
                self.root_window.after(1000)
            elif 20 <= self.timeleft <= 60:
                percent_left = self.timeleft/60
                if self.clock_features['quiet'] == 0 and last_seconds_left != seconds_left\
                                                and seconds_left%5 == 0:
                    print("Seconds remaining =" + str(seconds_left))
                self.root_window.after(100)
            elif self.timeleft < 20:
                percent_left = self.timeleft/60
                if self.clock_features['quiet'] == 0 and last_seconds_left != seconds_left:
                    print("Seconds remaining =" + str(seconds_left))
                self.root_window.after(50)
            else:
                percent_left = self.timeleft/3600
                self.root_window.after(1000)

            extent_degrees_left = 360 * percent_left
            self.widget_dict['widget_c'].create_oval(arr_coord, fill="white")
            self.widget_dict['widget_c'].create_arc(arr_coord,
                                                    start=90,
                                                    extent=-extent_degrees_left,
                                                    fill=self.clock_features['time_left_color'])

            self.root_window.update()
            last_seconds_left = seconds_left

        if self.clock_features['terminal_beep'] == 1:
            for _ in range(1, 10):
                print('\a')
                time.sleep(1)

        #at t=0 set to an all white circle
        if self.timeleft <= 0:
            self.widget_dict['widget_c'].create_oval(arr_coord, fill="white")
            self.root_window.update()
            self.on_closing()

    def setup_topwindow(self):
        """setup the timer window
        Starts at row=3 (top of clock) and goes to row=5(bottom of clock)"""
        self.root_window.wm_attributes("-topmost", 1)
        self.root_window.title("Graphical Countdown Timer!!!")

        print("SELFARGS=", self.args)
        widget_0 = Label(self.root_window, text="0")
        widget_0.grid(row=4, column=1)
        widget_15 = Label(self.root_window, text="15")
        widget_15.grid(row=5, column=2)
        widget_30 = Label(self.root_window, text="30")
        widget_30.grid(row=6, column=1)
        widget_45 = Label(self.root_window, text="45")
        widget_45.grid(row=5, column=0, sticky="e")
        widget_c = Canvas(self.root_window,
                          height=self.clock_features['y_size'],
                          width=self.clock_features['x_size'])
        widget_c.grid(row=5, column=1)
        #add buttons/fields interface for changing times, start/stop
        widget_buttons = Button(self.root_window, text="Restart", command=lambda: quit)
        widget_buttons.grid(row=7, column=0)
        widget_buttons = Button(self.root_window, text="Pause", command=lambda: quit)
        widget_buttons.grid(row=7, column=1)
        widget_buttons = Button(self.root_window, text="Adj. Time", command=lambda: quit)
        widget_buttons.grid(row=7, column=3)

        widget_c.create_oval(0, 0, self.clock_features['x_size'],
                             self.clock_features['y_size'], fill="white", tag="base")
        self.widget_dict = {"widget_0": widget_0,
                            "widget_15": widget_15,
                            "widget_30": widget_30,
                            "widget_45": widget_45,
                            "widget_c": widget_c}

    def setup_args(self):
        """Setup parameters from command line"""
        #setup the defaults
        quiet = 0
        terminal_beep = 0
        dict_time = {'seconds': 0, 'minutes': 0, 'hours': 0}
        int_xsize = int_ysize = 0
        time_left_color = "red"
        #If need args uncomment below and replace _ with args
        #args = []
        opts = []
        try:
            opts, _ = getopt.getopt(self.args,
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
                int_xsize = self.setup_size(arg)
            elif opt in ("-y", "--ysize"):
                int_ysize = self.setup_size(arg)
            elif opt in ("-c", "--color"):
                time_left_color = arg
            elif opt in ("-t", "--terminal_beep"):
                terminal_beep = 1
            elif opt in ("-q", "--quiet"):
                quiet = 1

        if int_ysize == 0 and int_xsize != 0:
            int_ysize = int_xsize

        if int_xsize == 0 and int_ysize != 0:
            int_xsize = int_ysize

        int_ysize = self.default_size_check(int_ysize)
        int_xsize = self.default_size_check(int_xsize)

        #Debugging
        #for opt, arg in opts:
        #    print(opt, arg)

        return {'x_size': int_xsize, 'y_size': int_ysize,\
                'quiet': quiet, 'terminal_beep': terminal_beep,\
                'time_left_color': time_left_color,\
                'dict_time': dict_time}

    def default_size_check(self, int_size):
        """setup Default window size if size not set"""
        if self.args == "" or int_size <= 0:
            int_size = 200
        return int_size

    def setup_size(self, size_arg):
        """Setup size of window for program"""
        if size_arg == '%':
            width_px = .5 * self.root_window.winfo_screenwidth()
            int_size = int(width_px)
        else:
            int_size = int(size_arg)
        return int_size

    def set_start_seconds(self):
        """Convert start time parameters to seconds"""
        if self.clock_features['dict_time']['hours'] == 0 and \
           self.clock_features['dict_time']['minutes'] == 0 and \
           self.clock_features['dict_time']['seconds'] == 0:
            self.clock_features['dict_time']['minutes'] = 15
        self.timeleft = self.clock_features['dict_time']['hours']*3600 + \
                        self.clock_features['dict_time']['minutes']*60 + \
                        self.clock_features['dict_time']['seconds']


    def on_closing(self):
        """End the program gracefully if user clicks the X"""
        self.root_window.eval('::ttk::CancelRepeat')
        self.root_window.quit()
        self.root_window.destroy()

if __name__ == "__main__":
    INSTA = Countdowntimer(sys.argv[1:])
    print("Program Ended Successfully")
