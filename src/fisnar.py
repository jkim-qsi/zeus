import logging
import signal
import time
from time import sleep
from colorama import init, Fore, Back, Style
from threading import Thread, Lock
import sys
import traceback
import serial



class Fisnar(object):
    ser = None    

    def __init__(self, port='COM6'):
        init()
        
        self.ser = serial.Serial(port=port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=2, xonxoff=0, rtscts=0)
        print('Serial port initialized')
    
    def status(self):
        print('Machine status')
        self.ser.write('MS\r'.encode('ascii'))
        sleep(2.0)
        # received = self.ser.read_until(size=4) #expected='!', size=10)
        # print(received)
        # received = self.ser.read_until(size=5) #expected='!', size=10)
        # print(received)
        
        received = self.ser.read(size=8) #expected='!', size=10)
        print(received)
        
        return
    
    def home_motors(self):
        print('Homing motors')
        self.ser.write('HM\r'.encode('ascii'))
        # received = self.ser.read_until(size=5) #expected='!', size=10)
        # print(received)
        
        sleep(1.0)
        
        received = self.ser.read(size=6) #expected='!', size=10)
        print(received)
        return
    
    def moveX(self, x):
        print('Move X to {}'.format(x))
        command = 'MX {:.3f}\r'.format(x)
        print(command)
        for ch in command.encode('ascii'):
            self.ser.write(ch)
            sleep(0.1)
        received = self.ser.read(size=6) #expected='!', size=10)
        print(received)
        return
        
    def moveY(self, y):
        print('Move Y to {}'.format(y))
        command = 'MY({:.1f})\r'.format(y)
        print(command)
        self.ser.write(command.encode('ascii'))
        received = self.ser.read_until(size=5) #expected='!', size=10)
        print(received)
        return
    
    def moveZ(self, z):
        print('Move Z to {}'.format(z))
        command = 'MZ({:.3f})\r'.format(z)
        print(command)
        self.ser.write(command.encode('ascii'))
        received = self.ser.read_until(size=5) #expected='!', size=10)
        print(received)
        return
    
    def currX(self):
        # print('Move Z to {}'.format(z))
        command = 'PX\r'
        print(command)
        self.ser.write(command.encode('ascii'))
        received = self.ser.read(size=10) #expected='!', size=10)
        print(received)
        return
    
    def flush_input_buffer(self):
                
        received = self.ser.read(self.ser.in_waiting)
        
        print(received)
        
        return 
    
    
    def __del__(self):
        self.ser.close()
        