# mac
# py2applet --make-setup main.py
# python3 setup.py py2app -A
# windows
# pyinstaller -F -w main.py
import sys
import tkinter
import tkinter.messagebox
import webbrowser
from tkinter import Tk, Button, Entry, Label
from tkinter.ttk import Combobox

import requests

import flag

INIT_WINDOW = Tk()
flag_string = tkinter.StringVar()
user_name = tkinter.StringVar()

IEPath = "C:/Program Files/internet explorer/iexplore.exe"
webbrowser.register('IE', None, webbrowser.BackgroundBrowser(IEPath))

window: any


def show_flag():
    flag_string.set(flag.get_flag())


def copy_flag():
    INIT_WINDOW.clipboard_clear()
    INIT_WINDOW.clipboard_append(flag_string.get())
    window.destroy()


def show_get_flag_window():
    global window
    window = tkinter.Toplevel(INIT_WINDOW)
    window.geometry('+%d+%d' % (450, 450))
    window.title('获取序列号')
    show_flag()
    Entry(window, textvariable=flag_string, state='disabled').grid(row=1, column=2, padx=10, pady=5)
    Button(window, text='复制', padx=10, pady=5, command=copy_flag).grid(row=1, column=3, padx=10, pady=5)


def login():
    data = {"userName": user_name.get(), "flag": flag.get_flag()}
    try:
        res = requests.post("http://" + server_address_combobox.get(), json=data)
        if res.status_code == 200:
            if sys.platform == 'win32':
                webbrowser.get("IE").open_new(res.text)
            else:
                webbrowser.open_new(res.text)
        else:
            tkinter.messagebox.showerror(message=res.text)
    except:
        print("服务器连接失败")
        tkinter.messagebox.showerror(message="服务器连接失败")


if __name__ == '__main__':
    INIT_WINDOW.title("登录验证")
    INIT_WINDOW.geometry('+%d+%d' % (400, 400))

    Label(INIT_WINDOW, text="服务器地址:").grid(row=1, column=1, padx=10, pady=5)
    server_address_combobox = Combobox(INIT_WINDOW, values=["10.164.112.188:30001", "10.111.48.9:30001"])
    server_address_combobox.grid(row=1, column=2, padx=10, pady=5)
    Button(INIT_WINDOW, text='查看序列号', padx=10, pady=5, command=show_get_flag_window).grid(row=1, column=3, padx=10,
                                                                                          pady=5)
    Label(INIT_WINDOW, text="输入用户名").grid(row=2, column=1, padx=10, pady=5)
    Entry(INIT_WINDOW, textvariable=user_name).grid(row=2, column=2, padx=10, pady=5)
    Button(INIT_WINDOW, text='登录', padx=10, pady=5, command=login).grid(row=2, column=3, padx=10, pady=5)

    INIT_WINDOW.mainloop()
