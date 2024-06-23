#%%
import zeus
# import ezstepper
# import fisnar
import snapmaker
import citizenscale
from time import sleep
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#%%

# Initialize gantry
sm = snapmaker.Snapmaker(port='COM8')
# sm.home_motors()
sm.flush_input_buffer()

# Initialize scale
cs = citizenscale.CitizenScale(port='COM7')

# Initialize pipette head
zm = zeus.ZeusModule(1, init_module=False, discard_tip=False) # 1 is set by the jumper on the Zeus X1 module
# zm = zeus.ZeusModule(1, init_module=True, discard_tip=True) # 1 is set by the jumper on the Zeus X1 module
#%%
deck = zeus.DeckGeometry(index=0, endTraversePosition=1300, beginningofTipPickingPosition=1600, positionofTipDepositProcess=1600)
zm.setDeckGeometryParameters(deck)
#%%
# water_container = zeus.ContainerGeometry(index=0, diameter=200, bottomSection=10000, bottomPosition=1550, immersionDepth=50)
# zm.setContainerGeometryParameters(water_container)
#%%
# container for scale
water_container = zeus.ContainerGeometry(index=1, diameter=200, bottomSection=10000, bottomPosition=2050, immersionDepth=20)
zm.setContainerGeometryParameters(water_container)

#%%
# Liquid class 23 for 300uL clear tip with filter
lc_water_300uL = zeus.LiquidClass(index=23, liquidClassForFilterTips=1, \
                                  aspirationMode=0, aspirationFlowRate=500, aspirationSwapSpeed=1000, aspirationSettlingTime=20, \
                                  lld=1, clldSensitivity=1, plldSensitivity=2, \
                                  dispensingMode=0, dispensingFlowRate=500, stopFlowRate=500, dispensingSettlingTime=10, \
                                  blowoutAirVolume=1500,
                                  )
zm.setLiquidClassParameters(lc_water_300uL)
#%%
# cc_water_300uL_aspirate = zeus.calibrationCurve(index=lc_water_300uL.index, direction='aspirate')
# zm.setCalibrationCurveParameters(cc_water_300uL_aspirate)

# # default for calibration
# cc_water_300uL_aspirate_forcal = zeus.calibrationCurve(index=lc_water_300uL.index, direction='aspirate', \
#                                                 target_volumes =  [0, 50, 100, 200, 500, 1000, 2000, 3000], \
#                                                 actual_volumes = [0, 50, 100, 200, 500, 1000, 2000, 3000])
# zm.setCalibrationCurveParameters(cc_water_300uL_aspirate_forcal)

# Calibrated on 6/23/2024
cc_water_300uL_aspirate_cal = zeus.calibrationCurve(index=lc_water_300uL.index, direction='aspirate', \
                                                target_volumes =  [0, 50, 100, 250, 500, 1250, 2000, 3000], \
                                                actual_volumes = [0, 49, 97, 216, 478, 1210, 1962, 2947])
zm.setCalibrationCurveParameters(cc_water_300uL_aspirate_cal)


#%%
# cc_water_300uL_dispense = zeus.calibrationCurve(index=lc_water_300uL.index, direction='dispense')
# zm.setCalibrationCurveParameters(cc_water_300uL_dispense)

# default for calibrationf
cc_water_300uL_dispense_forcal = zeus.calibrationCurve(index=lc_water_300uL.index, direction='dispense', \
                                                target_volumes =  [0, 50, 100, 200, 500, 1000, 2000, 3000], \
                                                actual_volumes = [0, 50, 100, 200, 500, 1000, 2000, 3000])
zm.setCalibrationCurveParameters(cc_water_300uL_dispense_forcal)



#%%

# zm.moveZDrive(2000, speed=400)

