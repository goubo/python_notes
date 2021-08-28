from tkinter import Toplevel, Canvas, NW

from PIL import Image, ImageTk

show_flag = False
canvas = image = None


def show(main_window):
    global show_flag, canvas
    window = Toplevel(main_window)
    show_flag = True
    window.title('预览')
    canvas = Canvas(window, width=800, height=800, bg='white')
    canvas.grid(row=1, column=1)

    def close():
        global show_flag
        show_flag = False
        window.destroy()

    window.protocol('WM_DELETE_WINDOW', close)
    return window


def add_image(path):
    global image
    img_file = Image.open(path)
    w, h = img_file.size
    print(w, h)
    image = ImageTk.PhotoImage(img_file)
    canvas.create_image(0, 0, anchor='nw', image=image)
    return image
