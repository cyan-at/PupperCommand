from UDPComms import Publisher, Subscriber, timeout
from PS4Joystick import Joystick

import time

## you need to git clone the PS4Joystick repo and run `sudo bash install.sh`

## Configurable ##
MESSAGE_RATE = 20
PUPPER_COLOR = {"red":0, "blue":0, "green":255}

joystick_pub = Publisher(8830)
joystick_subcriber = Subscriber(8840, timeout=0.01)
joystick = Joystick()
joystick.led_color(**PUPPER_COLOR)

while True:
    print("running")
    values = joystick.get_input()

    # discrete
    R1 = values["button_r1"]
    x = values["button_cross"]
    L1 = values["button_l1"]

    # continuous
    left_y = -values["left_analog_y"]
    left_x = values["left_analog_x"]
    right_x = values["right_analog_x"]
    right_y = -values["right_analog_y"]
    dpady = values["dpad_up"] - values["dpad_down"]
    dpadx = values["dpad_right"] - values["dpad_left"]

    # unused
    L2 = values["l2_analog"]
    R2 = values["r2_analog"]
    square = values["button_square"]
    circle = values["button_circle"]
    triangle = values["button_triangle"]

    msg = {
        # discrete between 0 (off) and 1 (on)
        "R1": R1,
        "x": x,
        "L1": L1,

        # continuous these all go between 0.0 and 1.0
        "ly": left_y,
        "lx": left_x,
        "rx": right_x,
        "ry": right_y,
        "dpady": dpady,
        "dpadx": dpadx,

        # other
        "message_rate": MESSAGE_RATE,

        # unused
        "L2": L2,
        "R2": R2,
        "square": square,
        "circle": circle,
        "triangle": triangle,
    }
    joystick_pub.send(msg)

    try:
        msg = joystick_subcriber.get()
        joystick.led_color(**msg["ps4_color"])
    except timeout:
        pass

    time.sleep(1 / MESSAGE_RATE)
