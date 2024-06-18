import logging
import signal
import time
from time import sleep
from colorama import init, Fore, Back, Style
from threading import Thread, Lock
import sys
import traceback
import serial



class Snapmaker(object):
    ser = None    
    safeZ=200.0

    def __init__(self, port='COM8'):
        init()
        
        self.ser = serial.Serial(port=port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=2, xonxoff=0, rtscts=0)
        print('Serial port initialized')
    
    def status(self):
        pass
    
    def home_motors(self):
        print('Homing motors')
        print(' Home Z first to prevent collisions')
        self.ser.write('G28 Z\r'.encode('ascii'))
        sleep(5.0)
        print(' Home XY')
        self.ser.write('G28 X Y\r'.encode('ascii'))
        sleep(5.0)
        # received = self.ser.read_until(size=5) #expected='!', size=10)
        # print(received)       
        
        
        received = self.ser.read() #size=6) #expected='!', size=10)
        print(received)
        return
    
    def move(self, coord=[None, None, None]):
        
        axis = ('X', 'Y', 'Z')
        print('Move to X,Y,Z coordinates: {}'.format(coord))
        
        
        command = 'G0'
        for idx, pos in enumerate(coord):
            if pos is not None:
                command += ' {}{:.1f}'.format(axis[idx], pos)
        command += '\r'
        
        print(command)
        self.ser.write(command.encode('ascii'))
        # sleep(2.0)
        
        received = self.ser.read_until(expected='\n') #expected='!', size=10)
        print(received)
        
        return

    def goToSafeZ(self):
        self.move([None, None, self.safeZ])
        return
    
    def flush_input_buffer(self):
                
        received = self.ser.read(self.ser.in_waiting)
        
        print(received)
        
        return 
    
    
    def __del__(self):
        self.ser.close()
        