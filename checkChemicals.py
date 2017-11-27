import constants
import math

inc = constants.inc
dec = constants.dec
GivenWaterVolume = constants.GivenWaterVolume
CH = constants.CH
CYA = constants.CYA
pH = constants.pH
TA = constants.TA
Borate = constants.Borate
FC = constants.FC

# calculate from pool dimensions, stored in DB
water = 10000.00

# change = [CH, CYA, Borate, FC]

FreeChlorine = constants.FreeChlorine

TotalAlkalinity = constants.TotalAlkalinity

CyanuricAcid = constants.CyanuricAcid

CalciumHardness = constants.CalciumHardness

Borates = constants.Borates

Salt = constants.Salt

optimalValuesMin = constants.optimalValuesMin
optimalValuesMax = constants.optimalValuesMax

chemicalDict = {CYA: CyanuricAcid, CH: CalciumHardness, TA: TotalAlkalinity, FC: FreeChlorine, Borate: Borates}


def inRange(val, min, max):
    if val > max or val < min:
        return False
    else:
        return True


def checkLevelOk(val, level):
    return inRange(level, optimalValuesMin[val], optimalValuesMax[val])


def val_cal(amountChemical, changeReq, changeVal):
    poolFactor = water / GivenWaterVolume
    changeFactor = changeReq / changeVal
    return round(poolFactor * changeFactor * amountChemical, 2)


def calc(listOfChem, change):
    s = val_cal(listOfChem[3], change, listOfChem[2])
    print('Need to add ', s, 'oz of ', listOfChem[0])

def get_min_fc(cyaLevel):
    return (optimalValuesMin[FC] / 100) * cyaLevel

def get_ideal_fc(cyaLevel):
    return (optimalValuesMax[FC] / 100) * cyaLevel


def checkFC(level, cyaLevel):
    # minV = get_min_fc(cyaLevel)
    # maxV = get_ideal_fc(cyaLevel)
    return inRange(level, get_min_fc(cyaLevel), get_ideal_fc(cyaLevel))


def higher_or_lower(val, level):
    if level > optimalValuesMax[val]:
        return True
    elif level < optimalValuesMin[val]:
        return False


def getValueToRise(val, level):
    chem = chemicalDict[val]
    change = optimalValuesMax[val] - level
    print(optimalValuesMax[val])
    for item in chem:
        calc(item, change)


def checkpHandTA(TAlevel, pHval, borate_level):
    if checkLevelOk(pH, pHval) and checkLevelOk(TA, TAlevel):
        return True
    elif checkLevelOk(pH, pHval) and TAlevel < 70:
        s = val_cal(22.4, (90 - TAlevel), 10)
        print('Need to add ', s, ' oz of Baking Soda')
        return False
    else:
        calc_ph(pHval, borate_level, TAlevel)
        return False


# def handlepHconversion(pHval,TAval):
#     water_liters = water * 3.785
#     print('waterLiters',water_liters)
#     current_hydronium_molarity = 10**-pHval#-math.log10(pHval)#math.pow(10,-pHval)
#     print('phval',-math.log10(current_hydronium_molarity))
#     print(current_hydronium_molarity)
#     perfect_phmolarity = 10**-7.5#-math.log10(7.5)#math.pow(10,-7.5)
#     print(perfect_phmolarity)
#     density_muriatic_acid = 1.16 #g/ml
#     molarity_acid = density_muriatic_acid*(31.5/100)*(1/36.45)*1000
#     print(molarity_acid)
#     print('phAcid',-math.log10(molarity_acid))
#     v_to_be_added = water_liters*(perfect_phmolarity - current_hydronium_molarity) /(molarity_acid - perfect_phmolarity)
#     print(v_to_be_added)
#     v_to_be_added_oz = v_to_be_added*33.184
#     print(v_to_be_added_oz)
#     changed_ta = TAval - (v_to_be_added_oz*GivenWaterVolume*10)/(water * 26.6)
#     print('changedTA',changed_ta)
#     if(checkLevelOk(TA,changed_ta)):
#         return v_to_be_added_oz
#     else:
#         getValueToRise(TA, changed_ta)
#         return v_to_be_added_oz

# vol  = handlepHconversion(8.5,80)
# print(vol)


def calc_ph(ph_val, borate_level, ta_level):
    mamul = [2.0, 1.11111, 1.0, .909091, 1.08448, 2.16897]
    acids = ['15.7% - 10 Baume', '28.3% - 18 Baume', '31.45% - 20 Baume', '34.6% - 22 Baume', '29%', '14.5%']
    delta = 7.5 - ph_val
    delta *= water
    temp = (ph_val + 7.5) / 2
    adj = ((192.1626 + -60.1221 * temp + 6.0752 * math.pow(temp, 2) + -0.1943 * math.pow(temp, 3)) * (
    ta_level + 13.91)) / 114.6
    extra = (-5.476259 + 2.414292 * temp + -0.355882 * math.pow(temp, 2) + 0.01755 * math.pow(temp, 3)) * int(
        borate_level)
    extra *= delta
    delta *= adj
    if ph_val < 7.2:
        # Washing soda, soda ash
        washing_soda = (delta / 218.68) + (extra / 218.68)
        washing_soda_vol = washing_soda * 0.8715
        print('Washing Soda to be added by volume', round(washing_soda_vol), 'oz')
        print('Washing Soda to be added by weight', round(washing_soda), 'oz')
        # Borax
        borate_need = (delta / 110.05) + (extra / 110.05)
        borate_need_vol = borate_need * 0.9586
        print('Borate to be added by volume', round(borate_need_vol), 'oz')
        print('Borate to be added by weight', round(borate_need), 'oz')
    if ph_val > 7.8:
        for i in range(6):
            # Muriatic acid
            volume_of_acid = (delta / -240.15 * mamul[i]) + (extra / -240.15 * mamul[i])
            print('Volume of', acids[i], 'muriatic acid to be added', round(volume_of_acid), 'oz')

        # Dry acid
        weight_of_acid = (delta / -178.66) + (extra / -178.66);
        volume = weight_of_acid * 0.6657
        print('Volume of dry acid by weight to be added', round(volume), 'oz')


# waterflow in gallons per minute, returns hours
def water_turn_over_time(pump_flow):
    return round((water / pump_flow) / 60)


#calc_ph(6.5, 0, 100, 2)
print(water_turn_over_time(11), 'hours')


def calc_drain_water_vol(desired_ppm, actual_ppm):
    return round(water * ((actual_ppm-desired_ppm) / actual_ppm))


print('Drain', calc_drain_water_vol(50, 100), 'gallons and replace with new')
