"""
import cv2
import sys

def diffImg(t0,t1,t2):
  d1 = cv2.absdiff(t2,t1)
  d2 = cv2.absdiff(t1,t0)
  return cv2.bitwise_and(d1,d2)

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

winName = "Movement Indicator"
cv2.namedWindow(winName, cv2.WINDOW_AUTOSIZE)

# test = cam.read()[1]
# print(test)

# Read three images first:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_BGR2GRAY)
print("cam.read()[1]")
print(type(cam.read()[1]))
print(cam.read()[1].shape)
print("cam.read()")
print(type(cam.read()))
print(len(cam.read()))
print("gray")
print(type(cv2.cvtColor(cam.read()[1],cv2.COLOR_RGB2GRAY)))
print(cv2.cvtColor(cam.read()[1],cv2.COLOR_RGB2GRAY).shape)
# t_minus = cam.read()[1]
# t = cam.read()[1]
# t_plus = cam.read()[1]

# Initialize temp
thres = 14.5
flag = 0
start = 0
count = 0  # duration
color_img = cam.read()[1] 
while(start==0):
    cv2.imshow(winName, color_img)
    color_img = cam.read()[1]
    gray = cv2.cvtColor(color_img,cv2.COLOR_RGB2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=10,#5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    for (x, y, w, h) in faces:
        if(w>37 and h>37 and start==0):
            print("Back!")
            print(w,h)
        elif(w<=37 and h <= 37 and count<=10 and start==0):
            count = count+1
        elif(count>10 and start==0):
            print("start")
            start = 1
        cv2.rectangle(color_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    if cv2.waitKey(10)==27:
        cv2.destroyWindow(winName)
        break
print("=============================================================================")

while True:
    # Capture frame-by-frame
    cv2.imshow(winName, color_img)
    # cv2.imshow(winName, diffImg(t_minus,t,t_plus))
    # Read next image
    t_minus = t
    t = t_plus
    color_img = cam.read()[1]
    gray = cv2.cvtColor(color_img,cv2.COLOR_RGB2GRAY)
    t_plus = gray
    # temp = diffImg(t_minus,t,t_plus) 
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=10,#5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    temp = diffImg(t_minus,t,t_plus) 
    size = gray.shape

    for (x, y, w, h) in faces:
        index = x-w #int(round(w/2))
        if (index <=0):
            start_x = 0
        else:
            start_x = index

        index = x+2*w #int(round(w/2))
        if (index > size[1]):
            end_x = size[1]
        else:
            end_x = index

        index = y+6*h #int(round(w/2))
        if (index > size[0]):
            end_y = size[0]
        else:
            end_y = index
        cv2.rectangle(color_img, (start_x, y), (end_x, end_y), (0, 255, 0), 2)
        # print(faces[0][0])
        
        # print(temp[y:end_y][start_x:end_x])


    total = 0
    for row in temp[y:end_y+1]:
        total = total + sum(row[start_x:end_x+1])
    total = total/(w*h)
    print(total)
    if (total>thres):# and flag==0):
        flag = 1
        print("You MOVE")
    elif(total<=thres and flag ==1):
        flag = 0
        print("Freeze")

    # t_plus = cam.read()[1]
    if cv2.waitKey(10)==27:
        cv2.destroyWindow(winName)
        break

"""
"""
# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
"""

# from UI import *
import cv2

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     test = audio_player('./test.mp3')
#
#     test.start()
#     while True:
#         print('ffff')
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     test.pause()
#
#     while True:
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#
#
#     sys.exit(app.exec_())

from UI import *
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QAudioOutput, QAudioFormat
import sys

app = QApplication(sys.argv)
count = 0
# music = audio_player('/Users/cooolallen1/Desktop/test.mp3')
# music.start()
# music.output

music = QSound('test.mp3')

music.play()
while(count<=100000):
    # print(music.output.state())
    print("count: ", count)
    count = count + 1
music.stop()
print("music pause")
# music.stream.stop_stream()
# music.stream.close()
# music.p.terminate()
music.destroy()
sys.exit(app.exec_())



# app=QApplication(sys.argv) #1st Edit
#
# output=QAudioOutput()
#
# soundFile=QtCore.QFile()
# soundFile.setFileName("./test.mp3")
# soundFile.open(QtCore.QIODevice.ReadOnly)
#
# output.start(soundFile)
#
#
#
# while True:
#     print(output.state())
# app.exec_()                #1st Edit