import cv2
#import dlib
import numpy as np

#model_detector1 = dlib.simple_object_detector("det_squares1.svm") # путь к детектору
cam = cv2.VideoCapture(1)

key = 1
ESCAPE = 27
while key != ESCAPE:
    ret, frame = cam.read()
    frame_viz = frame.copy()

    cv2.imshow("Frame", frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv, (0, 0, 0), (255, 120, 58))
    #cv2.imshow("HSV", hsv)
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    #cv2.drawContours(frame, contours, -1, (255, 0, 0), 2, cv2.LINE_AA, hierarchy, 2)
    cv2.drawContours(frame, contours[1], -1, (255, 0, 0), 3)
    print(cv2.contourArea(contours[1]))
    for contour in contours:
        if 5200 <= cv2.contourArea(contour) <= 11100:
            print("OK", cv2.contourArea(contour))




    cv2.imshow("Contours", frame)








    key = cv2.waitKey(10)
cv2.destroyAllWindows()
cam.release()