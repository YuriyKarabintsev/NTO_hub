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
        '''first = square[0:square.shape[1] // 4, 0:square.shape[0] // 4]
        second = square[square.shape[1] // 4:, 0:square.shape[0] // 4]
        third = square[0:square.shape[0] // 4, square.shape[1] // 4:]
        fourth = square[square.shape[1] // 4:, square.shape[1] // 4:]

        #for first
        hsv1 = cv2.cvtColor(first, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv1, (minb, ming, minr), (maxb, maxg, maxr))

        # for second
        hsv2 = cv2.cvtColor(second, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv2, (minb, ming, minr), (maxb, maxg, maxr))

        # for third
        hsv3 = cv2.cvtColor(second, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv3, (minb, ming, minr), (maxb, maxg, maxr))

        # for fourth
        hsv4 = cv2.cvtColor(second, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv4, (minb, ming, minr), (maxb, maxg, maxr))'''


        first = square[0:square.shape[1] // 3, :]
        second = square[square.shape[1] // 3: (square.shape[1] // 3) * 2, :]
        third = square[(square.shape[1] // 3) * 2:, :]
        hsv = cv2.cvtColor(second, cv2.COLOR_BGR2HSV)
        # for first
        mask1 = cv2.inRange(hsv, (minb, ming, minr), (maxb, maxg, maxr))
        # first white
        mask1_w = cv2.inRange(hsv, (230, 230, 230), (255, 255, 255))

        # for second
        mask2 = cv2.inRange(hsv, (minb, ming, minr), (maxb, maxg, maxr))

        # for third
        mask3 = cv2.inRange(hsv, (minb, ming, minr), (maxb, maxg, maxr))

        if (np.sum([first == second]) > 50000) or (np.sum([second == third]) > 50000):
            # hub actions -> 1
        elif np.sum(mask1_w) > 30000:
            # hub actions -> 2
        else:
            # hub actions -> to copter
    key = cv2.waitKey(10)
cv2.destroyAllWindows()
cam.release()