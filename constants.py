inc = 'I'
dec = 'D'
GivenWaterVolume = 10000.00
CH = 'Calcium Hardness'
CYA = 'Cyanuric Acid'
pH = 'pH'
TA = 'Total alkalinity'
Borate = 'Borate'
FC = 'Free Chlorine'

FreeChlorine = [
    ['Liquid Chlorine', 0.19, 1, 10.2],
    ['Liquid Bleach', 0, 1, 24],
]

TotalAlkalinity = [
    ['Sodium Bicarbonate', 0.11, 10, 22.4]
    #['Liquid Muriatic acid', dec, 10, 25.6]
]

CyanuricAcid = [
    ['Cyanuric Acid', 0.87, 10, 13.3]
]

CalciumHardness = [
    ['Calcium Chloride 100%', 0.02, 10, 13.3],
    ['Calcium Chloride 77%', 0, 10, 17.3]
]

Borates = [
    ['Borax', 0.06, 10, 117.25],
    ['Sodium Tetra Borate', 0.0, 10, 90]
]

Salt = [
    ['Salt', 0, 10, 13.3]
]

optimalValuesMin = {CH: 200, CYA: 30, pH: 7.5, TA: 80, Borate: 30, FC: 7.5}
optimalValuesMax = {CH: 400, CYA: 50, pH: 7.8, TA: 120, Borate: 50, FC: 11.5}



