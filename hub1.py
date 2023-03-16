import cv2
#import dlib
#import numpy as np

#model_detector1 = dlib.simple_object_detector("det_squares1.svm") # путь к детектору
#cam = cv2.VideoCapture(0)

key = 1
ESCAPE = 27
while key != ESCAPE:
    #ret, frame = cam.read()
    frame = cv2.imread("C:\Users\uraka\PycharmProjects\NTO_hub\hub1.py")
    frame_viz = frame.copy()

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(10)
    #frame_viz = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes1 = model_detector1(frame)
    print(boxes1)
    for box in boxes1:
        # Пороги:
        # red: minb - 0, maxb - 59, ming - 29, maxg - 255, minr - 16, maxr - 255 (0, 29, 16), (59, 255, 255)
        # green: minb - 0, maxb - 88, ming - 137, maxg - 255, minr - 0, maxr - 255 (0, 120, 0), (88, 255, 255)
        # blue: minb - 91, maxb - 255, ming - 95, maxg - 195, minr - 178, maxr - 255 (91, 95, 178), (255, 195, 255)
        # white: minb - 0, maxb - 87, ming - 0, maxg - 34, minr - 180, maxr - 255
        # every color is seen: (0, 0, 123), (255, 255, 255)

        (x, y, xb, yb) = [box.left(), box.top(), box.right(), box.bottom()]
        cv2.rectangle(frame_viz, (x, y), (xb, yb), (0, 0, 255), 2)
        cv2.imshow("Frame", frame_viz)
        square = frame_viz[y:yb, x:xb]
        # Проверка на ориентацию
        kernel = np.ones((5, 5), "uint8")

        vert = square[:, (square.shape[0] // 4) * 3:]
        hsv_vert = cv2.cvtColor(vert, cv2.COLOR_BGR2HSV)
        mask_vert = cv2.erode(cv2.inRange(hsv_vert, (0, 0, 100), (255, 255, 255)), kernel, iterations=7)
        cv2.imshow("mask_vert", mask_vert)

        hor = square[(square.shape[1] // 4) * 3:, :]
        hsv_hor = cv2.cvtColor(hor, cv2.COLOR_BGR2HSV)
        mask_hor = cv2.erode(cv2.inRange(hsv_hor, (0, 0, 100), (255, 255, 255)), kernel, iterations=7)
        cv2.imshow("mask_hor", mask_hor)
        print(np.sum(mask_vert), np.sum(mask_hor), "SUMS")
        if np.sum(mask_vert) < 10000 and np.sum(mask_hor) < 10000:
            M = cv2.getRotationMatrix2D((square.shape[1] / 2, square.shape[0] / 2), 180, 1)
            square = cv2.warpAffine(square, M, (square.shape[1], square.shape[0]))
        elif np.sum(mask_vert) < 10000 and np.sum(mask_hor) > 10000:
            M = cv2.getRotationMatrix2D((square.shape[1] / 2, square.shape[0] / 2), 90, 1)
            square = cv2.warpAffine(square, M, (square.shape[1], square.shape[0]))
        elif np.sum(mask_vert) > 10000 and np.sum(mask_hor) < 10000:
            M = cv2.getRotationMatrix2D((square.shape[1] / 2, square.shape[0] / 2), -90, 1)
            square = cv2.warpAffine(square, M, (square.shape[1], square.shape[0]))
        cv2.imshow("square", square)

        # number from left to right
        first = square[:(square.shape[1] // 4) * 3, square.shape[0] // 4: (square.shape[0] // 4) * 2]
        second = square[:(square.shape[1] // 4) * 3, (square.shape[0] // 4) * 2: (square.shape[0] // 4) * 3]
        third = square[:(square.shape[1] // 4) * 3, (square.shape[0] // 4) * 3:]

        # for first
        #hsv1 = cv2.cvtColor(first, cv2.COLOR_BGR2HSV)
        hsv1 = cv2.cvtColor(square, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(hsv1, (0, 29, 16), (59, 255, 255))
        cv2.imshow("FOR RED", mask1)

        # for second
        hsv2 = cv2.cvtColor(second, cv2.COLOR_BGR2HSV)
        mask2 = cv2.inRange(hsv2, (0, 29, 16), (59, 255, 255))

        # for third
        hsv3 = cv2.cvtColor(third, cv2.COLOR_BGR2HSV)
        mask3 = cv2.inRange(hsv3, (0, 120, 0), (88, 255, 255))
        cv2.imshow("THIRD", mask3)

        print(np.sum(mask1), np.sum(mask2), np.sum(mask3))
        if np.sum(mask1) > 200000 and np.sum(mask2) > 200000 and np.sum(mask3) > 200000:
            print("YES")
            # actions of hub...
    key = cv2.waitKey(10)
cv2.destroyAllWindows()
cam.release()