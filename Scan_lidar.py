# -*- coding: utf-8 -*

# Import libraries

import os
os.system('sudo systemctl start pigpiod')
import time
import pigpio
import numpy as np
import math
import matplotlib.pyplot as plt
import csv
from mpl_toolkits.mplot3d import Axes3D
from tfmini_23 import get_dist
import pickle


# Connect to local Pi.
pi = pigpio.pi()

# Set GPIO 17 & 18 as outputs
servo1 = 17
servo2 = 18

#Define variables
radius = get_dist()
min_pos_x = 0
max_pos_x = 180
pos_x = min_pos_x
min_pos_y = 110
max_pos_y = 2
pos_y = min_pos_y
pos_x_init = (max_pos_x + min_pos_x) / 2
pos_y_init = (max_pos_y + min_pos_y) / 2
deg2rad = math.pi / 180
altitude = 0
inc_step_x = 2
inc_step_y = 2
delay_x = 0
delay_y = 0

xlist = []
ylist = []
zlist = []
coord = [xlist, ylist, zlist]


def AngleToPWM(angle):
    if angle > 180 or angle < 0 :
        return False
    start = 500
    end = 2500
    pwm_for_one_degree = (end - start)/180 #Calcul ratio from angle to percent
    angle_as_duration_pwm = angle * pwm_for_one_degree
    return start + angle_as_duration_pwm


def coord_xyz(pos_x, pos_y):

    radius = get_dist()
    azimuth = pos_x * deg2rad
    elevation = pos_y * deg2rad
    x = radius * math.sin(elevation) * math.cos(azimuth)
    y = radius * math.sin(elevation) * math.sin(azimuth)
    z = radius * math.cos(elevation)

    x = round(x, 2)
    y = round(y, 2)
    z = round(z, 2)
    xlist.append(x)
    ylist.append(y)
    zlist.append(z)

    return x, y, z, radius


# Choice of scan
scan = int(input("Press 1 and ENTER for 'AUTO scan'\nPress 2 and ENTER for 'MANUAL scan'\n"))
if scan > 2 or scan < 1 :
    print("Wrong choice, please choose again!")
    scan = int(input("Press 1 and ENTER for 'AUTO scan'\nPress 2 and ENTER for 'MANUAL scan'\n"))

#Setup values for manual scan
if scan == 2:
    start_time = time.time()
    #Angles choice for scan
    min_pos_y = float(input("1. Choose a MINIMAL elevation's angle between -22° and 0° and press ENTER:\n"))
    if min_pos_y > 0 or min_pos_y < -22.0 :
        print("Bad angle, please choose between -22° and 0°")
        min_pos_y = float(input("New angle:"))

    max_pos_y = float(input("2. Choose a MAXIMAL elevation's angle between 0° et 88° and press ENTER:\n"))
    if max_pos_y > 88.0 or max_pos_y < 0 :
        print("Bad angle, please choose between 0° and 88°")
        max_pos_y = float(input("New angle:"))

    # Setup pan&tilt plan
    min_pos_y = 90 - min_pos_y
    pos_y = min_pos_y
    max_pos_y = 90 - max_pos_y

    # Start PWM running on both servos, value of 7 (pulse off)
    pi.set_servo_pulsewidth(servo1, AngleToPWM(pos_x))
    pi.set_servo_pulsewidth(servo2, AngleToPWM(pos_y))
    while pos_y > max_pos_y:

        if max_pos_x > min_pos_x:
            for pos_x in np.arange(min_pos_x, max_pos_x, inc_step_x):
                pwm = AngleToPWM(pos_x)
                pi.set_servo_pulsewidth(servo1, pwm)
                time.sleep(delay_x)
                coord_xyz(pos_x, pos_y)

        pos_y = pos_y - inc_step_y
        duty = AngleToPWM(pos_y)
        pi.set_servo_pulsewidth(servo2, duty)

        if max_pos_x > min_pos_x:
            for pos_x in np.arange(max_pos_x, min_pos_x, -inc_step_x):
                pwm = AngleToPWM(pos_x)
                pi.set_servo_pulsewidth(servo1, pwm)
                time.sleep(delay_x)
                coord_xyz(pos_x, pos_y)

        pos_y = pos_y - inc_step_y
        duty = AngleToPWM(pos_y)
        pi.set_servo_pulsewidth(servo2, duty)

    #Go to initial position
    pi.set_servo_pulsewidth(servo1, 1500)
    pi.set_servo_pulsewidth(servo2, 1500)

    #Stop signal
    pi.stop()
    print("--- %s seconds ---" % (time.time() - start_time))

# Auto scan
else:
    start_time = time.time()
    pi.set_servo_pulsewidth(servo1, AngleToPWM(pos_x))
    pi.set_servo_pulsewidth(servo2, AngleToPWM(pos_y))
    while pos_y > max_pos_y:

        if max_pos_x > min_pos_x:
            for pos_x in np.arange(min_pos_x, max_pos_x, inc_step_x):
                pwm = AngleToPWM(pos_x)
                pi.set_servo_pulsewidth(servo1, pwm)
                time.sleep(delay_x)
                coord_xyz(pos_x, pos_y)

        pos_y = pos_y - inc_step_y
        duty = AngleToPWM(pos_y)
        pi.set_servo_pulsewidth(servo2, duty)

        if max_pos_x > min_pos_x:
            for pos_x in np.arange(max_pos_x, min_pos_x, -inc_step_x):
                pwm = AngleToPWM(pos_x)
                pi.set_servo_pulsewidth(servo1, pwm)
                time.sleep(delay_x)
                coord_xyz(pos_x, pos_y)

        pos_y = pos_y - inc_step_y
        duty = AngleToPWM(pos_y)
        pi.set_servo_pulsewidth(servo2, duty)

    #Go to initial position
    pi.set_servo_pulsewidth(servo1, 1500)
    pi.set_servo_pulsewidth(servo2, 1500)

    #Stop signal
    pi.stop()
    print("--- %s seconds ---" % (time.time() - start_time))

# Save points cloud in csv file
with open("Points_cloud.csv", "w") as f_write:
    writer = csv.writer(f_write)
    writer.writerows(zip(*coord))

# Show 3D points cloud into Matplotlib
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X')
ax.set_xlim(-100, 100)
ax.set_ylabel('Y')
ax.set_ylim(-10, 200)
ax.set_zlabel('Z')
ax.set_zlim(-100, 250)
ax.scatter(xlist, ylist, zlist, s=0.5) # 's' is the marker size
pickle.dump(fig, open('Mapp_lidar.fig.pickle', 'wb')) # Picture backup
plt.show()
