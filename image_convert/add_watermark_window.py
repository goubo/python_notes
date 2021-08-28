from tkinter import Label, StringVar, Button, N, Toplevel
import canvas_window

show_flag = False


def show(main_window):
    global show_flag
    window = Toplevel(main_window)
    show_flag = True
    window.title('图片添加水印')
    # 获取屏幕 宽、高ø
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    # 计算 x, y 位置
    w = 300
    h = 200
    x = (ws / 2) - w
    y = (hs / 2) - h
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    path = StringVar('')
    Label(window, text='选择图片:').grid(row=0, column=0)

    def select_path():
        # file = askopenfile(mode='r',
        #                    initialdir=os.path.split(os.path.realpath(__file__))[0])
        # if file is not None:
        #     content = file.read()
        #     print(content)

        path.set('/Users/bobo/Downloads/UVXyjTJKlRgvfzO.jpg')
        show_canvas_window(window, path.get())

    Button(window, text='选择图片', command=select_path).grid(row=0, column=1, sticky=N)
    Label(window, textvariable=path, ).grid(row=1, column=1, columnspan=3)

    def close():
        global show_flag
        show_flag = False
        canvas_window.show_flag = False
        window.destroy()

    window.protocol('WM_DELETE_WINDOW', close)

    return window


def show_canvas_window(window, path):
    if not canvas_window.show_flag:
        canvas_window.show(window)
        canvas_window.add_image(path)
