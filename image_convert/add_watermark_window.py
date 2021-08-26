import os
from tkinter import Label, Entry, StringVar, Button
from tkinter.filedialog import askopenfile, askopenfilename


def select_path():
    file = askopenfile(mode='r',
                       initialdir=os.path.split(os.path.realpath(__file__))[0])
    print(111)
    if file is not None:
        content = file.read()
        print(content)


def show(window):
    window.title('图片添加水印')
    # 获取屏幕 宽、高
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    # 计算 x, y 位置
    w = 300
    h = 200
    x = (ws / 2) - w
    y = (hs / 2) - h
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    path = StringVar()

    Label(window, text='选择图片').grid(row=0, column=0)
    Entry(window, textvariable=path).grid(row=0, column=1)
    Button(window, text='选择图片', command=select_path).grid(row=0, column=2)
