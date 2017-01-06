
from PyQt5.QtWidgets import QApplication
import sys
import cv2
import random
import threading
import pyaudio
import wave
import time

from UI import *
# set duration(frame number) for next 123 stop
global mainWindow

FRAME_THRES = 100
def mode1_camera():
    # Initial setup.
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cam = cv2.VideoCapture(0)
    winName = "Mode1"
    cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)
    bb_thres = 100# 200  # 100
    approach_thres = 50
    thres = 20
    # Cary
    while_break = False
    frame_duration = 100
    # 
    start = False
    count = 0  # duration
    myMessage = None
    result = None
    t1 = threading.Thread(target=play_music, args=())


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
    start_time = time.time()
    approach = False
    while True:
        # Pushing back
        t_minus = t
        t = t_plus
        color_img = cam.read()[1]
        gray = cv2.cvtColor(color_img, cv2.COLOR_RGB2GRAY)
        t_plus = gray

        # whether the music has to play
        if(t1.isAlive()==False):
            t1 = threading.Thread(target=play_music, args=())
        if(t1.isAlive()==False and frame_duration>=FRAME_THRES):
            frame_duration = 0
            t1.start()
            

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
                cv2.rectangle(color_img, (start_x, y), (end_x, end_y), (0, 0, 255), 2)  # BGR
                # if music stop
                if not t1.isAlive():
                    print("You MOVE")
                    frame_duration = frame_duration + 1
                    if myMessage is not None:
                        myMessage.state = 'move'
                        myMessage.setPicture()
                    while_break = True

            elif (total <= thres):  # and flag == 1):
                cv2.rectangle(color_img, (start_x, y), (end_x, end_y), (0, 255, 0), 2)
                # if music stop
                if not t1.isAlive():
                    print("Freeze")
                    frame_duration = frame_duration + 1
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
                cv2.rectangle(color_img, (approach_start_x, 0), (approach_end_x, size[0]), (0, 0, 255), 2)  # BGR
                # if music stop
                if not t1.isAlive():
                    print("You MOVE APPROACH")
                    frame_duration = frame_duration + 1
                    if myMessage is not None:
                        myMessage.state = 'move'
                        myMessage.setPicture()
                    while_break = True
            elif (total <= approach_thres):  # and flag ==1):
                cv2.rectangle(color_img, (approach_start_x, 0), (approach_end_x, size[0]), (0, 255, 0), 2)
                # if music stop
                if not t1.isAlive():
                    frame_duration = frame_duration + 1
                    print("Freeze APPROACH")
                    if myMessage is not None:
                        myMessage.state = 'freeze'
                        myMessage.setPicture()
        # print for checking time
        print(frame_duration)
        # detect moving
        if(while_break):
            result = False
            break
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
            mainWindow.table.record('mode1',True,time.time()-start_time)
            cv2.imshow(winName, cv2.resize(player_win_img, (640, 480)))
        else:
            myMessage.close()
            player_win_img = cv2.imread('./figures/player_lose.png')
            mainWindow.table.record('mode1',False,time.time()-start_time)
            cv2.imshow(winName, cv2.resize(player_win_img, (640, 480)))
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
    start_time = time.time()
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

        if judge.result is not None:
            break


        # Display the resulting frame
        cv2.imshow(winName, cv2.resize(frame, (640, 480)))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyWindow(winName)
            cam.release()
            return

    # Judge result
    if judge.result:#win
        player_win_img = cv2.imread('./figures/player_win.png')
        mainWindow.table.record('mode2',True,time.time()-start_time)
        cv2.imshow(winName, cv2.resize(player_win_img, (640, 480)))
    else:#lose
        player_win_img = cv2.imread('./figures/player_lose2.png')
        mainWindow.table.record('mode2',False,time.time()-start_time)
        cv2.imshow(winName, cv2.resize(player_win_img, (640, 480)))

    # wait and quit
    while True:
        k = cv2.waitKey(10)
        if k == ord('q'):
            # When everything is done, release the capture
            cv2.destroyWindow(winName)
            cam.release()
            break

def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

def play_music():
    CHUNK = 1024
    # play 123
    song_front = random.randint(0,3)
    if(song_front==0):
        music_name = '123_slow.wav'
    elif(song_front==1):
        music_name = '123_median.wav'
    else:
        music_name = '123_quick.wav'

    wf = wave.open(music_name, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)
    while(data!=''):
        stream.write(data)
        data = wf.readframes(CHUNK)

    # play stop
    song_back = random.randint(0,3)  
    if(song_back==0):
        music_name = 'stop_slow.wav'
    elif(song_back==1):
        music_name = 'stop_median.wav'
    else:
        music_name = 'stop_quick.wav'
    wf = wave.open(music_name, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)
    while(data!=''):
        stream.write(data)
        data = wf.readframes(CHUNK)
    return

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


