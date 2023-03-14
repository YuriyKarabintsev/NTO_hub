import cv2
import os
import xml.etree.ElementTree as pars

import dlib

dir = r"C:/Users/1/PycharmProjects/cx1"
images = []
annots = [] # списки с координатами рамок, ограничивающих объекты
ImgNameList = os.listdir(dir + "/images/") # просмотр файлов в какой-либо папке
for FileName in ImgNameList:
    #print()
    image = cv2.imread(dir + "/images/" + FileName)
    #cv2.imshow("Image", image)
    #cv2.waitKey(0)
    OnlyFileName = FileName.split(".")[0]
    print(OnlyFileName)
    e = pars.parse(dir + "/annots/" + OnlyFileName + ".xml")
    print(dir + "/annots/" + OnlyFileName + ".xml")
    root = e.getroot()
    object = root.find("object")
    for object in root.findall("object"):
        print("OBJECT")
        object = object.find("bndbox")
        x = int(object.find("xmin").text)
        y = int(object.find("ymin").text)
        x2 = int(object.find("xmax").text)
        y2 = int(object.find("ymax").text)
        image_viz = image.copy()
        cv2.rectangle(image_viz, (x, y), (x2, y2), (0, 200, 0))
        #cv2.imshow("Image", image_viz)
        cv2.waitKey(0)
        #if ((x2 - x) / (y2 - y) > 0.3) and ((x2 - x) / (y2 - y) < 2):
        print((x2 - x) / (y2 - y))
        images.append(image)
        annots.append([dlib.rectangle(left=x, top=y, right=x2, bottom=y2)]) # перевод координат в структуру, подходящую для dlib

options = dlib.simple_object_detector_training_options() # настройки объекта детектора
options.be_verbose = True # настройка получения отладочной информации
detector = dlib.train_simple_object_detector(images, annots, options) # запуск детектора для тренировки
# images и annots должны быть одинаковой длины
detector.save("det_squares.svm")
print("Detector saved")

print(ImgNameList)