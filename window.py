import win32process
import wmi
import win32gui


c = wmi.WMI()

def get_app_path(exe,hwnd=win32gui.GetForegroundWindow()):
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        for p in c.query('SELECT ExecutablePath FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
            exe = p.ExecutablePath
            break
    except:
        return None
    else:
        return exe


def get_app_name(exe,hwnd = win32gui.GetForegroundWindow()):
    try:
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        for p in c.query('SELECT Name FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
            exe = p.Name
            break
    except:
        return None
    else:
        return exe


def get_window_title(hwnd= win32gui.GetForegroundWindow()):
    return win32gui.GetWindowText(hwnd)