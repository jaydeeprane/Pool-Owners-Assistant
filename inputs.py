import checkChemicals
import constants

def check_calculate(val, level):
    if not checkChemicals.checkLevelOk(val, level):
        if checkChemicals.higher_or_lower(val, level):
            print('Drain', checkChemicals.calc_drain_water_vol(constants.optimalValuesMax[val], level), 'gallons and replace with new')
            return True
        else:
            checkChemicals.getValueToRise(val, level)
            return True
    return False

def cal_fc (level, cyalevel):
    if level > checkChemicals.get_ideal_fc(cyalevel):
        print('Drain', checkChemicals.calc_drain_water_vol(checkChemicals.get_ideal_fc(cyalevel), level),'gallons and replace with new')
    else:
        listOfChems = constants.FreeChlorine
        needed_rise = checkChemicals.get_ideal_fc(cyalevel) - level
        for chem in listOfChems:
            s = checkChemicals.val_cal(chem[3], needed_rise, chem[2])
            print('Need to add ', s, 'oz of ', chem[0])
    return True

good_to_go = False
water = float(input('Gallons of water: '))
checkChemicals.water = water
calFlag = True
cyaFlag = True
borateFlag = True
pHTAFlag = True
fcFlag = True

while(not good_to_go):
    if calFlag:
        calHardness = float(input('Enter the calcium hardness levels: '))
        val = constants.CH
        cost = 3 #per OZ
        if check_calculate(val, calHardness):
            continue
        print(val, 'is good to go')
        calFlag = False
    if cyaFlag:
        val = constants.CYA
        cya = float(input('Enter the CYA levels: '))
        if check_calculate(val, cya):
            continue
        print(val, 'is good to go')
        cyaFlag = False
    if borateFlag:
        borate = float(input('Enter Borate levels: '))
        val = constants.Borate
        if check_calculate(val, borate):
            continue
        print(val, 'is good to go')
        borateFlag = False
    if pHTAFlag:
        phval = float(input('Enter the pH value: '))
        TAval = float(input('Enter the total alkalinity'))
        if not checkChemicals.checkpHandTA(TAval, phval, borate):
            continue
        print('pH and Total alkalinity are good to go!')
        pHTAFlag = False
    if fcFlag:
        fcval = float(input('Enter the FC value: '))
        if not checkChemicals.checkFC(fcval, cya):
            cal_fc(fcval, cya)
            continue
        print('FC value is good to go!')
    good_to_go = True

if good_to_go:
    print('Pool is ready to swim!')

