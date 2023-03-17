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

    #ret, frame = cap.read()
    frame = cv2.imread(r"C:\Users\uraka\PycharmProjects\NTO_hub\h3.PNG")#frame_orig.copy()
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
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea)
    frame_viz = frame.copy()
    for contour in range(len(contours)):
        print(cv2.contourArea(contours[contour]))
        if 500 <= cv2.contourArea(contours[contour]) <= 2500:
            print("OK")
            (x, y, w, h) = cv2.boundingRect(contours[contour])
            print(w, h)
            print(np.sum(contours[contour][int(h*0.7):, int(w*0.7):]), "CORNER 1")
            if (w / h) < 1.3 and (h / w) < 1.3 and w < 200 and h < 200:
                cv2.drawContours(frame_viz, contours[contour], -1, (255, 0, 0), 2)
                cv2.rectangle(frame_viz, (x, y), (x+w, y+h), (0, 0, 255), 2)
    #cv2.drawContours(frame_viz, contours, -1, (0, 255, 0), 0)
    cv2.imshow("Contours", frame_viz)
    key = cv2.waitKey(10)


cap.release()
cv2.destroyAllWindows()