#%%
# motor position parameters
sm_pos = {
    'park':       [0, 253, 175],
    'tip_pickup': [-3.1,   246.5, 95],
    'over_scale': [205, 193, 175],
    
}
zm_z = {
    'travel': 1000,
    'surface': 2025,
    'aspirate': 2040,
    # 'dispense': 2040 # on small plate
    'dispense': 1700 # in water bottle
}
zm_speed = 400
# sm_z = {
#     'tip_pickup': 175,
#     'over_scale: 175
# }
# sm_y = {
#     'tip_pickup': 193,
#     'over_scale': 193
# }
# sm_x = {
#     'tip_pickup': 5,
#     'over_scale': 115,
#     }
#%%

# Pipette tip tray 
# input('Press any key to pickup tip')
# sm.move((sm_x['tip_pickup'], sm_y, sm_z))
sm.move(sm_pos['park'])

sm.move(sm_pos['tip_pickup'])

#%%
# sm.move(sm_pos['park'])
#%%

# sleep(1.0)
zm.pickUpTip(5, 0) # tip type 5: 300uL conductive filtered)
sleep(5.0)
sm.move(sm_pos['park'])
#%%

#%%
# water container position
# sm.move((sm_x['over_scale'], sm_y, sm_z))


sm.move(sm_pos['over_scale'])
#%%

zm.moveZDrive(1000, speed=zm_speed)


#%%
###### Cell for calibrating aspiration
# 50 / 100/ 250/ 500/ 750/ 1250/ 2000/ 3000
asp_volume = 3000
repeat = 10
cal_data = []
zm_speed_dis = 1300

# liquid_level = -1
    
for rep in range(repeat):
    cs.tare()
    
    if liquid_level == -1:
        zm.aspirate_lld(aspirationVolume=asp_volume, containerGeometryTableIndex=water_container.index,
                        deckGeometryTableIndex=deck.index, liquidClassTableIndex=lc_water_300uL.index, 
                        lldSearchPosition=1800)
        sleep(5.0)
    else:
        print('Found liquid level at {}'.format(liquid_level))
        zm.moveZDrive(liquid_level + water_container.immersionDepth, speed=zm_speed_dis)
        sleep(5.0)
        cs.tare()
        sleep(1.0)
        flowrate = 500
        asp_time = 3 + asp_volume/flowrate
        zm.simpleAspirate(asp_volume, flowrate=flowrate)
        
        # zm.aspirate_at(aspirationVolume=asp_volume, containerGeometryTableIndex=water_container.index,
        #                 deckGeometryTableIndex=deck.index, liquidClassTableIndex=lc_water_300uL.index, 
        #                 liquidSurface=liquid_level + water_container.immersionDepth)  
        sleep(asp_time)  
        zm.moveZDrive(1500, speed=zm_speed_dis)
        
        sleep(1.0)
    remain_vol = asp_volume

    data = []
    for sample in range(10):    
        sleep(0.5)
        value, unit = cs.measure()
        data.append(value)
        print('Measurement {}={} {}'.format(sample, value, unit))

    # #%%

    print(data)
    data_arr = np.array(data)
    cal_data.append(np.mean(data_arr[data_arr < -asp_volume/10/2]))
    print(cal_data[-1])

    fig, ax = plt.subplots()
    ax.plot(data)
    ax.set(xlabel='samples', ylabel='Mass ({})'.format(unit))
    plt.tight_layout()
    plt.show()
    
    disp_flowrate = 1000
    disp_time = 3.0+ asp_volume / disp_flowrate
    zm.simpleDispense(asp_volume, flowrate=1000)
    # sleep(2.0)
    # zm.clear_tip(dispensingVolume=5, containerGeometryTableIndex=water_container.index,
    #                 deckGeometryTableIndex=deck.index, liquidClassTableIndex=lc_water_300uL.index,
    #                 dispenseHeight=1500)
    sleep(disp_time)
    
    liquid_level = zm.liquid_level
    print('Found liquid level at {}'.format(liquid_level))
    print('Rep {}'.format(rep))
    
    df =pd.DataFrame({'data': cal_data}) 
    df.to_clipboard(index=False)
    display(df)
    
    
# print(cal_data)
print(np.mean(cal_data))


#%%
    # zm.simpleDispense(asp_volume)
    


