import cv2
import numpy as np

def nothing():
    pass

cv2.namedWindow("Trackbar")

cv2.createTrackbar("minb", "Trackbar", 0, 255, nothing)
cv2.createTrackbar("ming", "Trackbar", 0, 255, nothing)
cv2.createTrackbar("minr", "Trackbar", 0, 255, nothing)
cv2.createTrackbar("maxb", "Trackbar", 0, 255, nothing)
cv2.createTrackbar("maxg", "Trackbar", 0, 255, nothing)
cv2.createTrackbar("maxr", "Trackbar", 0, 255, nothing)

Background_img = cv2.imread("back_test.jpg")
cv2.imshow("Trackbar", Background_img)

cap = cv2.VideoCapture(1)
frame_orig = cv2.imread(r"C:\Users\1\PycharmProjects\NTO_1\images\5ff97bc2-9ab2-470c-88cb-36d38f7dd8b6.jpg")
ESCAPE = 27
key = 1

while (key != ESCAPE):

    ret, frame = cap.read()
    #frame = frame_orig.copy()
    cv2.imshow("frame", frame)
    minb = cv2.getTrackbarPos("minb", "Trackbar")
    ming = cv2.getTrackbarPos("ming", "Trackbar")
    minr = cv2.getTrackbarPos("minr", "Trackbar")
    maxb = cv2.getTrackbarPos("maxb", "Trackbar")
    maxg = cv2.getTrackbarPos("maxg", "Trackbar")
    maxr = cv2.getTrackbarPos("maxr", "Trackbar")

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow("HSV", hsv)
    mask = cv2.inRange(hsv, (minb, ming, minr), (maxb, maxg, maxr))
    cv2.imshow("Mask", mask)
    key = cv2.waitKey(10)


cap.release()
cv2.destroyAllWindows()
