import datetime
import json
import os
from tkinter import Toplevel, StringVar, Label, Button, Entry, N, Radiobutton, HORIZONTAL, Scale, IntVar, colorchooser
from tkinter.filedialog import askopenfilename

import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw
from numpy import array

import utils

show_flag = False
show_image = False
logo: Image
image: Image
image_res: Image

textVar: StringVar  # 文字
sticky: StringVar  # 位置
show_xy = [0, 0]  # 显示位置
rel_xy = array([0, 0])  # 相对偏移量
sticky_xy = [0, 0]  # 定位位置
fondSizeVal: IntVar  # 字号
rgbVal: StringVar  # 颜色
angleVal: IntVar  # 旋转角度x
alphaVal: IntVar  # 透明通道
path: StringVar
color_rgb = (70, 127, 161)

fond_size_scale: Scale
angle_scale: Scale
alpha_scale: Scale


def reset_config(*v):
    if 'image_res' not in globals().keys():
        return
    if not show_image:
        return
    global image, logo
    filename = utils.resource_path(os.path.join("res", "SimHei.ttf"))
    print(filename)
    font = ImageFont.truetype(filename, fondSizeVal.get())
    logo = Image.new('RGBA', font.getsize(textVar.get()))
    draw = ImageDraw.Draw(logo)
    test = color_rgb + (alphaVal.get(),)
    draw.text((0, 0), textVar.get(), fill=test, font=font)
    logo = logo.rotate(angleVal.get(), expand=1)
    image_copy = image_res.copy()
    image_copy.paste(logo, (show_xy[0], show_xy[1]), logo)
    image = np.array(image_copy)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imshow('预览', image)
    return


mouse_flag = False


def mouse_event(event, x, y, flags, param):
    if 'image_res' not in globals().keys() or 'logo' not in globals().keys():
        return
    global image, mouse_flag, rel_xy
    if event == 1:
        mouse_flag = True
    elif event == 4:
        mouse_flag = False
    if flags == 0 or not mouse_flag:  # 鼠标未点击
        return
    # 显示位置
    image_copy = image_res.copy()
    show_xy[0] = x - int(logo.size[0] / 2)
    show_xy[1] = y - int(logo.size[1] / 2)
    image_copy.paste(logo, (show_xy[0], show_xy[1]), logo)
    image = np.array(image_copy)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imshow('预览', image)
    # 计算偏移量
    rel_xy = array(show_xy) - array(sticky_xy)


def reset_offset():
    if 'image_res' not in globals().keys() or 'logo' not in globals().keys():
        return
    # 定位位置
    global show_xy
    x, y = utils.text_offset(image_res.size[0], image_res.size[1], logo.size[0], logo.size[1], sticky.get())
    sticky_xy[0] = x
    sticky_xy[1] = y
    show_xy = sticky_xy.copy()
    reset_config()
    return


def set_font_size(v):
    fondSizeVal.set(v)
    reset_config()


def set_angle(v):
    angleVal.set(v)
    reset_config()


def set_alpha(v):
    alphaVal.set(v)
    reset_config()


def show_canvas_window(image_path):
    global image, image_res, show_xy, show_image
    show_image = True
    cv2.destroyAllWindows()
    image_res = Image.open(image_path)
    image = np.array(image_res)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imshow('预览', image)
    cv2.moveWindow("预览", 400, 0)
    cv2.setMouseCallback('预览', mouse_event)
    reset_offset()
    show_xy = array(rel_xy) + array(sticky_xy)
    reset_config()
    return


