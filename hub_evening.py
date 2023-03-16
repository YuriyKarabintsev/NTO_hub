import cv2
#import dlib
#import numpy as np

#model_detector1 = dlib.simple_object_detector("det_squares1.svm") # путь к детектору
cam = cv2.VideoCapture(0)

key = 1
ESCAPE = 27
while key != ESCAPE:
    #ret, frame = cam.read()
    frame = cv2.imread(r"C:\Users\uraka\PycharmProjects\NTO_hub\h1.PNG")
    frame_viz = frame.copy()
    cv2.imshow("Out", frame_viz)
    hsv = cv2.cvtColor(frame_viz, cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(hsv, (0, 0, 0), (255, 255, 169))
    cv2.imshow("Mask", thresh)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea)
    cv2.drawContours(frame_viz, contours, -1, (0, 255, 0), 3, 2)
    for c in range(len(contours)):
        print(cv2.contourArea(contours[c]), "CONTOURS", len(contours))
        if cv2.contourArea(contours[c]) < 10:
            cv2.drawContours(frame_viz, contours[c], -1, (0, 255, 255), 2)
        cv2.imshow("Contours", frame_viz)

    key = cv2.waitKey(10)
cv2.destroyAllWindows()
cam.release()