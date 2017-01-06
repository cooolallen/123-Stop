
from PyQt5.QtWidgets import QApplication
import sys
import cv2
import random

from UI import *


def mode1_camera():
    # Initial setup.
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0)
    winName = "Mode1"
    cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)
    bb_thres = 200  # 100
    approach_thres = 50
    thres = 20
    flag = False
    start = False
    count = 0  # duration
    myMessage = None
    result = None

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
                print("Back!", w, h)
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

        cv2.imshow(winName, cv2.resize(color_img, (640, 480)))
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    print("=============================================================================")
    # Buffer fill in .
    t = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)
    t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)

    approach = False
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

            # Energy Calculation
            if (end_y - y >= size[0] - 10):
                approach = True
                approach_start_x = 0
                approach_end_x = size[1]

            total = 0
            for row in temp[y:end_y + 1]:
                total = total + sum(row[start_x:end_x + 1])
            total = total / (w * h)
            print(total)
            if (total > thres):  # and flag==0):
                flag = True
                cv2.rectangle(color_img, (start_x, y), (end_x, end_y), (0, 0, 255), 2)  # BGR
                print("You MOVE")
                if myMessage is not None:
                    myMessage.state = 'move'
                    myMessage.setPicture()

            elif (total <= thres):  # and flag == 1):
                flag = False
                cv2.rectangle(color_img, (start_x, y), (end_x, end_y), (0, 255, 0), 2)
                print("Freeze")
                if myMessage is not None:
                    myMessage.state = 'freeze'
                    myMessage.setPicture()

        # Approach
        if (approach and len(faces) == 0):
            total = 0
            for row in temp[0:size[0] + 1]:
                total = total + sum(row[approach_start_x:approach_end_x + 1])
            total = total / (w * h)
            print(total)
            if (total > approach_thres):  # and flag==0):
                flag = 1
                cv2.rectangle(color_img, (approach_start_x, 0), (approach_end_x, size[0]), (0, 0, 255), 2)  # BGR
                print("You MOVE APPROACH")
            elif (total <= approach_thres):  # and flag ==1):
                flag = 0
                cv2.rectangle(color_img, (approach_start_x, 0), (approach_end_x, size[0]), (0, 255, 0), 2)
                print("Freeze APPROACH")

        # update frame
        cv2.imshow(winName, cv2.resize(color_img, (640, 480)))

        k = cv2.waitKey(10)
        if k == ord('q'):
            break
        elif k==32:#space
            print('win')
            result = True
            break

    ## Result Judge
    if result is not None:
        if result:
            myMessage.close()
            player_win_img = cv2.imread('./figures/player_win.png')
            cv2.imshow(winName, cv2.resize(player_win_img, (640, 480)))
        else:
            myMessage.state = 'catched'
            myMessage.setPicture()
    else:
        cv2.destroyWindow(winName)
        cam.release()
        return

    # wait and quit
    while True:
        k = cv2.waitKey(10)
        if k == ord('q'):
            cv2.destroyWindow(winName)
            break


def mode2_camera():
    # Initial Setup
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0)
    winName = "Mode2"
    cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)
    start = False
    duration = 5
    rand_range = 100
    count = 0  # duration


    # Wiating for starting
    while not start:
        frame = cam.read()[1]

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=10,  # 5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        if (len(faces) == 0):
            print("Please be in front of camera")
        elif (count == 10):
            print("Start")
            start = True
        else:
            print("count = ", count)
            count += 1
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow(winName, cv2.resize(frame, (640, 480)))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("============================================================================")
    count = -1
    w_random = -1
    h_random = -1
    r_n = -1
    judge = JudgeDialog(r_n)
    while True:
        # Capture frame-by-frame
        frame = cam.read()[1]

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=10,  # 5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        if (len(faces) == 0):
            print("play music")

            if count <= duration:
                count += 1
                frame, w_random, h_random, r_n = random_number(frame,w_random,h_random,r_n,count, rand_range)
            else:
                count=0
                frame, w_random, h_random, r_n = random_number(frame,w_random,h_random,r_n,count, rand_range)

        else:
            print("stop music")
            judge.num = r_n


        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow(winName, cv2.resize(frame, (640, 480)))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    cam.release()
    cv2.destroyAllWindows()

def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

def random_number(frame,w_random,h_random,r_n,count,range):

    print('count=',count,'w=',w_random,'h=',h_random)
    if count == 0:
        r_n = random.randint(1, range)

        w_ori,h_ori,_ = frame.shape
        print(w_ori,h_ori)
        w_random = random.randint(1,w_ori-30)
        h_random = random.randint(1,h_ori-190)
        # w_random = 1280- 190
        # h_random = 720 - 30

    cv2.putText(frame, str(r_n), (h_random,w_random), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 5, (0, 0, 255), 3, 8)

    return frame,w_random,h_random,r_n

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow(mode1_camera,mode2_camera)

    sys.exit(app.exec_())


