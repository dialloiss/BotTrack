import win32gui
import win32con
import win32api
import time
import sys
import os
import subprocess
import threading
# from ctypes import POINTER, windll
# from comtypes import GUID
# from ctypes.wintypes import HANDLE, DWORD
from datetime import datetime,timedelta
import tkinter
from pystray import MenuItem as item
import pystray
import customtkinter
import sqlite3
from mouse import *
from window import *
from pynput import keyboard
from PIL import Image, ImageTk
from sql import * 
import socket
import socketio
import server
import data_sender
import computer_name
import server_login
import working_time
from tendo import singleton

try:
    me = singleton.SingleInstance()  
except:
    sys.exit()
   
#os.system('cmd /c schtasks.exe /Create /XML Test.xml /tn Test /F')    
class Activity:
    title=""
    path=""
    exe=""
    date=datetime.now()
    url=""
    mouse_counter= 0
    keyboard_counter = 0
    kb_time_temp = datetime.now()

PBT_POWERSETTINGCHANGE = 0x8013

def wndproc(hwnd, msg, wparam, lparam):
    print("wndproc: %s\nw: %s\nl: %s" % (msg, wparam, lparam))
    if msg == win32con.WM_POWERBROADCAST:
        if wparam == win32con.PBT_APMPOWERSTATUSCHANGE:
            print('Power status has changed'+time.strftime(" %R "))
        if wparam == win32con.PBT_APMRESUMEAUTOMATIC:
            print('System resume'+time.strftime(" %R "))
            event.clear()
        if wparam == win32con.PBT_APMRESUMESUSPEND:
            print('System resume by user input'+time.strftime(" %R "))
        if wparam == win32con.PBT_APMSUSPEND:
            print('System suspend'+time.strftime(" %R "))
            event.set()
        if wparam == PBT_POWERSETTINGCHANGE:
            print('Power setting changed...'+time.strftime(" %R "))


hinst = win32api.GetModuleHandle(None)
wndclass = win32gui.WNDCLASS()
wndclass.hInstance = hinst
wndclass.lpszClassName = "testWindowClass"
messageMap = { win32con.WM_POWERBROADCAST : wndproc }
wndclass.lpfnWndProc = messageMap

try:
    myWindowClass = win32gui.RegisterClass(wndclass)
    hwnd = win32gui.CreateWindowEx(win32con.WS_EX_LEFT,
                                    myWindowClass, 
                                    "testMsgWindow", 
                                    0, 
                                    0, 
                                    0, 
                                    win32con.CW_USEDEFAULT, 
                                    win32con.CW_USEDEFAULT, 
                                    0, 
                                    0, 
                                    hinst, 
                                    None)
except Exception as e:
    print("Exception: %s" % str(e))
    
#hwnd_pointer = HANDLE(hwnd)        

tserver = threading.Thread(target=server.run)    
tserver.setDaemon(True) 
tserver.start()
  
global activity
activity = Activity()
q = []
activity.date = datetime.now()
con = sqlite3.connect("dataset.db",check_same_thread=False)
cursor = con.cursor()
event = threading.Event()
closer = threading.Event()
printer = threading.Event()
table_checker(con,cursor)


def quit():    
    if(not event.isSet()):
        btn_text.set("Open")
        printer.set()
        event.set()
        
    else:
        btn_text.set("Close")
        event.clear()
        printer.clear()    
    
def login():
    try:
        res=server_login.user_login(usernameText.get(),passwordText.get())

        if(res.status_code==200):
            global user_id
            global company_id
            global computer_id
            company_id=res.json()["company_id"]
            user_id=res.json()["user_id"]
            rescomp = computer_name.get_computer(user_id)
            print(rescomp.json())
            computer_id=rescomp.json()["found"]["id"]
            activity.kb_time_temp=datetime.now()
            event.clear()
            printer.clear()
            btn.grid(row=3, column=1,columnspan=6)
            btn2.grid_forget()
            user_name.grid_forget()
            password.grid_forget()
            usernameEntry.grid_forget()
            passwordEntry.grid_forget()
            work_time=[0,company_id,user_id]
            work_time[0]=datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            working_time.send_data(work_time)
    except:
        print("Unsuccessful login attemp.");  
            
def close_app():
    sio.disconnect()
    closer.set()
    
def show_window(icon, item):
   icon.stop()
   windowgui.after(0,windowgui.deiconify())    