def show(main_window):
    global show_flag, textVar, sticky, fondSizeVal, rgbVal, angleVal, color_rgb, alphaVal, path, fond_size_scale, \
        angle_scale, alpha_scale
    path = StringVar()
    textVar = StringVar()
    sticky = StringVar()
    rgbVal = StringVar()
    alphaVal = IntVar()
    alphaVal.set(200)
    rgbVal.set(','.join([str(value) for value in (color_rgb[2], color_rgb[1], color_rgb[0], alphaVal.get())]))
    sticky.set('nw')
    angleVal = IntVar()
    angleVal.set(0)
    fondSizeVal = IntVar()
    fondSizeVal.set(45)
    if show_flag:
        return
    show_flag = True
    window = Toplevel(main_window)
    window.title('图片添加水印')
    window.geometry('+0+0')

    def close():
        global show_flag, path, show_image
        show_flag = False
        show_image = False
        cv2.destroyAllWindows()
        window.destroy()

    window.protocol('WM_DELETE_WINDOW', close)

    Label(window, text='选择图片:').grid(row=0, column=0)

    def select_path():
        file_path = askopenfilename(title='Select the diagnostic instrument .jpeg file',
                                    filetypes=[('图片', ('.jpeg', '.png', '.jpg', '.gif'))])
        if file_path:
            path.set(file_path)
            show_canvas_window(path.get())

    Button(window, text='选择图片', command=select_path).grid(row=0, column=1, sticky=N, columnspan=3)
    Label(window, text='水印文字:').grid(row=2, column=0)
    e = Entry(window, textvariable=textVar)
    e.bind('<KeyRelease>', reset_config)
    e.grid(row=2, column=1, columnspan=3)

    Label(window, text='字号:').grid(row=3, column=0)
    fond_size_scale = Scale(window, orient=HORIZONTAL, from_=3, to=200, relief='flat', sliderrelief='flat', length=200,
                            command=set_font_size)
    fond_size_scale.set(fondSizeVal.get())
    fond_size_scale.grid(row=3, column=1, columnspan=3)

    Label(window, text='旋转:').grid(row=4, column=0)
    angle_scale = Scale(window, orient=HORIZONTAL, from_=0, to=360, relief='flat', sliderrelief='flat', length=200,
                        command=set_angle)
    angle_scale.grid(row=4, column=1, columnspan=3)

    def CallColor():
        color = colorchooser.askcolor()
        if color[0]:
            global color_rgb
            color_rgb = color[0]
            test = (color_rgb[2], color_rgb[1], color_rgb[0], alphaVal.get())
            rgbVal.set(','.join([str(value) for value in test]))
            reset_config()

    Label(window, text='颜色:').grid(row=5, column=0)
    Button(window, text="选择颜色", command=CallColor).grid(row=5, column=1)
    Label(window, textvariable=rgbVal).grid(row=5, column=2)

    Label(window, text='透明:').grid(row=6, column=0)
    alpha_scale = Scale(window, orient=HORIZONTAL, from_=0, to=255, relief='flat', sliderrelief='flat', length=200,
                        command=set_alpha)
    alpha_scale.grid(row=6, column=1, columnspan=3)
    alpha_scale.set(alphaVal.get())

    Label(window, text='位置:').grid(row=7, column=0)
    Radiobutton(window, text='左上', variable=sticky, value='nw', comman=reset_offset).grid(row=7, column=1)
    Radiobutton(window, text='中上', variable=sticky, value='n', comman=reset_offset).grid(row=7, column=2)
    Radiobutton(window, text='右上', variable=sticky, value='ne', comman=reset_offset).grid(row=7, column=3)
    Radiobutton(window, text='左中', variable=sticky, value='w', comman=reset_offset).grid(row=8, column=1)
    Radiobutton(window, text='中中', variable=sticky, value='center', comman=reset_offset).grid(row=8, column=2)
    Radiobutton(window, text='右中', variable=sticky, value='e', comman=reset_offset).grid(row=8, column=3)
    Radiobutton(window, text='左下', variable=sticky, value='sw', comman=reset_offset).grid(row=9, column=1)
    Radiobutton(window, text='中下', variable=sticky, value='s', comman=reset_offset).grid(row=9, column=2)
    Radiobutton(window, text='右下', variable=sticky, value='se', comman=reset_offset).grid(row=9, column=3)

    Button(window, text="导入水印", command=import_info).grid(row=10, column=2)
    Button(window, text="保存水印", command=save_info).grid(row=10, column=3)
    Button(window, text="保存图片", command=save_image).grid(row=11, column=3)


def print_info():
    print('水印文字', textVar.get())
    print('位置', sticky.get())
    print('绝对位置偏移量', rel_xy)
    print('定位位置位置', sticky_xy)
    print('字号', fondSizeVal.get())
    print('颜色', (color_rgb[2], color_rgb[1], color_rgb[0], alphaVal.get()))
    print('透明度', alphaVal.get())
    print('角度', angleVal.get())


def save_image():
    if not path.get():
        return
    path_ = os.path.splitext(path.get())
    global image
    save_path = path_[0] + '_watermark' + path_[1]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    Image.fromarray(image).save(save_path)


def save_info():
    desk = os.path.join(os.path.expanduser('~'), 'Desktop', datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + '.wark')
    info = {'textVar': textVar.get(), 'sticky': sticky.get(), 'rel_xy': rel_xy.tolist(),
            'fondSizeVal': fondSizeVal.get(),
            'color': color_rgb, 'angleVal': angleVal.get(), 'alphaVal': alphaVal.get()}
    f = open(desk, 'w')
    f.write(json.dumps(info))
    f.close()


def import_info():
    global rel_xy, color_rgb, show_xy
    file_path = askopenfilename(title='选择水印文件',
                                filetypes=[('wark', '*.wark')])
    if file_path:
        info = json.loads(open(file_path, 'r').read())
        textVar.set(info['textVar'])
        sticky.set(info['sticky'])
        fondSizeVal.set(info['fondSizeVal'])
        angleVal.set(info['angleVal'])
        alphaVal.set(info['alphaVal'])
        rel_xy = info['rel_xy']
        color_rgb = tuple(info['color'])
        fond_size_scale.set(info['fondSizeVal'])
        angle_scale.set(info['angleVal'])
        alpha_scale.set(info['alphaVal'])
        reset_offset()
        show_xy = array(rel_xy) + array(sticky_xy)
        reset_config()
