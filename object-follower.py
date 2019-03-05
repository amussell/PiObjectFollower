import numpy as np
import cv2
from Direction import printDirectionTuple, getObjectDirection, getImageCenter, Direction
import queue
from ArmControl import faceCentered, ArmControl

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') # Load Face Tracking Model
cap = cv2.VideoCapture(0)

# Face rectangle outline parameters
rectangleOutlineColor = (255,0,0) #Blue
rectangleLineWidth = 2 # pixels

# setup queue for object following
faceQueue = queue.Queue(maxsize=1)
cameraControl = ArmControl(horizontalControlPin=10, verticalControlPin=11)
cameraControl.trackFaceAsync(faceQueue)

while(True):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5) #Detect Faces
    if len(faces) > 0:
        try:
            faceQueue.put_nowait((faces[0], frame))
        except queue.Full:
            pass
        
        x,y,w,h = faces[0]
        cv2.rectangle(frame, (x,y),(x+w,y+h),rectangleOutlineColor,rectangleLineWidth) #Draw rectangle
        #printDirectionTuple(getObjectDirection(faces[0], frame))
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cameraControl.stopAsyncFaceTracking()
cap.release()
cv2.destroyAllWindows()