#%%
# import zeus
# import ezstepper
# import fisnar
import snapmaker
import os
from time import sleep

# os.add_dll_directory(R"C:\Users\Lab\Downloads\usb2can_canal_v2.0.0\usb2can_canal_v2.0.0\x64\Release")

sm = snapmaker.Snapmaker(port='COM8')

sm.flush_input_buffer()

# Pipette 0,0 tray position
# sm.move((86.3, 193.1, 87))

# water container position
sm.move((86.3, 193.1, 87))

# fn.status()
# sleep(1.0)

# sm.home_motors()
# sleep(5.0)

sm.move((None, 100.0, None))
# fn.currX()
# sleep(1.0)
# fn.home_motors()
# sleep(1.0)
# fn.moveX(x=10)
# sleep(2.0)
sm.flush_input_buffer()

# %%
