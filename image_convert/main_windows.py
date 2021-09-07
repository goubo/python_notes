from tkinter import Tk, Button

from image_convert import add_watermark_window

INIT_WINDOW = Tk()


def show_add_watermark_button_click():
    add_watermark_window.show(INIT_WINDOW)


def show(w=800, h=600):
    INIT_WINDOW.title("图形处理")
    ws = INIT_WINDOW.winfo_screenwidth()
    hs = INIT_WINDOW.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    INIT_WINDOW.geometry('%dx%d+%d+%d' % (w, h, x, y))
    Button(INIT_WINDOW, text='图片添加水印', padx=10, pady=5, command=show_add_watermark_button_click) \
        .grid(row=1, column=1, padx=10, pady=5)
    Button(INIT_WINDOW, text='pdf 转 image', padx=10, pady=5) \
        .grid(row=1, column=2, padx=10, pady=5)
    INIT_WINDOW.mainloop()
