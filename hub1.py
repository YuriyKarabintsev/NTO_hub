import cv2
import dlib
import numpy as np

model_detector1 = dlib.simple_object_detector("det_squares.svm") # путь к детектору
cam = cv2.VideoCapture(0)

key = 1
ESCAPE = 27
while key != ESCAPE:
    ret, frame = cam.read()
    frame_viz = frame.copy()
    #frame_viz = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes1 = model_detector1(frame)
    #if not boxes1:
        #print("no")
    for box in boxes1:
        print(box.shape)
        (x, y, xb, yb) = [box.left(), box.top(), box.right(), box.bottom()]
        cv2.rectangle(frame_viz, (x, y), (xb, yb), (0, 0, 255), 2)
        cv2.imshow("Frame", frame_viz)
        square = frame_viz[x:xb, y:yb]
        # number from left to right
        first = square[0:square.shape[1] // 3, :]
        second = square[square.shape[1] // 3: (square.shape[1] // 3) * 2, :]
        third = square[(square.shape[1] // 3) * 2:, :]
        hsv = cv2.cvtColor(second, cv2.COLOR_BGR2HSV)

        # for first
        mask1 = cv2.inRange(hsv, (minb, ming, minr), (maxb, maxg, maxr))

        # for second
        hsv2 = cv2.cvtColor(second, cv2.COLOR_BGR2HSV)
        mask2 = cv2.inRange(hsv, (minb, ming, minr), (maxb, maxg, maxr))

        # for third
        hsv3 = cv2.cvtColor(second, cv2.COLOR_BGR2HSV)
        mask3 = cv2.inRange(hsv, (minb, ming, minr), (maxb, maxg, maxr))

        print(first.shape[0] * first.shape[1]) #to know the size of picture
        if np.sum(mask1, axis=0) + np.sum(mask2, axis=0) + np.sum(mask3, axis=0) > 50000:
            print("YES")
            # actions of hub...

    key = cv2.waitKey(10)
cv2.destroyAllWindows()
cam.release()