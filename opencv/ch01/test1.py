import cv2

img = cv2.imread('test1.jpg', 0)
cv2.imshow('image', img)
k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()  # wait for ESC key to exit
elif k == ord('s'):
    cv2.imwrite('save.png', img, [cv2.IMWRITE_PNG_COMPRESSION, 50])  # wait for 's' key to save and exit
cv2.destoryAllWindows()
