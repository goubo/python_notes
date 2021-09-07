import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

text = "这是一段文字123abcd!<@,."
font_size = 35
font = ImageFont.truetype('SimHei.ttf', font_size)
print(font.getsize(text))
image = Image.new('RGBA', font.getsize(text))
draw = ImageDraw.Draw(image)
draw.text((0, 0), text, '#22aa33', font=font)

res_image = Image.open("/Users/bo/my/git/python_notes/opencv/ch01/test1.jpg")

image = image.rotate(40, expand=1)
res_image.paste(image, (50, 60), image)

img = np.array(res_image)
cv2.imshow("image", img)
image.save('test2.png', 'png')
cv2.waitKey(0)
