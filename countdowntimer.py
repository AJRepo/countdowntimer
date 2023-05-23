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
        self.root_window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.clock_features = self.setup_args()

        self.set_start_seconds()

        self.setup_topwindow()

        self.clock_coord = (0, 0, self.clock_features['x_size'], self.clock_features['y_size'])

        #Setup Clock pre-running of timer
        self.setup_labels()

        #Run the countdown timer and display
        self.runclock()

        #don't need both mainloop() and while in runclock()
        #self.root_window.mainloop()

        if self.clock_features['terminal_beep'] == 1:
            for _ in range(1, 5):
                print('\a')
                time.sleep(1)
        #print(self.clock_features)
        #print(self.clock_features['dict_time'])
        #print(self.clock_features['dict_time']['minutes'])
        #print("Program Exited Ok")

    def setup_labels(self):
        """set the labels for the clock
        """
        #if self.running and self.widget_dict['widget_0'].winfo_exists():
        #if self.running and not self.clock_features['exiting']:
        top_label = int(self.timeleft/3600)*60
        #in python int() always rounds down
        self.widget_dict['widget_0'].config(text=top_label)
        self.widget_dict['widget_15'].config(text=top_label+15)
        self.widget_dict['widget_30'].config(text=top_label+30)
        self.widget_dict['widget_45'].config(text=top_label+45)

    def print_m(self):
        """print minutes remaining
        """
        print("Minutes Remaining =" + str(round(self.timeleft/60, 0)))

    def runclock(self):
        """Run the countdown clock
        """
        last_seconds_left = round(self.timeleft, 0)
        last_time = time.time()

        #not >= 0 because we don't want @0 to execute
        while self.timeleft > 0 and not self.clock_features['exiting']:
            if self.running:
                this_time = time.time()
                self.timeleft = self.timeleft - (this_time - last_time)
                seconds_left = round(self.timeleft, 0)

                #draw clock functions
                if self.clock_features['console_only'] is not True:
                    self.draw_clock()

                if self.clock_features['quiet'] == 0:
                    self.print_time(seconds_left, last_seconds_left)

                self.sleep_time(seconds_left)

                last_seconds_left = seconds_left
                last_time = this_time
                #print("DEBUG 10: Seconds remaining =" + str(seconds_left))
            else:
                #print("DEBUG 20: remaining =" + str(seconds_left))
                self.root_window.update()
                time.sleep(.001)
                this_time = last_time = time.time()


    def draw_clock(self):
        """draw the clock """
        self.setup_labels()

        self.draw_time_left()

        self.root_window.update()
        #at t=0 set to an all clock_bg_color circle
        if self.timeleft <= 0:
            self.widget_dict['widget_c'].create_oval(self.clock_coord,
                                                     fill=self.clock_features['clock_bg_color'])
            self.root_window.update()
            self.on_closing()

    def draw_time_left(self):
        """draw the countdown clock wedge"""
        if self.timeleft > 3599:
            this_clock_bg_color = "orange"
        else:
            this_clock_bg_color = self.clock_features['clock_bg_color']

        #set before sleep
        fraction_left = self.fraction_left()
        self.draw_pie(fraction_left, this_clock_bg_color)
        #Don't use self.root_window.after(miliseconds) as we want to draw and THEN wait
        self.root_window.update()

    def print_time(self, seconds_left, last_seconds_left):
        """Print to terminal depending on how much time is remaining"""
        if self.timeleft > 305 and (5*round(seconds_left/5))%3600 <= 0:
            #print every hour
            self.print_m()
        elif ((self.timeleft > 300) and (seconds_left%300 == 0)):
            #print every five min
            self.print_m()
        elif ((self.timeleft > 300) and (seconds_left%60 == 0) and \
               self.clock_features['term_ppm'] ==1):
            #print every min if promoted
            self.print_m()
        elif 60 <= self.timeleft < 301 and seconds_left%60 == 0:
            #print every min under 5 min
            self.print_m()
        elif 5 <= self.timeleft <= 60:
            #print every 5 seconds for 5 < t < 60
            if last_seconds_left != seconds_left and seconds_left%5 == 0:
                print("Seconds remaining =" + str(seconds_left))
        elif self.timeleft < 5:
            #print every second under 5 seconds
            if last_seconds_left != seconds_left:
                print("Seconds remaining =" + str(seconds_left))

    def sleep_time(self, seconds_left):
        """Determine the time to slep based on how much time is remaining"""
        #percent red can be > 100% but it is normalized to 360 deg as an extent
        if self.timeleft > 60 and self.clock_features['term_ppm'] == 1:
            time.sleep(1)
        elif self.timeleft > 305:
            #update every 5 seconds if > 5 minutes 5 seconds to go
            if (5*round(seconds_left/5))%3600 <= 0:
                self.setup_labels()
            time.sleep(5)
        elif 60 <= self.timeleft <= 305:
            time.sleep(2)
        elif 5 <= self.timeleft <= 60:
            time.sleep(.1)
        elif self.timeleft < 5:
            time.sleep(.05)
        else:
            #print("DEBUG2: Seconds remaining =" + str(self.timeleft))
            time.sleep(1)


    def fraction_left(self):
        """Calculate fraction of clock to display as time left"""
        if self.timeleft <= 60:
            fraction_left = self.timeleft/60
        else:
            fraction_left = (self.timeleft%3600)/3600
        return fraction_left

    def draw_pie(self, fraction_left, this_clock_bg_color):
        """draw the pie on the clock
        technically fraction_left in the clock could be autogenerated, but leavign as a var
        for general drawing"""
        arr_coord = (0, 0, self.clock_features['x_size'], self.clock_features['y_size'])
        extent_degrees_left = 360 * fraction_left
        self.widget_dict['widget_c'].create_oval(arr_coord,
                                                 fill=this_clock_bg_color)
        self.widget_dict['widget_c'].create_arc(arr_coord,
                                                start=90,
                                                extent=-extent_degrees_left,
                                                fill=self.clock_features['time_left_color'])

    def setup_topwindow(self):
        """setup the timer window
        Starts at row=3 (top of clock) and goes to row=5(bottom of clock)"""
        self.root_window.wm_attributes("-topmost", 1)
        self.root_window.title("Graphical Countdown Timer!!!")

        #print("SELFARGS=", self.args)
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
        if self.clock_features['buttons']:
            widget_buttons = Button(self.root_window, text="Restart",
                                    command=self.restart)
            widget_buttons.grid(row=7, column=0)
            widget_pause_button = Button(self.root_window, text="Pause",
                                         command=self.toggle_running)
            widget_pause_button.grid(row=7, column=1)
            widget_buttons = Button(self.root_window, text="Adj. Time", command=lambda: quit)
            widget_buttons.grid(row=7, column=3)
        else:
            widget_pause_button = 'DISABLED'

        self.widget_dict = {"widget_0": widget_0,
                            "widget_15": widget_15,
                            "widget_30": widget_30,
                            "widget_45": widget_45,
                            "widget_c": widget_c,
                            "widget_pause_button": widget_pause_button
                           }

        if self.clock_features['console_only'] is not True:
            widget_c.create_oval(0, 0, self.clock_features['x_size'],
                                 self.clock_features['y_size'],
                                 fill=self.clock_features['clock_bg_color'], tag="base")

    def restart(self):
        """Reset timeleft variable"""
        self.set_start_seconds()
        self.setup_topwindow()
        self.draw_time_left()

    def toggle_running(self):
        """Toggle self.running variable"""
        #self.widget_dict['widget_pause_button'].config(state="normal")
        if self.running:
            self.running = False
        else:
            self.running = True

    def setup_args(self):
        """Setup parameters from command line"""
        # There are that many command line options (branches, statements)
        #pylint: disable=too-many-branches
        #pylint: disable=too-many-statements
        #setup the defaults
        quiet = 0
        term_ppm = 0
        terminal_beep = 0
        buttons = False
        console_only = False
        dict_time = {'seconds': 0, 'minutes': 0, 'hours': 0}
        int_xsize = int_ysize = 0
        time_left_color = "red"
        clock_bg_color = "white"
        #If need args uncomment below and replace _ with args
        #args = []
        opts = []
        try:
            opts, _ = getopt.getopt(self.args,
                                    "btqh:m:s:x:y:c:",
                                    ["terminal_beep", "quiet", "hours=", "minutes=", "seconds=",
                                     "buttons", "xsize=", "ysize=", "color=", "clock_bg_color=",
                                     "console_only", "term_ppm"]
                                   )
        except getopt.GetoptError:
            print("Usage:\n countdowntimer.py [Arguments]\n")
            print("Arguments:")
            print("  [--buttons] [-b] Add buttons to control timer")
            print("  [--console_only] Only use the console - not graphical timer")
            print("  [--color=<color>] [-c <color>] Color of time remaining")
            print("  [--clock_bg_color=<color>] Color not filled by timer when seconds <= 60")
            print("  [--help ]   Print Help (this message) and exit")
            print("  [-h <#>] [--hours=<#>]")
            print("  [-m <#>] [--minutes=<#>]")
            print("  [-s <#>] [--secondss=<#>]")
            print("  [-q or --quiet]  Do not print time left in terminal")
            print("  [--term_ppm] Print to terminal time left each minute")
            print("  [-t or --terminal_beep] Execute a beep at t=0")
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
            elif opt == "--console_only":
                console_only = True
            elif opt in ("-c", "--color"):
                time_left_color = arg
            elif opt == "--clock_bg_color":
                clock_bg_color = arg
            elif opt in ("-t", "--terminal_beep"):
                terminal_beep = 1
            elif opt in ("--term_ppm"):
                term_ppm = 1
            elif opt in ("-q", "--quiet"):
                quiet = 1
            elif opt in ("-b", "--buttons"):
                buttons = True

        int_ysize = self.default_size_check(int_ysize, int_xsize)
        int_xsize = self.default_size_check(int_xsize, int_ysize)

        #Debugging
        #for opt, arg in opts:
        #    print(opt, arg)

        return {'x_size': int_xsize, 'y_size': int_ysize,\
                'quiet': quiet,\
                'term_ppm': term_ppm,\
                'terminal_beep': terminal_beep,\
                'time_left_color': time_left_color,\
                'clock_bg_color': clock_bg_color,\
                'buttons': buttons,\
                'dict_time': dict_time,\
                'exiting': False, \
                'console_only': console_only
               }

    def default_size_check(self, int_size, other_axis):
        """setup Default window size if size not set"""
        #
        if int_size <= 0 < other_axis:
            int_size = other_axis
        elif self.args == "" or int_size <= 0:
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
        self.running = False
        self.clock_features['exiting'] = True
        self.root_window.update_idletasks()
        self.root_window.eval('::ttk::CancelRepeat')
        self.root_window.quit()
        self.root_window.destroy()

if __name__ == "__main__":
    INSTA = Countdowntimer(sys.argv[1:])
    print("Program Ended Successfully")
