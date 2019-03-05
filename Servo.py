from Direction import Direction
#import RPi.GPIO as GPIO

class Servo(object):
"""This class controls a servo with GPIO pwm control.
"""


    def __init__(self, pin : int):
        self.pin = pin
        self.position = 0
        self.setPos(0)

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwmControl = GPIO.PWM(self.pin, 1000) # 1000 Hz
        self.pwmControl.start(50) # Set pwm to 50%

    def setPos(self, angle: int) -> None:
        """Sets the angle of the servo to a value between 0 and 180.
        If the value exceeds the limits of 0 and 180 it is set to the nearest
        allowable value.
        
        Args:
            angle (int): The angle to set the servo to.
        """

        safeAngle = adjustExtremes(angle)
        self.position = safeAngle
        self.pwmControl.ChangeDutyCycle(angleToDutyCycle(self.position))
        pass

    def rotate(self, direction: Direction, relativeAngle: int) -> None:
        """Rotates the servo in the given direction by the given amount in degrees.
        If the given amount exceeds the allowable range of the servo. Then the servo is
        rotated until it reaches the allowable amount.

        If an invalid direction is passed in nothing is done.
        
        Args:
            direction (Direction): Clockwise or CounterClockwise
            relativeAngle (int): how many degrees to rotate servo
        """

        newAngle = 0
        if (direction == Direction.Clockwise):
            newAngle = self.position + relativeAngle
        elif (direction == Direction.CounterClockwise):
            newAngle = self.position - relativeAngle
        else:
            return # If the direction was not specified as Clockwise or Counter Clockwise we don't do anything
        self.setPos(newAngle)

def adjustExtremes(angle: int) -> int:
    """returns the angle passed in unless it is outside of allowable limits.
    If the value is greater than 180, then 180 is returned. If the value is
    less than 0 then 0 is returned.
    
    Args:
        angle (int): the angle to check.
    
    Returns:
        int: and angle within allowable limits.
    """

    adjusted = angle
    if angle > 180:
        adjusted = 180
    elif angle < 0:
        adjusted = 0
    return adjusted

def angleToDutyCycle(angle: int) -> int:
    """Converts from an angle between 0 and 180 to a duty cycle between 0 and 100.
    
    Args:
        angle (int): angle
    
    Returns:
        int: dutyCycle
    """

    ratio = angle/180.0
    dutyCycle = ratio * 100
    return dutyCycle