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
thres = 150000
flag = 0
color_img = cam.read()[1] 
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

        # print(temp[y:end_y][start_x:end_x])

    total = 0
    for row in temp[y:end_y+1]:
        total = total + sum(row[start_x:end_x+1])
    # print(total)
    if (total>thres and flag==0):
      flag = 1
      print(flag)
    elif(total<=thres and flag ==1):
      flag = 0
      print(flag)

    # t_plus = cam.read()[1]
    if cv2.waitKey(10)==27:
        cv2.destroyWindow(winName)
        break
"""
# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
"""