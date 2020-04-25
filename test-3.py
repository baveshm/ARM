import sys
import time
from pymata4 import pymata4


DISTANCE_CM = 2
TRIGGER_PIN = 8
ECHO_PIN = 9


# A callback function to display the distance
def the_callback(data):
    """
    The callback function to display the change in distance
    :param data: [pin_type=12, trigger pin number, distance, timestamp]
    """
    print(f'Distance in cm: {data[DISTANCE_CM]}')


def sonar(my_board, trigger_pin, echo_pin, callback):
    """
    Set the pin mode for a sonar device. Results will appear via the
    callback.
    :param my_board: an pymata express instance
    :param trigger_pin: Arduino pin number
    :param echo_pin: Arduino pin number
    :param callback: The callback function
    """

    # set the pin mode for the trigger and echo pins
    my_board.set_pin_mode_sonar(trigger_pin, echo_pin, callback)

    while True:
        try:
            time.sleep(0.1)
            print(f'data read: {my_board.sonar_read(TRIGGER_PIN)[0]}')
            distance = my_board.sonar_read(TRIGGER_PIN)[0]
            if distance<5:
                servo(board,10)
            else:
                servo_rev(board, 10)
        except KeyboardInterrupt:
            my_board.shutdown()
            sys.exit(0)


def servo(my_board, pin):

    # set the pin mode
    my_board.set_pin_mode_servo(pin)

    # set the servo to 90 degrees
    my_board.servo_write(pin, 90)

def servo_rev(my_board, pin):
    my_board.set_pin_mode_servo(pin)

    my_board.servo_write(pin, 40)


board = pymata4.Pymata4()
try:
    sonar(board, TRIGGER_PIN, ECHO_PIN, the_callback)
    board.shutdown()
except (KeyboardInterrupt, RuntimeError):
    board.shutdown()
    sys.exit(0)