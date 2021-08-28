import tkinter as tk  # 使用Tkinter前需要先导入
from PIL import Image, ImageTk

# 第1步，实例化object，建立窗口window
window = tk.Tk()

# 第2步，给窗口的可视化起名字
window.title('My Window')

# 第3步，设定窗口的大小(长 * 宽)
# window.geometry('500x300')  # 这里的乘是小x

# 第4步，在图形界面上创建 500 * 200 大小的画布并放置各种元素
canvas = tk.Canvas(window, bg='green', height=800, width=800)
# 说明图片位置，并导入图片到画布上
image_file = ImageTk.PhotoImage(Image.open('/Users/bobo/Downloads/UVXyjTJKlRgvfzO.jpg'))  # 图片位置（相对路径，与.py文件同一文件夹下，也可以用绝对路径，需要给定图片具体绝对路径）
canvas.create_image(0, 0, anchor='nw', image=image_file)  # 图片锚定点（n图片顶端的中间点位置）放在画布（250,0）坐标处
canvas.pack()


# 第6步，触发函数，用来一定指定图形
def moveit():
    canvas.move(rect, 2, 2)  # 移动正方形rect（也可以改成其他图形名字用以移动一起图形、元素），按每次（x=2, y=2）步长进行移动


# 第5步，定义一个按钮用来移动指定图形的在画布上的位置
b = tk.Button(window, text='move item', command=moveit).pack()

# 第7步，主窗口循环显示
window.mainloop()
