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

# # Set parameters
# zm.setDeckGeometryParameters(deck)
# sleep(0.5)
# zm.setContainerGeometryParameters(water_container)
# sleep(0.5)
# zm.setLiquidClassParameters(lc_water_300uL)
# sleep(0.5)
# zm.setCalibrationCurveParameters(cc_water_300uL_aspirate)
# sleep(0.5)
# zm.setCalibrationCurveParameters(cc_water_300uL_dispense)
# sleep(0.5)

# input("Place tips under pipette head and press any key to continue")
# # zm.pickUpTip(4, 0) # tip type 4: 300uL conductive non-filtered
# zm.pickUpTip(5, 0) # tip type 5: 300uL conductive filtered


input("Place sample container under pipette head and press any key to continue")
zm.moveZDrive(1300, speed=900)
sleep(2.0)
zm.simpleAspirate(volume=300)
sleep(2.0)
zm.moveZDrive(600, speed=800) #preset_speed='slow')


input("Remove sample container under pipette head and position chip")
# zm.bottomSearch(start=1900, stop=2500)
zm.moveZDrive(1800, speed=900)
sleep(3.0)
zm.moveZDrive(1985, speed=100)
sleep(3.0)

for idx in range(9):
    print('{} out of 9'.format(idx))
    zm.simpleDispense(volume=290)
    sleep(1.5)
    zm.simpleAspirate(volume=290)
    sleep(1.5)
zm.simpleDispense(volume=300)
sleep(1.5)

# reset
zm.moveZDrive(600, speed=900)
sleep(10.0)
# zm.simpleDispense(volume=300)

# zm.aspiration(aspirationVolume=300, deckGeometryTableIndex=0, liquidClassTableIndex=23, lld=1)
# zm.aspirate_lld(aspirationVolume=300, deckGeometryTableIndex=0, liquidClassTableIndex=23)
# zm.getErrorCode()
# input("Position chip under pipette head and press any key to continue")

# zm.initZDrive()

# Define deck and container geometry

# ez = ezstepper.EZStepper(1)


# def demo():
#     # ez.setVelocity(3)
#     # zm.moveZDrive(0, "fast")
#     # ez.moveAbsolute(0)
#     sleep(1)
#     zm.moveZDrive(1000, "fast")
#     for i in range(0, 6):
#         zm.moveZDrive(1400, "fast")
#         zm.moveZDrive(1500, "slow")
#         zm.moveZDrive(1000, "fast")
#         # ez.moveRelative(14.5)
#         sleep(1)
#     zm.moveZDrive(1400, "fast")
#     zm.moveZDrive(1500, "slow")
#     zm.moveZDrive(1000, "fast")
#     # ez.moveAbsolute(0)
#     zm.moveZDrive(0, "slow")

# if __name__ == '__main__':
#     demo()

# %%
