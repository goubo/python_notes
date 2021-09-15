# 像素操作
import cv2

image = cv2.imread('test1.jpg', 1)
(b, g, r) = image[100, 100]
print(b, g, r)
for i in range(1, 100):
    image[10 + i, 100] = (255, 0, 0)
cv2.imshow('image', image)
cv2.waitKey(2000)
