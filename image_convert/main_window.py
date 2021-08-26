from tkinter import Tk, Button, Toplevel

import add_watermark_window

INIT_WINDOW = Tk()
add_watermark_window_show = False


def show_add_watermark_button():
    global add_watermark_window_show
    print(add_watermark_window_show)
    if not add_watermark_window_show:
        add_watermark_window_show = True
        window = Toplevel(INIT_WINDOW)
        add_watermark_window.show(window)

        def close():
            global add_watermark_window_show
            add_watermark_window_show = False
            window.destroy()

        window.protocol('WM_DELETE_WINDOW', close)


def init(w=800, h=600):
    INIT_WINDOW.title("图形处理")
    # 获取屏幕 宽、高
    ws = INIT_WINDOW.winfo_screenwidth()
    hs = INIT_WINDOW.winfo_screenheight()
    # 计算 x, y 位置
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    INIT_WINDOW.geometry('%dx%d+%d+%d' % (w, h, x, y))
    Button(INIT_WINDOW, text='图片添加水印', padx=10, pady=5, command=show_add_watermark_button) \
        .grid(row=1, column=1, padx=10, pady=5)
    Button(INIT_WINDOW, text='pdf 转 image', padx=10, pady=5) \
        .grid(row=1, column=2, padx=10, pady=5)


def show(w=800, h=600):
    init(w, h)
    INIT_WINDOW.mainloop()
