import cv2
import dlib
import numpy as np

model_detector1 = dlib.simple_object_detector("det_squares1.svm") # путь к детектору
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
        #print(box.shape)
        (x, y, xb, yb) = [box.left(), box.top(), box.right(), box.bottom()]
        cv2.rectangle(frame_viz, (x, y), (xb, yb), (0, 0, 255), 2)
        cv2.imshow("Frame", frame_viz)
        square = frame_viz[y:yb, x:xb]
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
        print("Show square")
        cv2.imshow("Square", square)


        first = square[0:square.shape[1] // 3, :]
        second = square[square.shape[1] // 3: (square.shape[1] // 3) * 2, :]
        third = square[(square.shape[1] // 3) * 2:, :]

        # for first
        hsv1 = cv2.cvtColor(first, cv2.COLOR_BGR2HSV)
        mask1_b = cv2.inRange(hsv1, (84, 58, 174), (134, 255, 255))
        mask1_g = cv2.inRange(hsv1, (43, 95, 129), (127, 255, 183))
        mask1_r = cv2.inRange(hsv1, (0, 132, 201), (255, 255, 255))
        mask1_w = cv2.inRange(hsv1, (0, 0, 180), (87, 34, 255))

        # for second
        hsv2 = cv2.cvtColor(second, cv2.COLOR_BGR2HSV)
        mask2_b = cv2.inRange(hsv2, (84, 58, 174), (134, 255, 255))
        mask2_g = cv2.inRange(hsv2, (43, 95, 129), (127, 255, 183))
        mask2_r = cv2.inRange(hsv2, (0, 132, 201), (255, 255, 255))
        mask2_w = cv2.inRange(hsv2, (0, 0, 180), (87, 34, 255))

        # for third
        hsv3 = cv2.cvtColor(third, cv2.COLOR_BGR2HSV)
        mask3_b = cv2.inRange(hsv3, (84, 58, 174), (134, 255, 255))
        mask3_g = cv2.inRange(hsv3, (43, 95, 129), (127, 255, 183))
        mask3_r = cv2.inRange(hsv3, (0, 132, 201), (255, 255, 255))
        # third white
        mask3_w = cv2.inRange(hsv3, (0, 0, 180), (87, 34, 255))
        cv2.imshow("White3", mask3_w)
        print(np.sum(mask3_w), "WHITE")
        print(np.sum(mask1_g), "-", np.sum(mask1_r), np.sum(mask1_b), "GREEN1")
        print(np.sum(mask2_g), "-", np.sum(mask2_r), np.sum(mask2_b), "GREEN2")
        print(np.sum(mask3_g), "-", np.sum(mask3_r), np.sum(mask3_b), "GREEN3")
        print(np.sum([mask1_b == mask2_b]), "EQUALS")

        # Случай 1 - ровно 2 одинаковых полосы
        '''if ((np.sum([mask1_r == mask2_r]) > 50000 and np.sum([mask1_r == mask3_r]) < 50000 and np.sum([mask2_r == mask3_r] < 50000)) or\
                (np.sum([mask2_r == mask3_r]) > 50000 and np.sum([mask1_r == mask2_r]) < 50000 and np.sum([mask1_r == mask3_r]) < 50000)) or \
                ((np.sum([mask1_b == mask2_b]) > 50000 and np.sum([mask1_b == mask3_b]) < 50000 and np.sum(
                    [mask2_b == mask3_b] < 50000)) or \
                 (np.sum([mask2_b == mask3_b]) > 50000 and np.sum([mask1_b == mask2_b]) < 50000 and np.sum(
                     [mask1_b == mask3_b]) < 50000)) or \
                ((np.sum([mask1_g == mask2_g]) > 50000 and np.sum([mask1_g == mask3_g]) < 50000 and np.sum(
                    [mask2_g == mask3_g] < 50000)) or \
                 (np.sum([mask2_g == mask3_g]) > 50000 and np.sum([mask1_g == mask2_g]) < 50000 and np.sum(
                     [mask1_g == mask3_g]) < 50000)) or \
                ((np.sum([mask1_w == mask2_w]) > 50000 and np.sum([mask1_w == mask3_w]) < 50000 and np.sum(
                    [mask2_w == mask3_w] < 50000)) or \
                 (np.sum([mask2_w == mask3_w]) > 50000 and np.sum([mask1_w == mask2_w]) < 50000 and np.sum(
                     [mask1_w == mask3_w]) < 50000)):'''
        choose1 = [np.sum(mask1_r), np.sum(mask1_g), np.sum(mask1_b)]
        choose2 = [np.sum(mask2_r), np.sum(mask2_g), np.sum(mask2_b)]
        choose3 = [np.sum(mask3_r), np.sum(mask3_g), np.sum(mask3_b)]
        print(choose1.index(max(choose1)), choose2.index(max(choose2)))
        if (choose1.index(max(choose1)) == choose2.index(max(choose2)) and choose1.index(max(choose1)) != choose3.index(max(choose3))) or \
                (choose2.index(max(choose2)) == choose3.index(max(choose3)) and choose1.index(
                    max(choose1)) != choose3.index(max(choose3))) or \
                (choose1.index(max(choose1)) == choose3.index(max(choose3)) and choose1.index(
                    max(choose1)) != choose2.index(max(choose2))):
            # hub actions -> 1
            print("To 1")
        elif np.sum(mask3_w) > 250000:
            # hub actions -> 2
            print("To 2")
        elif ((np.sum(mask1_g) < np.sum(mask1_r) or np.sum(mask1_g) < np.sum(mask1_b)) and\
                (np.sum(mask2_g) < np.sum(mask2_r) or np.sum(mask2_g) < np.sum(mask2_b)) and\
                (np.sum(mask3_g) < np.sum(mask3_r) or np.sum(mask3_g) < np.sum(mask3_b))):
            # hub actions -> 3
            print("To 3")
        else:
            # hub actions -> to copter
            print("To copter")
    key = cv2.waitKey(10)
cv2.destroyAllWindows()
cam.release()