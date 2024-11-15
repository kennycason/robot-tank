# Primary Tank code
import RPi.GPIO as GPIO
from enum import Enum

R_PIN_ENABLE_A = 25
R_PIN_IN1 = 24
R_PIN_IN2 = 23

L_PIN_ENABLE_A = 16
L_PIN_IN1 = 20
L_PIN_IN2 = 26

GPIO.setmode(GPIO.BCM)  # use BCM numbers


class Direction(Enum):
    STOP = 0
    FORWARD = 1
    REVERSE = 2


class Track:
    def __init__(self, pin_enableA: int, pin_in1: int, pin_in2: int, is_inverted: bool = False):
        print("Init Track, enA: " + str(pin_enableA) + ", in1: " + str(pin_in1) + ", in2: " + str(pin_in2))
        self.pin_enableA = pin_enableA
        self.pin_in1 = pin_in1
        self.pin_in2 = pin_in2
        self.pwmMax: int = 100
        self.pwmStart: int = 100
        self.speed: int = 100  # not used
        self.direction = Direction.STOP
        self.is_inverted = is_inverted

        GPIO.setup(pin_in1, GPIO.OUT)
        GPIO.setup(pin_in2, GPIO.OUT)
        GPIO.setup(pin_enableA, GPIO.OUT)

        GPIO.setup(pin_in1, GPIO.LOW)
        GPIO.setup(pin_in2, GPIO.LOW)

        self.pwm = GPIO.PWM(pin_enableA, self.pwmMax)
        self.pwm.start(self.pwmStart)

    def forward(self):
        print("track forward")
        self.direction = Direction.FORWARD
        if not self.is_inverted:
            GPIO.output(self.pin_in1, True)
            GPIO.output(self.pin_in2, False)
            self.set_speed(self.speed)
            # self.pwm.ChangeDutyCycle(100)
        else:
            GPIO.output(self.pin_in1, False)
            GPIO.output(self.pin_in2, True)
            self.set_speed(self.speed)
            # self.pwm.ChangeDutyCycle(0)

    def reverse(self):
        print("track reverse")
        self.direction = Direction.REVERSE
        if not self.is_inverted:
            GPIO.output(self.pin_in1, False)
            GPIO.output(self.pin_in2, True)
            self.set_speed(self.speed)
            # self.pwm.ChangeDutyCycle(0)
        else:
            GPIO.output(self.pin_in1, True)
            GPIO.output(self.pin_in2, False)
            self.set_speed(self.speed)
            # self.pwm.ChangeDutyCycle(100)

    def stop(self):
        print("track stop")
        self.direction = Direction.STOP
        GPIO.output(self.pin_in1, False)
        GPIO.output(self.pin_in2, False)
        # keep speed as-is, and change duty cycle so that resuming movement will use last speed.
        self.pwm.ChangeDutyCycle(0)

    def set_speed(self, speed: int):
        self.speed = speed
        if self.speed >= 100:
            self.speed = 100
        elif self.speed < 0:
            self.speed = 0

        print("speed: " + str(self.speed))

        # if motor is not running, only set the internal speed. speed will be passed to motor when tank moves.
        if self.direction == Direction.STOP:
            print("tank stopped, not changing motor speed")
            return

        # # in the case speed is 0, then just call our helper function to stop the track
        # if self.speed == 0:
        #     self.direction = Direction.STOP
        #     self.stop()

        if self.direction == Direction.FORWARD:
            if not self.is_inverted:
                self.pwm.ChangeDutyCycle(self.speed)
            else:
                self.pwm.ChangeDutyCycle(100 - self.speed)
        elif self.direction == Direction.REVERSE:
            if not self.is_inverted:
                self.pwm.ChangeDutyCycle(100 - self.speed)
            else:
                self.pwm.ChangeDutyCycle(self.speed)

    def speed_up(self):
        print("speed++")
        self.set_speed(self.speed + 10)

    def speed_down(self):
        print("speed--")
        self.set_speed(self.speed - 10)


class Tank:
    def __init__(self):
        self.left_track = Track(L_PIN_ENABLE_A, L_PIN_IN1, L_PIN_IN2, is_inverted=True)
        self.right_track = Track(R_PIN_ENABLE_A, R_PIN_IN1, R_PIN_IN2, is_inverted=True)

    def status(self):
        return {
            'leftTrack': {
                'speed': self.left_track.speed
            },
            'rightTrack': {
                'speed': self.right_track.speed
            }
        }

    def cleanup(self):
        GPIO.cleanup()

    def left_track_forward(self):
        self.left_track.forward()

    def left_track_reverse(self):
        self.left_track.reverse()

    def left_track_stop(self):
        self.left_track.stop()

    def right_track_forward(self):
        self.right_track.forward()

    def right_track_reverse(self):
        self.right_track.reverse()

    def right_track_stop(self):
        self.right_track.stop()

    def forward(self):
        print("forward")
        self.left_track.forward()
        self.right_track.forward()

    def reverse(self):
        print("reverse")
        self.left_track.reverse()
        self.right_track.reverse()

    def stop(self):
        print("stop")
        self.left_track.stop()
        self.right_track.stop()

    def turn_left(self):
        print("turn left")
        self.left_track.stop()
        self.right_track.forward()

    def turn_right(self):
        print("turn right")
        self.left_track.forward()
        self.right_track.stop()

    def rotate_clockwise(self):
        print("rotate clockwise")
        self.left_track.forward()
        self.right_track.reverse()

    def rotate_counterclockwise(self):
        print("rotate counterclockwise")
        self.left_track.reverse()
        self.right_track.forward()

    def right_track_speed_up(self):
        print("right track speed++")
        self.right_track.speed_up()

    def right_track_speed_down(self):
        print("right track speed--")
        self.right_track.speed_down()

    def left_track_speed_up(self):
        print("left track speed++")
        self.left_track.speed_up()

    def left_track_speed_down(self):
        print("left track speed--")
        self.left_track.speed_down()

    def speed_up(self):
        print("speed++")
        self.left_track.speed_up()
        self.right_track.speed_up()
        return self.status()

    def speed_down(self):
        print("speed--")
        self.left_track.speed_down()
        self.right_track.speed_down()
        return self.status()

    def set_speed(self, speed: int):
        print("set speed: " + str(speed))
        self.left_track.set_speed(speed)
        self.right_track.set_speed(speed)
        return self.status()