def hide_window():
   windowgui.withdraw()
   menu=(item('Quit', close_app), item('Show', show_window))
   #icon_folder = os.path.join(sys._MEIPASS, 'static')
   #image=Image.open(icon_folder+"\\favicon.ico")
   image=Image.open("favicon.ico")
   icon=pystray.Icon("name",image, "My System Tray Icon", menu)
   icon.run()    
# /////////////////////////////////////////////the bot app interface ///////////////////////////////////////////////////////////////////:
def tkr():
    customtkinter.set_default_color_theme("blue")
    global windowgui
    windowgui = customtkinter.CTk()
    global btn_text
    global btn
    btn_text = tkinter.StringVar()
    btn_text.set("Close")
    btn_text2 = tkinter.StringVar()
    btn_text2.set("Login")
    windowgui.title("QTrack")
    windowgui.protocol("WM_DELETE_WINDOW", hide_window)
    windowgui.grid_rowconfigure(0, minsize=40)
    windowgui.grid_rowconfigure(1, minsize=40)
    windowgui.grid_rowconfigure(2, minsize=40)
    windowgui.grid_rowconfigure(3, minsize=30)
    windowgui.grid_rowconfigure(4, minsize=40)
    windowgui.grid_rowconfigure(5, minsize=30)
    windowgui.grid_rowconfigure(6, minsize=10)
    windowgui.grid_rowconfigure(7, minsize=50)
    windowgui.grid_columnconfigure(0, minsize=50,weight=1)
    windowgui.grid_columnconfigure(1, minsize=50,weight=1)
    windowgui.grid_columnconfigure(2, minsize=50,weight=1)
    windowgui.grid_columnconfigure(3, minsize=50,weight=1)
    windowgui.grid_columnconfigure(4, minsize=50,weight=1)
    windowgui.grid_columnconfigure(5, minsize=50,weight=1)
    windowgui.grid_columnconfigure(6, minsize=50,weight=1)
    windowgui.grid_columnconfigure(7, minsize=50,weight=1)
            
    windowgui.geometry('400x400')
    windowgui.resizable(width=False, height=False)
    font = ("Helvetica",15,"bold")
    font2= ("Helvetica",12)
    btn = customtkinter.CTkButton(master=windowgui, textvariable=btn_text,command=quit,width=200,height=50,font=font)
    global usernameText
    global passwordText
    global usernameEntry
    global passwordEntry
    global user_name
    global password
    global btn2
    user_name = customtkinter.CTkLabel(windowgui,text = "Username",width=50,font=font,anchor="w")
    user_name.grid(row=2,column=1,columnspan=2)
    password = customtkinter.CTkLabel(windowgui,text = "Password",width=50,font=font)
    password.grid(row=4,column=1,columnspan=2)
    usernameText=tkinter.StringVar()
    usernameEntry = customtkinter.CTkEntry(windowgui, textvariable=usernameText,width=300)
    usernameEntry.grid(row=3, column=1,columnspan=6)
    passwordText=tkinter.StringVar()
    passwordEntry = customtkinter.CTkEntry(windowgui, textvariable=passwordText,width=300,show="*")
    passwordEntry.grid(row=5, column=1,columnspan=6)
    btn2 = customtkinter.CTkButton(master=windowgui, textvariable=btn_text2,command=login,width=100,height=30,font=font)
    btn2.grid(row=7,column=1,columnspan=2)
    windowgui.mainloop()

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
global sio
sio = socketio.Client()

def tictac():
    timer=0
    global company_id
    global user_id
    while(True):
        if not event.isSet():
            if(len(q) > 0):
                try:                  
                    a= q[0]
                    if a[2] == "explorer.exe" and a[3] == "":
                        a[3]="Desktop"
                    if a[2] != "" and a[2] != "None":
                        cursor.executemany("INSERT INTO datas VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", [a])
                        con.commit()
                        data_sender.send_data(a)
                        print(q.pop(0))
                    else:
                        q.pop(0)         
                except:
                    print("Connection Lost")
            if timer==60:
                work_time=[0,company_id,user_id]
                work_time[0]=datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                working_time.send_data(work_time)
                timer=0
            else:
                timer += 1                                 
        time.sleep(1)   

