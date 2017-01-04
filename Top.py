
from PyQt5.QtWidgets import QApplication
import sys
import cv2


from UI import *

def mode1_camera():
    #Initial setup.
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0)
    winName = "Mode1"
    cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)
    bb_thres = 200#37
    thres = 14.5
    flag = False
    start = False
    count = 0  # duration
    myMessage = None

    while not start:
        color_img = cam.read()[1]
        gray = cv2.cvtColor(color_img, cv2.COLOR_RGB2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=10,  # 5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        for (x, y, w, h) in faces:
            if (w > bb_thres and h > bb_thres):
                print("Back!",w,h)
                if myMessage is None:
                    myMessage = MessageDialog('back')
            elif (w <= bb_thres and h <= bb_thres and count <= 10):
                count = count + 1
            elif (count > 10):
                print("start")
                if myMessage is not None:
                    myMessage.state = 'start'
                    myMessage.setPicture()



                start = True
            cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow(winName, cv2.resize(color_img,(640,480)))
        if cv2.waitKey(10)& 0xFF == ord('q'):
            break

    print("=============================================================================")
    # Buffer fill in .
    t = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)
    t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)

    while True:
        # Pushing back
        t_minus = t
        t = t_plus
        color_img = cam.read()[1]
        gray = cv2.cvtColor(color_img, cv2.COLOR_RGB2GRAY)
        t_plus = gray

        # Face detection
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=10,  # 5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Motion detection
        temp = diffImg(t_minus, t, t_plus)
        size = gray.shape

        for (x, y, w, h) in faces:
            index = x - w  # int(round(w/2))
            if (index <= 0):
                start_x = 0
            else:
                start_x = index

            index = x + 2 * w  # int(round(w/2))
            if (index > size[1]):
                end_x = size[1]
            else:
                end_x = index

            index = y + 6 * h  # int(round(w/2))
            if (index > size[0]):
                end_y = size[0]
            else:
                end_y = index
            cv2.rectangle(color_img, (start_x, y), (end_x, end_y), (0, 255, 0), 2)
            # print(faces[0][0])

            # print(temp[y:end_y][start_x:end_x])

        # Energy Calculation
        total = 0
        for row in temp[y:end_y + 1]:
            total = total + sum(row[start_x:end_x + 1])
        total = total / (w * h)
        print(total)
        if (total > thres):  # and flag==0):
            flag = 1
            print("You MOVE")
            if myMessage is not None:
                myMessage.state = 'move'
                myMessage.setPicture()

        elif (total <= thres and flag == 1):
            flag = 0
            print("Freeze")
            if myMessage is not None:
                myMessage.state = 'freeze'
                myMessage.setPicture()

        cv2.imshow(winName, cv2.resize(color_img,(640,480)))
        if cv2.waitKey(10)& 0xFF == ord('q'):
            cv2.destroyWindow(winName)
            break

def mode2_camera():
    pass

def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow(mode1_camera)

    sys.exit(app.exec_())