import enum
import numpy as np
from typing import Tuple
from math import floor

class Direction(enum.Enum):
"""Enum for different Directions.
"""

    Left = 1
    Right = 2
    Up = 3
    Down = 4
    NoDirection = 5 # Use if a two points are the same
    Clockwise = 5
    CounterClockwise = 6

def getImageCenter(img: np.array) -> Tuple[int, int]:
    """Finds the center point of an image
    
    Args:
        img (np.array): image in np array formatted as (height, width, channels)
    
    Returns:
        Tuple[int, int]: (x, y) center point of image
    """

    width = img.shape[1]
    height = img.shape[0]
    mid = (floor(width/2), floor(height/2))
    return mid

def getObjectCenter(obj: Tuple[int,int,int,int]) -> Tuple[int, int]:
    """Finds the center point of an object
    
    Args:
        obj (Tuple[int,int,int,int]): object tuple in form of (x,y,width,height)
    
    Returns:
        Tuple[int, int]: point tuple in form (x,y)
    """

    x,y,w,h = obj
    return x + floor(w/2), y + floor(h/2)

def isLeftOrRight(pointA: Tuple[int,int], pointB: Tuple[int,int]) -> Direction:
    """Returns left is pointA is left of pointB

    returns Direction.NoDirection if the points have the same x value
    
    Args:
        pointA (tuple): tuple in form (x, y)
        pointB (tuple): tuple in form (x, y)
    
    Returns:
        Direction: the direction (left or right) of pointA relative to pointB
    """

    if pointA[0] < pointB[0]: return Direction.Left
    if pointA[0] > pointB[0]: return Direction.Right
    return Direction.NoDirection

def isUpOrDown(pointA: Tuple[int,int], pointB: Tuple[int,int]) -> Direction:
    """Returns Up if pointA is above pointB

    returns NoDirection if pointA and pointB have the same y value.

    Args:
        pointA (tuple): tuple in form (x, y)
        pointB (tuple): tuple in form (x, y)

    Returns:
        Direction: direction of pointA relative to pointB
    """

    if pointA[1] > pointB[1]: return Direction.Down # Coordinated increase as they are lower
    if pointA[1] < pointB[1]: return Direction.Up
    return Direction.NoDirection

def printDirectionTuple(directions: Tuple[Direction, Direction]) -> None:
    names = {
        Direction.Left : "Left", 
        Direction.Right : "Right", 
        Direction.Up : "Upper", 
        Direction.Down : "Lower",
        Direction.NoDirection : "Middle"
    }
    print(names[directions[0]] + "-" + names[directions[1]])


def getObjectDirection(obj : Tuple[int,int,int,int], frame: np.array) -> Tuple[Direction, Direction]:
    """Gets the direction of the center of the object relative to the center
    of the frame. 
    
    Args:
        obj (tuple, frame): tuple in form (x, y, width, height)
        Direction ([type]): [description]
    
    Returns:
        tuple(Direction, Direction): (leftOrRight, upOrDown)
    """

    x,y,w,h = obj
    imageCenter = getImageCenter(frame)
    objectCenter = getObjectCenter(obj)
    horizontalDirection = isLeftOrRight(objectCenter, imageCenter)
    verticalDirection = isUpOrDown(objectCenter, imageCenter)
    return horizontalDirection, verticalDirection