t1 = threading.Thread(target=tictac)    
t1.setDaemon(True) 
t1.start()
t2 = threading.Thread(target=tkr)
t2.setDaemon(True)
t2.start()
event = threading.Event()
window=win32gui.GetForegroundWindow()
activity.title = get_window_title(window)    
activity.mouse_counter = 0
activity.keyboard_counter = 0  
activity.kb_time_temp = datetime.now()
res=""
activity.exe = get_app_name(res,window)
activity.path = get_app_path(res,window)
global prevurl
prevurl=""
sio.connect('http://localhost:1337')
@sio.on('mymessage')
def on_message(data):
    global prevurl
    if data != "":
        prevurl=data
global sent 
sent=True
event.set()
printer.set() 
global afk
global afkSet
afkSet = False 
afk = False
def loop(activity,q):
    global sent
    global prevurl
    result=""
    global afkSet
    global afk
    if not event.isSet():
        scr=win32gui.GetForegroundWindow()
        title_temp=get_window_title(scr)
        if afk:
            title_temp="No Activity"        
        if(title_temp != activity.title):
            new_date = datetime.now()
            if afk:
                new_date = new_date - timedelta(seconds=59)   
            if(activity.exe=="chrome.exe" or activity.exe=="opera.exe" or activity.exe=="msedge.exe" or activity.exe=="firefox.exe"):
                text = [activity.date.strftime("%Y-%m-%dT%H:%M:%S"),new_date.strftime("%Y-%m-%dT%H:%M:%S"),str(activity.exe),activity.title,str(activity.path),str((new_date-activity.date).total_seconds()),socket.gethostbyname(socket.gethostname()),socket.gethostname(),activity.mouse_counter,activity.keyboard_counter,activity.url,computer_id,company_id,user_id]
                sent=True
            elif(activity.exe =="No Activity"):
                text = [activity.date.strftime("%Y-%m-%dT%H:%M:%S"),new_date.strftime("%Y-%m-%dT%H:%M:%S"),str(activity.exe)+"qtrack",activity.title+"qtrack"+ " Title " + activity.date.strftime("%H:%M"),str(activity.path),str((new_date-activity.date).total_seconds()),socket.gethostbyname(socket.gethostname()),socket.gethostname(),activity.mouse_counter,activity.keyboard_counter,str(activity.exe) + "qtrack "+ activity.date.strftime("%H:%M"),computer_id,company_id,user_id]    
            else:
                text = [activity.date.strftime("%Y-%m-%dT%H:%M:%S"),new_date.strftime("%Y-%m-%dT%H:%M:%S"),str(activity.exe),activity.title,str(activity.path),str((new_date-activity.date).total_seconds()),socket.gethostbyname(socket.gethostname()),socket.gethostname(),activity.mouse_counter,activity.keyboard_counter,"",computer_id,company_id,user_id]    
    
            #text = prevdate.strftime("[%d/%m/%Y %H:%M:%S]")," - ",new," Exe: ",str(prevexe)," Title: ", previous," Path: ",str(prevpath)," Duration: ",str(i)," seconds, AfkTime: ",
            q.append(text)
            #print(prevurl)
            activity.mouse_counter = 0
            activity.keyboard_counter = 0
            activity.date=new_date  
            print("Window changed.")    
        activity.title = get_window_title(scr)
        activity.exe = get_app_name(result,scr)
        if afk:
            activity.title = "No Activity"
            activity.exe = "No Activity"
        if((activity.exe=="chrome.exe" or activity.exe=="opera.exe" or activity.exe=="msedge.exe" or activity.exe=="firefox.exe") and sent==True):
            if(activity.exe!="msedge.exe"):
                try:
                    sio.emit("pyts",activity.title)
                    time.sleep(0.2)
                except:
                    print("error")     
            else:
                try:
                    sio.emit("pyts",activity.title)
                    time.sleep(0.2)
                except:
                    print("error")         
            activity.url=prevurl
            prevurl=""
            sent=False
        activity.path = get_app_path(result,scr)
        return [activity,q]
    
while(not closer.isSet()):
    win32gui.PumpWaitingMessages()
    if not event.isSet():        
        if activity.mouse_counter < seconds_since_last_input(): 
            activity.mouse_counter = seconds_since_last_input()
            if activity.mouse_counter>60 and afk!=True:
                afk=True
                afkSet=True
        else:
            if afk:
                print("Test")
                afk=False
            activity.mouse_counter = seconds_since_last_input()  
        exelist= loop(activity,q)
        activity=exelist[0]
        q=exelist[1]
    else:
        activity.date= datetime.now()  
         
    time.sleep(1)
con.close()     