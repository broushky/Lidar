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
#import sys
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
min_pos_x = 50
max_pos_x = 130
pos_x = min_pos_x
min_pos_y = 105
max_pos_y = 60
pos_y = min_pos_y
pos_x_init = (max_pos_x + min_pos_x) / 2
pos_y_init = (max_pos_y + min_pos_y) / 2
deg2rad = math.pi / 180
last_radius = 0
inc_step_x = 5
inc_step_y = 3
delay_x = 0.05
delay_y = 0.05

xlist = []
ylist = []
zlist = []


def AngleToPWM(angle):
    if angle > 180 or angle < 0 :
        return False
    start = 500
    end = 2500
    pwm_for_one_degree = (end - start)/180 #Calcul ratio from angle to percent
    angle_as_duration_pwm = angle * pwm_for_one_degree
    return start + angle_as_duration_pwm


# Choice of scan
scan = int(input("Press 1 and ENTER for 'AUTO scan'\nPress 2 and ENTER for 'MANUAL scan'\n"))
if scan > 2 or scan < 1 :
    print("Wrong choice, please choose again!")
    scan = int(input("Press 1 and ENTER for 'AUTO scan'\nPress 2 and ENTER for 'MANUAL scan'\n"))

#Loop for duty values
if scan == 2:
    start_time = time.time()
    #Angles choice for scan
    min_pos_y = float(input("1. Choose a MINIMAL elevation's angle between -22° and 0° and press ENTER:\n"))
    while min_pos_y > 0 or min_pos_y < -22 :
        print("Bad angle, please choose between -22° and 0°")
        min_pos_y = float(input("New angle:"))

    max_pos_y = float(input("2. Choose a MAXIMAL elevation's angle between 0° et 88° and press ENTER:\n"))
    while max_pos_y > 88 or max_pos_y < 0 :
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
                #print(pos_x)
                radius = get_dist()
                azimuth = pos_x * deg2rad
                elevation = pos_y * deg2rad
                x = radius * math.sin(elevation) * math.cos(azimuth)
                y = radius * math.sin(elevation) * math.sin(azimuth)
                z = radius * math.cos(elevation)

                x = round(x, 2)
                y = round(y, 2)
                z = round(z, 2)

                #print("x=", x)
                #print("y=", y)
                #print("z=", z)

                xlist.append(x)
                ylist.append(y)
                zlist.append(z)

                ax.scatter(xlist[j],ylist[j],zlist[j])
                j+=1
                plt.show()
                plt.pause(0.0001)

        duty = AngleToPWM(pos_y)
        pi.set_servo_pulsewidth(servo2, duty)
        time.sleep(delay_x)
        pos_y = pos_y - inc_step_y
        #print(pos_x, pos_y)
        radius = get_dist()
        azimuth = pos_x * deg2rad
        elevation = pos_y * deg2rad
        x = radius * math.sin(elevation) * math.cos(azimuth)
        y = radius * math.sin(elevation) * math.sin(azimuth)
        z = radius * math.cos(elevation)

        x = round(x, 2)
        y = round(y, 2)
        z = round(z, 2)

        #print("x=", x)
        #print("y=", y)
        #print("z=", z)

        xlist.append(x)
        ylist.append(y)
        zlist.append(z)

        ax.scatter(xlist[j],ylist[j],zlist[j])
        j+=1
        plt.show()
        plt.pause(0.0001)

        if max_pos_x > min_pos_x:
            for pos_x in np.arange(max_pos_x, min_pos_x, -inc_step_x):
                pwm = AngleToPWM(pos_x)
                pi.set_servo_pulsewidth(servo1, pwm)
                time.sleep(delay_x)
                #print(pos_x)
                radius = get_dist()
                azimuth = pos_x * deg2rad
                elevation = pos_y * deg2rad
                x = radius * math.sin(elevation) * math.cos(azimuth)
                y = radius * math.sin(elevation) * math.sin(azimuth)
                z = radius * math.cos(elevation)

                x = round(x, 2)
                y = round(y, 2)
                z = round(z, 2)

                #print("x=", x)
                #print("y=", y)
                #print("z=", z)

                xlist.append(x)
                ylist.append(y)
                zlist.append(z)

                ax.scatter(xlist[j],ylist[j],zlist[j])
                j+=1
                plt.show()
                plt.pause(0.0001)

        duty = AngleToPWM(pos_y)
        pi.set_servo_pulsewidth(servo2, duty)
        time.sleep(delay_y)
        pos_y = pos_y - inc_step_y
        #print(pos_x, pos_y)
        radius = get_dist()
        azimuth = pos_x * deg2rad
        elevation = pos_y * deg2rad
        x = radius * math.sin(elevation) * math.cos(azimuth)
        y = radius * math.sin(elevation) * math.sin(azimuth)
        z = radius * math.cos(elevation)

        x = round(x, 2)
        y = round(y, 2)
        z = round(z, 2)

        #print("x=", x)
        #print("y=", y)
        #print("z=", z)

        xlist.append(x)
        ylist.append(y)
        zlist.append(z)

        ax.scatter(xlist[j],ylist[j],zlist[j])
        j+=1
        plt.show()
        plt.pause(0.0001)

    #Go to initial position
    pi.set_servo_pulsewidth(servo1, 1500)
    pi.set_servo_pulsewidth(servo2, 1500)

    #Stop signal
    pi.stop()
    print("--- %s seconds ---" % (time.time() - start_time))
