from time import sleep
from colorama import init, Fore, Back, Style
import traceback
import serial
import re



class CitizenScale(object):
    ser = None

    def __init__(self, port='COM7'):
        init()
        
        self.ser = serial.Serial(port=port, baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=2, xonxoff=0, rtscts=0)
        print('Serial port initialized')
    
    def status(self):
        pass
    
    def tare(self):
        self.ser.write('[T]\r'.encode('ascii'))
        
        received = self.ser.read_until(expected='\r') #expected='!', size=10)
        print(received)
        match = re.search('Done', str(received))
        if match is None:
            print('Tare response from scale not received.')
            return -1
        else:
            print('Tare successful.')
            return 0
    
    def measure(self, verbose=False):
        self.ser.write('[W]\r'.encode('ascii'))
        
        received = self.ser.read_until(expected='\r') #expected='!', size=10)
        if verbose:
            print(received)
        
        match = re.search('\s+([-+])\s+([\d.]+) ([a-zA-Z]+)', str(received))
        
        # print(match)
        if match is not None:
            sign = match[1]
            value = float(match[2])
            unit = match[3]
            
            if sign == '-':
                value *= -1
                        
            # print(value)
            # print(unit)
                
            return value, unit
        else:
            return -1, -1
    
    def flush_input_buffer(self):
                
        received = self.ser.read(self.ser.in_waiting)
        
        print(received)
       
        
        return 
    
    
    def __del__(self):
        self.ser.close()
        