#%%

###### Cell for calibrating dispense
eval_volume = 250

asp_volume = 3000
repeat = 11
cal_data = []
zm_speed_dis = 1300

# liquid_level = -1
    
cs.tare()
sleep(2.0)

remain_vol = 0

for rep in range(repeat):    
    if remain_vol < eval_volume:
        print('out of liquid in pipette tip, aspirating')
        
        zm.simpleDispense(volume=remain_vol)
        sleep(2.0)
        zm.moveZDrive(1800, speed=zm_speed)
        sleep(2.0)
        
        if zm.liquid_level == -1:
            zm.aspirate_lld(aspirationVolume=asp_volume, containerGeometryTableIndex=water_container.index,
                        deckGeometryTableIndex=deck.index, liquidClassTableIndex=lc_water_300uL.index, 
                        lldSearchPosition=1800)
            asp_time = asp_volume / lc_water_300uL.aspirationFlowRate + 12
            sleep(asp_time)
        else:
            zm.moveZDrive(zm.liquid_level + water_container.immersionDepth, speed=zm_speed_dis)
            sleep(2.0)
            asp_flowrate = 500
            asp_time = asp_volume / asp_flowrate + 3
            
            zm.simpleAspirate(asp_volume, flowrate = asp_flowrate)
            sleep(asp_time)
            zm.moveZDrive(1500, speed=zm_speed_dis)
            sleep(2.0)

        remain_vol = asp_volume
                
    if zm.liquid_level != -1:
        display('Found liquid level at {}'.format(zm.liquid_level))
        dispense_z = zm.liquid_level
    else:
        dispense_z = zm_z['dispense']
        
    zm.moveZDrive(dispense_z, speed=zm_speed_dis)
    sleep(5.0)
        
    cs.tare()
    sleep(2.0)
    
    dis_flowrate = 500
    dis_time = eval_volume / disp_flowrate + 3.0
    zm.simpleDispense(volume=eval_volume, flowrate=dis_flowrate)
    remain_vol -= eval_volume
    
    sleep(dis_time)
    zm.moveZDrive(dispense_z-100, speed=zm_speed_dis)
    
    sleep(1.0)    
    
    data = []
    for sample in range(10):    
        sleep(0.5)
        value, unit = cs.measure()
        data.append(value)
        print('Measurement {}={} {}'.format(sample, value, unit))

    # #%%

    print(data)
    data_arr = np.array(data)
    cal_data.append(np.mean(data_arr[data_arr > eval_volume/10/2]))
    # print(cal_data[-1])

    fig, ax = plt.subplots()
    ax.plot(data)
    ax.set(xlabel='samples', ylabel='Mass ({})'.format(unit))
    plt.tight_layout()
    plt.show()
    
    df =pd.DataFrame({'data': cal_data}) 
    df.to_clipboard(index=False)
    display(df)
    

zm.moveZDrive(1500, speed=zm_speed_dis)
sleep(2.0)
zm.simpleDispense(volume=remain_vol)
sleep(2.0)
    


#%%
volume = 2000
zm.dispense_lld(dispensingVolume=volume, containerGeometryTableIndex=water_container.index,
                   deckGeometryTableIndex=deck.index, liquidClassTableIndex=lc_water_300uL.index,
                   lldSearchPosition=1500) 
# , liquidSurface=0,
#                    searchBottomMode=0, mixVolume=0, mixFlowRate=0, mixCycles=0):

#%%
zm.moveZDrive(zm_z['aspirate'], speed=zm_speed)
sleep(5.0)
#%%
zm.simpleAspirate(volume=100)

# sleep(5.0)
#%%
zm.moveZDrive(zm_z['dispense'], speed=zm_speed)


#%%
zm.moveZDrive(zm_z['travel'], speed=zm_speed)

#%%
volume = 2000
# zm.moveZDrive(zm_z['dispense'], speed=zm_speed)

zm.simpleDispense(volume=volume)
#%%

#%%
zm.simpleDispense(volume=290)

#%%
#%%
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
