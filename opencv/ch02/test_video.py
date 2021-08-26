import numpy as np
import cv2

cap = cv2.VideoCapture(0) #摄像头
while (True):
    # capture frame-by-frame
    ret, frame = cap.read()

    # our operation on the frame come here
    gray = cv2.cvtColor(frame, 1)

    # display the resulting frame
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # 按q键退出
        break
# when everything done , release the capture
cap.release()
cv2.destroyAllWindows()
