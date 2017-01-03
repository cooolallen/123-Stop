import cv2
import sys

#cascPath = sys.argv[1]
#faceCascade = cv2.CascadeClassifier(cascPath)
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=10,#5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    print(faces)
    size = gray.shape
    # print(size[0])
    # print(size[1])
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        # cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
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
        cv2.rectangle(frame, (start_x, y), (end_x, end_y), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()