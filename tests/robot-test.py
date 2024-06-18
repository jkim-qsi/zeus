#%%
import zeus
# import ezstepper
# import fisnar
import snapmaker
import os
from time import sleep

# Initialize gantry
sm = snapmaker.Snapmaker(port='COM8')
# sm.home_motors()
sm.flush_input_buffer()


# Initialize pipette head
zm = zeus.ZeusModule(1, init_module=True, discard_tip=True) # 1 is set by the jumper on the Zeus X1 module

deck = zeus.DeckGeometry(index=0, endTraversePosition=600, beginningofTipPickingPosition=1800, positionofTipDepositProcess=1800)
water_container = zeus.ContainerGeometry(index=0, diameter=200, bottomSection=10000, bottomPosition=1550, immersionDepth=20)

# Liquid class 23 for 300uL clear tip with filter
lc_water_300uL = zeus.LiquidClass(index=23, liquidClassForFilterTips=1, \
                                  aspirationMode=0, aspirationFlowRate=500, aspirationSwapSpeed=1000, aspirationSettlingTime=10, \
                                  lld=1, plldSensitivity=3, \
                                  dispensingMode=0, dispensingFlowRate=500, stopFlowRate=500, dispensingSettlingTime=10 \
                                  )
cc_water_300uL_aspirate = zeus.calibrationCurve(index=lc_water_300uL.index, direction='aspirate')
cc_water_300uL_dispense = zeus.calibrationCurve(index=lc_water_300uL.index, direction='dispense')



# Pipette tip tray 0,0 position
input('Press any key to pickup tip')
sm.move((86.3, 193.1, 87))
sleep(1.0)
zm.pickUpTip(5, 0) # tip type 5: 300uL conductive filtered)

# water container position
# sm.move((83.3, 143.1, 87))

# # 2mL Vial rack 0,0 position
# liquid_level = 1550
# liquid_volume = 30 # uL

# input('Press any key to aspirate')
# sm.move((168.3, 197.1, 87))
# sleep(10.0)
# zm.moveZDrive(liquid_level, speed=900)
# sleep(2.0)
# zm.simpleAspirate(volume=int(liquid_volume*10))
# sleep(2.0)
# zm.moveZDrive(600, speed=800) #preset_speed='slow')

# input('Press any key to move to dispense into left flow cell port')
# # Chip position 
# chipZ = 2135
# flowcell_pos = (85.5, 79.3, 87)
# #  left top flowcell port
# sm.move(flowcell_pos)
# zm.moveZDrive(2100, speed=900)
# sleep(3.0)
# zm.moveZDrive(chipZ, speed=100)
# sleep(3.0)

# for idx in range(9):
#     print('{} out of 9'.format(idx))
#     zm.simpleDispense(volume=290)
#     sleep(1.5)
#     zm.simpleAspirate(volume=290)
#     sleep(1.5)
# zm.simpleDispense(volume=300)
# sleep(1.5)

# # reset
# zm.moveZDrive(600, speed=900)
# sleep(10.0)

# # #  right top flowcell port
# # sm.move((95.5, 79.3, 87))



# # fn.status()
# # sleep(1.0)

# # sm.home_motors()
# # sleep(5.0)

# # sm.move((None, 100.0, None))
# # fn.currX()
# # sleep(1.0)
# # fn.home_motors()
# # sleep(1.0)
# # fn.moveX(x=10)
# # sleep(2.0)
# sm.flush_input_buffer()

# %%
