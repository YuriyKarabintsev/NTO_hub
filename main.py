import cv2
cam = cv2.VideoCapture(0)
ESCAPE = 27
key = 1
i = 1


print("Start")
while key != ESCAPE:
    print("works")
    ret, frame = cam.read()
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(10)
    if key == ord("f") or key == ord("F"):
        cv2.imwrite(r"C:\Users\1\PycharmProjects\cx1\images\\" + str(i) + ".jpg", frame)
        print("Foto made", i)
        i += 1