# -*- coding: utf-8 -*
import serial
import time

ser = serial.Serial("/dev/ttyUSB0", 115200)

def get_dist():
    while True:
        time.sleep(0.1)
        count = ser.in_waiting
        if count > 8:
            recv = ser.read(9)  
            ser.reset_input_buffer()  
            #type(recv), 'str' in python2(recv[0] = 'Y'), 'bytes' in python3(recv[0] = 89)
            #type(recv[0]), 'str' in python2, 'int' in python3 
            
            if recv[0] == 0x59 and recv[1] == 0x59:     #python3
                distance = recv[2] + recv[3] * 256
                strength = recv[4] + recv[5] * 256
                #print('(', distance, ',', strength, ')')
                ser.reset_input_buffer()
                return distance               
                                   
if __name__ == '__main__':
    try:
        if ser.is_open == False:
            ser.open()
        get_dist()
    except KeyboardInterrupt:   # Ctrl+C
        if ser != None:
            ser.close()