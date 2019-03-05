from Servo import Servo
from Direction import Direction, getImageCenter, getObjectCenter, getObjectDirection
from threading import Thread
import queue
import math
import numpy as np
from typing import Tuple, Boolean

class ArmControl:
    """Object to control a 2 axis servo controlled arm.

    Given a queue with (obj, frame) objects this class can track an the object from the queue.
    The data in (obj, frame) should be formated ((x,y,width,height), img: np.array)
    """

    def __init__(self, horizontalControlPin: int, verticalControlPin: int) -> ArmControl:
        self.horizontalControlPin = horizontalControlPin
        self.verticalControlPin = verticalControlPin
        self.horizontalServo = Servo(horizontalControlPin)
        self.verticalServo = Servo(verticalControlPin)
        
        self.tracking = False

    def moveLeft(self) -> None:
        """Moves horizontal servo 1 degree counter clockwise
        """

        self.horizontalServo.rotate(Direction.CounterClockwise, 1)
    
    def moveRight(self) -> None:
        """Moves horizontal servo 1 degree Clockwise
        """

        self.horizontalServo.rotate(Direction.Clockwise, 1)
    
    def moveUp(self) -> None:
        """Moves vertical servo 1 degree Clockwise
        """
        self.verticalServo.rotate(Direction.Clockwise, 1)

    def moveDown(self) -> None:
        """Moves vertical servo 1 degree CounterClockwise
        """
        self.verticalServo.rotate(Direction.CounterClockwise, 1)

    def trackFace(self, cameraStream: queue) -> None:
        """Tracks a face/object given a queue that contains objects and the frame the object was captured in.
        The queue object format is ((x,y,width,height), img: np.array)

        This function runs until stopAsyncFaceTracking() is called.
        
        Args:
            cameraStream (queue): queue with objects and frames
        """

        face = None
        frame = None
        # Get the first frame
        while face is None or frame is None:
            try:
                face, frame = cameraStream.get_nowait()
            except queue.Empty:
                pass
        self.tracking = True
        while(self.tracking):
            while(not faceCentered(face, frame) and self.tracking):
                direction = getObjectDirection(face, frame)
                if (direction[0] != Direction.NoDirection):
                    if (direction[0] == Direction.Left):
                        self.moveLeft()
                    elif (direction[0] == Direction.Right):
                        self.moveRight()
                if (direction[1] != Direction.NoDirection):
                    if (direction[1] == Direction.Up):
                        self.moveUp()
                    elif (direction[1] == Direction.Down):
                        self.moveDown()

                #Get the next image and face from queue
                face, frame = nextFaceFromQueue(face, frame, cameraStream)
            face, frame = nextFaceFromQueue(face, frame, cameraStream)
                    
            

    
    def trackFaceAsync(self, cameraStream: queue):
        """Calls trackFace on another thread. To stop that thread call stopAsyncFaceTracking().
            The queue object format is ((x,y,width,height), img: np.array)

        Args:
            cameraStream (Tuple): queue with objects and frames
        """

        followFaceTask = Thread(target=self.trackFace, args=[cameraStream])
        followFaceTask.start()

    def stopAsyncFaceTracking(self):
        """Call this function to stop trackFaceAsync thread.
        """

        self.tracking = False

tolerance = .08 # How close as percentage of the width of a frame that the face must be to the center     
def faceCentered(face: Tuple[int,int,int,int], frame: np.array) -> Boolean:
    """Detects if the face/object is close to the center of the frame.
    
    Args:
        face (Tuple[int,int,int,int]): (x,y,width,height) face bounding box
        frame (np.array): image face was captured in
    
    Returns:
        [Boolean]: [description]
    """

    allowablePixelDistance = frame.shape[1] * tolerance
    faceCenter = getObjectCenter(face)
    frameCenter = getImageCenter(frame)
    faceDistanceFromCenter = math.hypot(faceCenter[0] - frameCenter[0], faceCenter[1] - frameCenter[1])
    return faceDistanceFromCenter < allowablePixelDistance

def nextFaceFromQueue(face: Tuple[int,int,int,int], frame: np.array, faceQueue: queue):
    """Gets the next face/obj, frame pair from the queue. If a new pair is not available
    it returns the face and frame that were passed in.
    
    Args:
        face (Tuple[int,int,int,int]): face/object (x,y,width,height)
        frame (np.array): frame that face/object was detected in
        faceQueue (queue): queue that stores face/object frame pairs (face/obj: Tuple[int,int,int,int], frame: np.array)
    
    Returns:
        (face/obj: Tuple[int,int,int,int], frame: np.array): the next face/obj frame pair
    """

    nextFace = face
    nextFrame = frame
    if not faceQueue.empty():
        try:
            nextFace, nextFrame = faceQueue.get_nowait()
        except queue.Empty:
            pass # We will just use the latest image we have
    return nextFace, nextFrame