else:
    start_time = time.time()

    plt.ion() #
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    j=0

    pi.set_servo_pulsewidth(servo1, AngleToPWM(pos_x))
    pi.set_servo_pulsewidth(servo2, AngleToPWM(pos_y))
    while pos_y > max_pos_y:

        if max_pos_x > min_pos_x:
            for pos_x in np.arange(min_pos_x, max_pos_x, inc_step_x):
                pwm = AngleToPWM(pos_x)
                pi.set_servo_pulsewidth(servo1, pwm)
                time.sleep(delay_x)
                #print(pos_x)
                radius = get_dist()
                azimuth = pos_x * deg2rad
                elevation = pos_y * deg2rad
                x = radius * math.sin(elevation) * math.cos(azimuth)
                y = radius * math.sin(elevation) * math.sin(azimuth)
                z = radius * math.cos(elevation)

                x = round(x, 2)
                y = round(y, 2)
                z = round(z, 2)

                #print("x=", x)
                #print("y=", y)
                #print("z=", z)

                xlist.append(x)
                ylist.append(y)
                zlist.append(z)

                ax.scatter(xlist[j],ylist[j],zlist[j])
                j+=1
                plt.show()
                plt.pause(0.0001)

        duty = AngleToPWM(pos_y)
        pi.set_servo_pulsewidth(servo2, duty)
        time.sleep(delay_y)
        pos_y = pos_y - inc_step_y
        print(pos_y)
        radius = get_dist()
        azimuth = pos_x * deg2rad
        elevation = pos_y * deg2rad
        x = radius * math.sin(elevation) * math.cos(azimuth)
        y = radius * math.sin(elevation) * math.sin(azimuth)
        z = radius * math.cos(elevation)

        x = round(x, 2)
        y = round(y, 2)
        z = round(z, 2)

        #print("x=", x)
        #print("y=", y)
        #print("z=", z)

        xlist.append(x)
        ylist.append(y)
        zlist.append(z)

        ax.scatter(xlist[j],ylist[j],zlist[j])
        j+=1
        plt.show()
        plt.pause(0.0001)

        if max_pos_x > min_pos_x:
            for pos_x in np.arange(max_pos_x, min_pos_x, -inc_step_x):
                pwm = AngleToPWM(pos_x)
                pi.set_servo_pulsewidth(servo1, pwm)
                time.sleep(delay_x)
                #print(pos_x)
                radius = get_dist()
                azimuth = pos_x * deg2rad
                elevation = pos_y * deg2rad
                x = radius * math.sin(elevation) * math.cos(azimuth)
                y = radius * math.sin(elevation) * math.sin(azimuth)
                z = radius * math.cos(elevation)

                x = round(x, 2)
                y = round(y, 2)
                z = round(z, 2)

                #print("x=", x)
                #print("y=", y)
                #print("z=", z)

                xlist.append(x)
                ylist.append(y)
                zlist.append(z)

                ax.scatter(xlist[j],ylist[j],zlist[j])
                j+=1
                plt.show()
                plt.pause(0.0001)


        duty = AngleToPWM(pos_y)
        pi.set_servo_pulsewidth(servo2, duty)
        time.sleep(delay_y)
        pos_y = pos_y - inc_step_y
        #print(pos_y)
        radius = get_dist()
        azimuth = pos_x * deg2rad
        elevation = pos_y * deg2rad
        x = radius * math.sin(elevation) * math.cos(azimuth)
        y = radius * math.sin(elevation) * math.sin(azimuth)
        z = radius * math.cos(elevation)

        x = round(x, 2)
        y = round(y, 2)
        z = round(z, 2)

        print("x=", x)
        print("y=", y)
        print("z=", z)

        xlist.append(x)
        ylist.append(y)
        zlist.append(z)

        ax.scatter(xlist[j],ylist[j],zlist[j])
        j+=1
        plt.show()
        plt.pause(0.0001)

    #Go to initial position
    pi.set_servo_pulsewidth(servo1, 1500)
    pi.set_servo_pulsewidth(servo2, 1500)

    #Stop signal
    pi.stop()
    print("--- %s seconds ---" % (time.time() - start_time))

#print(xlist)
#print(ylist)
#print(zlist)

csvfile=open('Mapping_data.txt','w', newline='')
obj=csv.writer(csvfile)
obj.writerow(xlist)
obj.writerow(ylist)
obj.writerow(zlist)
csvfile.close()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X')
ax.set_xlim(-400, 400)
ax.set_ylabel('Y')
ax.set_ylim(-10, 500)
ax.set_zlabel('Z')
ax.set_zlim(-100, 400)
#plt.xlim((-300,300))
#plt.ylim((-300,300))

ax.scatter(xlist, ylist, zlist)
pickle.dump(fig, open('Mapp_lidar.fig.pickle', 'wb'))
plt.show()