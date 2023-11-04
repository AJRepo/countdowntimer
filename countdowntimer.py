#!/usr/bin/python3
"""This implements a graphical countdown timer

Copyright 2017 A. Ottenheimer - use of this code requires this comment to
be kept and aknowledgement sent to the author.
License: GPL 3. See LICENSE file.
"""

import time
import tkinter as tk
from tkinter import Tk, Label, Canvas, Button, Entry, Frame, StringVar
import sys
import getopt

# pylint: disable=too-many-instance-attributes
class Countdowntimer:
    """Countdowntimer Class"""
    def __init__(self, sys_args):
        self.args = sys_args  #pass args to Class variable
        self.seconds_left = 0  #Could be fractions of a second
        self.running = True

        self.root_window = Tk()
        self.root_window.title("Countdown Timer")
        self.root_window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.clock_features = self.setup_args()

        self.set_start_seconds()

        self.setup_topwindow()

        self.clock_coord = (0, 0, self.clock_features['x_size'], self.clock_features['y_size'])

        #time left as text

        self.root_window.update()

        #self.root_window.update()

        #Setup Clock pre-running of timer
        self.setup_labels()

        #Run the countdown timer and display
        self.runclock()

        #Don't call self.root_window calls if in exiting mode
        if self.running and not self.clock_features['exiting']:
            self.root_window.wait_window()
            self.root_window.mainloop()

        if self.clock_features['terminal_beep'] == 1:
            for _ in range(1, 5):
                print('\a')
                self.tksleep(1)
        #print(self.clock_features)
        #print(self.clock_features['dict_time'])
        #print(self.clock_features['dict_time']['minutes'])
        #print("Program Exited Ok")

    def display_time(self):
        """Display current time"""
        now = time.strftime('%H:%M:%S %p')
        self.current_time.config(text=now)
        self.current_time.after(1000,self.display_time)


    def setup_labels(self):
        """set the labels for the clock
        """
        #if self.running and self.widget_dict['widget_0'].winfo_exists():
        #if self.running and not self.clock_features['exiting']:
        top_label = int(self.seconds_left/3600)*60
        #in python int() always rounds down
        self.widget_dict['widget_0'].config(text=top_label)
        self.widget_dict['widget_15'].config(text=top_label+15)
        self.widget_dict['widget_30'].config(text=top_label+30)
        self.widget_dict['widget_45'].config(text=top_label+45)
        #self.widget_dict['widget_center_time'].config(top_label)


    def print_m(self):
        """print minutes remaining
        """
        print("Time Remaining = About " + str(round(self.seconds_left/60, 0)) + " minutes       ",
               end='\r')

    def runclock(self):
        """Run the countdown clock
        """
        last_seconds_left = round(self.seconds_left, 0)
        last_time = time.time()

        #not >= 0 because we don't want @0 to execute
        while self.seconds_left > 0 and not self.clock_features['exiting']:
            if self.running:
                this_time = time.time()
                self.seconds_left = self.seconds_left - (this_time - last_time)
                rounded_seconds_left = round(self.seconds_left, 0)

                #draw clock functions
                if self.clock_features['console_only'] is not True:
                    self.draw_clock()

                if self.clock_features['quiet'] == 0:
                    self.console_print_time(rounded_seconds_left, last_seconds_left)

                if self.clock_features['display_numeric']:
                    self.gui_print_time(rounded_seconds_left)

                self.sleep_time(rounded_seconds_left)

                last_seconds_left = rounded_seconds_left
                last_time = this_time
                #print("DEBUG 10: Seconds remaining =" + str(rounded_seconds_left))
            else:
                #print("DEBUG 20: remaining =" + str(rounded_seconds_left))
                self.root_window.update()
                self.tksleep(.001)
                this_time = last_time = time.time()


    def draw_clock(self):
        """draw the clock """
        self.setup_labels()

        self.draw_time_left()

        self.root_window.update()
        #at t=0 set to an all clock_bg_color circle
        if self.seconds_left <= 0:
            self.widget_dict['widget_c'].create_oval(self.clock_coord,
                                                     fill=self.clock_features['clock_bg_color'])
            self.root_window.update()
            self.on_closing()

    def draw_time_left(self):
        """draw the countdown clock wedge"""
        if self.seconds_left > 3599:
            this_clock_bg_color = "orange"
        else:
            this_clock_bg_color = self.clock_features['clock_bg_color']

        #set before sleep
        fraction_left = self.fraction_left()
        self.draw_pie(fraction_left, this_clock_bg_color)

        #Don't use self.root_window.after(miliseconds) as we want to draw and THEN wait
        self.root_window.update()

    def console_print_time(self, rounded_seconds_left, last_seconds_left):
        """Print to terminal depending on how much time is remaining"""
        if self.seconds_left > 305 and (5*round(rounded_seconds_left/5))%3600 <= 0:
            #print every hour
            self.print_m()
        elif ((self.seconds_left > 300) and (rounded_seconds_left%300 == 0)):
            #print every five min
            self.print_m()
        elif ((self.seconds_left > 300) and (rounded_seconds_left%60 == 0) and \
               self.clock_features['term_ppm'] ==1):
            #print every min if promoted
            self.print_m()
        elif 60 <= self.seconds_left < 301 and rounded_seconds_left%60 == 0:
            #print every min under 5 min
            self.print_m()
        elif 5 <= self.seconds_left <= 60:
            #print every 5 seconds for 5 < t < 60
            if last_seconds_left != rounded_seconds_left and rounded_seconds_left%5 == 0:
                print("Time remaining = " + str(rounded_seconds_left) + " seconds      ", end='\r')
        elif self.seconds_left < 5:
            #print every second under 5 seconds
            if last_seconds_left != rounded_seconds_left:
                print("Time remaining = " + str(rounded_seconds_left) + " seconds      ", end='\r')

    def gui_print_time(self, rounded_seconds_left):
        """Print to gui the time left"""
        sec=StringVar(value=f'{rounded_seconds_left%60:02.0f}')
        xmid = self.clock_features['x_size']/2
        ymid = self.clock_features['y_size']/2

        #print seconds
        Entry(self.root_window, textvariable=sec,
              width=2, bg="#fff", fg="#000",
              font="arial 25", bd=0).place(x=xmid+50,y=ymid+30)

        #print mins int() to round down
        mins=StringVar(value=f'{(int(rounded_seconds_left/60))%60:02.0f}')
        mins.set=("00")
        Entry(self.root_window, textvariable=mins,
              width=2, bg="#fff", fg="#000", font="arial 25", bd=0).place(x=xmid,y=ymid+30)

        #print hrs, test different way to place
        hrs=StringVar(value=f'{(int(rounded_seconds_left/3600))%24:02.0f}')
        widget_hr = Entry(self.root_window, text="11", textvariable=hrs,
              width=2, bg="#fff", fg="#000", font="arial 25", bd=0)
        widget_hr.place(x=xmid-50,y=ymid+30)

    def tksleep(self, seconds):
        """Emulating self.tksleep(seconds)"""
        mili_seconds = int(seconds*1000)
        #print(f"WAITING {ms} Miliseconds and {self.seconds_left}")
        #Don't call this after the window has been destroyed!

        #DEBUG
        #print(f"running={self.running}:exiting={self.clock_features['exiting']}")
        if (self.seconds_left > 0 and
            self.running is True and
            self.clock_features['exiting'] is False and
            self.root_window.winfo_exists() == 1):
            #DEBUG
            #print(f"exists={self.root_window.winfo_exists()}:running={self.running}")
            #print(f"exiting={self.clock_features['exiting']}")
            var = tk.IntVar(self.root_window)
            self.root_window.after(mili_seconds, lambda: var.set(1))
            self.root_window.wait_variable(var)

    def sleep_time(self, rounded_seconds_left):
        """Determine the time to slep based on how much time is remaining"""
        #percent red can be > 100% but it is normalized to 360 deg as an extent
        if self.seconds_left > 60 and self.clock_features['term_ppm'] == 1:
            self.tksleep(.25)
        elif self.seconds_left > 305 and not self.clock_features['display_numeric']:
            #update every 5 seconds if > 5 minutes 5 seconds to go
            if (5*round(rounded_seconds_left/5))%3600 <= 0:
                self.setup_labels()
            self.tksleep(5)
        # if display_numeric is true then sleep = 1 second
        elif 60 <= self.seconds_left <= 305 and not self.clock_features['display_numeric']:
            self.tksleep(2)
        elif 5 <= self.seconds_left <= 60:
            self.tksleep(.1)
        elif self.seconds_left < 5:
            self.tksleep(.05)
        else:
            #print("DEBUG2: Seconds remaining =" + str(self.seconds_left))
            self.tksleep(1)


    def fraction_left(self):
        """Calculate fraction of clock to display as time left"""
        if self.seconds_left <= 60:
            fraction_left = self.seconds_left/60
        else:
            fraction_left = (self.seconds_left%3600)/3600
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
        #self.widget_dict['widget_center_time'].text('asdfasdfa')

    def setup_topwindow(self):
        """setup the timer window
        Starts at row=3 (top of clock) and goes to row=5(bottom of clock)"""
        self.root_window.wm_attributes("-topmost", 1)
        self.root_window.title("Graphical Countdown Timer!!!")

        #print("SELFARGS=", self.args)

        widget_center_time = Label(self.root_window, text="TIME")
        widget_center_time.grid(row=5, column=1)
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
            self.frame_buttons = Frame(self.root_window)
            self.frame_buttons.grid(row=11, column=1, sticky='N', columnspan=3)
            widget_buttons = Button(self.frame_buttons, text="Restart",
                                    command=self.restart)
            widget_buttons.grid(row=1, column=0)
            widget_pause_button = Button(self.frame_buttons, text="Pause",
                                         command=self.toggle_running)
            widget_pause_button.grid(row=1, column=1, sticky='N')
            widget_buttons = Button(self.frame_buttons, text="Adj. Time", command=lambda: quit)
            widget_buttons.grid(row=1, column=2, sticky='N')
        else:
            widget_pause_button = 'DISABLED'

        self.widget_dict = {"widget_0": widget_0,
                            "widget_15": widget_15,
                            "widget_30": widget_30,
                            "widget_45": widget_45,
                            "widget_c": widget_c,
                            "widget_center_time": widget_center_time,
                            "widget_pause_button": widget_pause_button
                           }

        if self.clock_features['console_only'] is not True:
            widget_c.create_oval(0, 0, self.clock_features['x_size'],
                                 self.clock_features['y_size'],
                                 fill=self.clock_features['clock_bg_color'], tag="base")

        #display current time
        if self.clock_features['display_current_time']:
            self.current_time=Label(self.root_window,
                                    font=("arial",15,"bold"), text="", fg="#000", bg="#fff")
            #self.current_time.place(x=(self.clock_features['x_size']/2 - 40),y=40)
            self.current_time.grid(row=8, column=1)
            self.display_time()

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

    # pylint: disable=too-many-locals
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
        display_numeric = False
        display_current_time = False
        dict_time = {'seconds': 0, 'minutes': 0, 'hours': 0}
        int_x_size = int_y_size = 0
        time_left_color = "red"
        clock_bg_color = "white"
        #If need args uncomment below and replace _ with args
        #args = []
        opts = []
        try:
            opts, _ = getopt.getopt(self.args,
                                    "bdntqh:m:s:x:y:c:",
                                    ["terminal_beep", "quiet", "hours=", "minutes=", "seconds=",
                                     "buttons", "x_size=", "y_size=", "color=", "clock_bg_color=",
                                     "display_current_time", "console_only", "term_ppm",
                                     "display_numeric"]
                                   )
        except getopt.GetoptError:
            print("Usage:\n countdowntimer.py [Arguments]\n")
            print("Arguments:")
            print("  [--buttons] [-b] Add buttons to control timer")
            print("  [--console_only] Only use the console - not graphical timer")
            print("  [-c <color>] [--color=<color>] Color of time remaining")
            print("  [--clock_bg_color=<color>] Color not filled by timer when seconds <= 60")
            print("  [--help ]   Print Help (this message) and exit")
            print("  [-d ] [--display_numeric]")
            print("  [-h <#>] [--hours=<#>]")
            print("  [-m <#>] [--minutes=<#>]")
            print("  [-n ] [--display_currrent_time]")
            print("  [-s <#>] [--secondss=<#>]")
            print("  [-q or --quiet]  Do not print time left in terminal")
            print("  [--term_ppm] Print to terminal time left each minute")
            print("  [-t or --terminal_beep] Execute a beep at t=0")
            print("  [-x <#xwidth>] [--x_size=<#xwidth>]")
            print("  [-y <#yheight>] [--y_size=<#yheight>]")
            sys.exit(2)

        for opt, arg in opts:
            if opt in ("-h", "--hours"):
                dict_time['hours'] = float(arg)
            elif opt in ("-m", "--minutes"):
                dict_time['minutes'] = float(arg)
            elif opt in ("-s", "--seconds"):
                dict_time['seconds'] = float(arg)
            elif opt in ("-n", "--display_current_time"):
                display_current_time = True
            elif opt in ("-d", "--display_numeric"):
                display_numeric = True
            elif opt in ("-x", "--x_size"):
                int_x_size = self.setup_size(arg)
            elif opt in ("-y", "--y_size"):
                int_y_size = self.setup_size(arg)
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

        int_y_size = self.default_size_check(int_y_size, int_x_size)
        int_x_size = self.default_size_check(int_x_size, int_y_size)

        #Debugging
        #for opt, arg in opts:
        #    print(opt, arg)

        return {'x_size': int_x_size, 'y_size': int_y_size,\
                'quiet': quiet,\
                'term_ppm': term_ppm,\
                'terminal_beep': terminal_beep,\
                'time_left_color': time_left_color,\
                'clock_bg_color': clock_bg_color,\
                'buttons': buttons,\
                'dict_time': dict_time,\
                'exiting': False, \
                'console_only': console_only, \
                'display_numeric': display_numeric, \
                'display_current_time': display_current_time
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
        self.seconds_left = self.clock_features['dict_time']['hours']*3600 + \
                        self.clock_features['dict_time']['minutes']*60 + \
                        self.clock_features['dict_time']['seconds']


    def on_closing(self):
        """End the program gracefully if user clicks the X"""
        self.running = False
        self.clock_features['exiting'] = True
        self.root_window.update_idletasks()
        self.root_window.eval('::ttk::CancelRepeat')
        self.root_window.update_idletasks()
        self.root_window.quit()
        #don't use destroy
        #self.root_window.destroy()

if __name__ == "__main__":
    INSTA = Countdowntimer(sys.argv[1:])

    print("Program Ended Successfully.        ")
