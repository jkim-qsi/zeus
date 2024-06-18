#%%
import zeus
# import ezstepper
import os
from time import sleep

# os.add_dll_directory(R"C:\Users\Lab\Downloads\usb2can_canal_v2.0.0\usb2can_canal_v2.0.0\x64\Release")

zm = zeus.ZeusModule(1, init_module=True, discard_tip=False) # 1 is set by the jumper on the Zeus X1 module

deck = zeus.DeckGeometry(index=0, endTraversePosition=600, beginningofTipPickingPosition=1100, positionofTipDepositProcess=1200)
water_container = zeus.ContainerGeometry(index=0, diameter=200, bottomSection=10000, bottomPosition=1800, immersionDepth=20)

# Liquid class 23 for 300uL clear tip with filter
lc_water_300uL = zeus.LiquidClass(index=23, liquidClassForFilterTips=1, \
                                  aspirationMode=0, aspirationFlowRate=500, aspirationSwapSpeed=1000, aspirationSettlingTime=10, \
                                  lld=1, plldSensitivity=3, \
                                  dispensingMode=0, dispensingFlowRate=500, stopFlowRate=500, dispensingSettlingTime=10 \
                                  )
cc_water_300uL_aspirate = zeus.calibrationCurve(index=lc_water_300uL.index, direction='aspirate')
cc_water_300uL_dispense = zeus.calibrationCurve(index=lc_water_300uL.index, direction='dispense')

# reset
# zm.moveZDrive(1800, speed=900)
# zm.moveZDrive(1980, speed=100)
# sleep(2.0)
# zm.moveZDrive(1980, speed=100)

zm.moveZDrive(600, speed=900)


# sleep(5.0)
# input('Press any key to dispense')
# zm.simpleDispense(volume=300)
# sleep(1.0)

# %%
