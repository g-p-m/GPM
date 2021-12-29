#import matplotlib, matplotlib.pyplot as plt
#matplotlib.use('TkAgg')
import sys, scipy.stats, swisseph as swe  # 2.8.00-1   # pip install pyswisseph   # https://pypi.org/project/pyswisseph
objects = [swe.MOON, swe.SUN, swe.MERCURY, swe.VENUS, swe.MARS, swe.JUPITER, swe.SATURN]
swe.set_ephe_path('/usr/share/ephe' if sys.platform=='linux' else '\\sweph\\ephe') # set path to semo_12.se1 and semo_18.se1 from ftp.astro.com/pub/swisseph/ephe/
ito = 0  # index of the Target Object (that is, Moon)
targetAngle = 360 / int(sys.argv[2])
width = (6 if (targetAngle>=90 or targetAngle==60) else 2)   # As in Table 12 in  https://vixra.org/pdf/1106.0036v1.pdf
MaxOBJECTS = 4  # With bigger values scipy.stats.chisquare() sometimes fails: returns a 'nan' value (not a number)
insideYear, countYear = [], [0] * 2022
ctg, ccg = [0] * MaxOBJECTS, [0] * MaxOBJECTS   # ctg = count in Target Group, ccg = count in Control Group
assert swe.julday(1911, 3, 2, -2) == swe.julday(1911, 2, 29, 22)  # Assert negative hours are OK, and on non-leap years Feb.29 => Mar.1

def computeAll(year, month, day, hour, minute, second):
    julday = swe.julday(year, month, day, hour + minute/60.0 + second/3600.0)  # Julian day
    return [ swe.calc_ut(julday, obj, swe.FLG_SWIEPH)[0][0] for obj in objects]

def isTargetAngle(a):
    return (1 if (abs(targetAngle-a) <= width or abs(360-targetAngle-a) <= width) else 0)

for line in open(sys.argv[1], 'rt'):   ### Process the input file, collect statistics for the Target Group
    if line[0]=='#':  continue
    line = line.split(',')
    year  = int(line[0])
    month = int(line[1])
    day   = int(line[2])
    hour   = int(line[3])
    minute = int(line[4])
    second = int(line[5])
    countYear[year] += 1
    insideYear.append([month, day, hour, minute, second])
    longitudes = computeAll(year, month, day, hour, minute, second)
    numObjects = min(MaxOBJECTS-1,sum([isTargetAngle((longitudes[ito] + 360 - longitudes[i]) % 360) for i in range(1,len(objects))]))
    ctg[numObjects] += 1    # Sum of all ctg's is nl
    #for x in longitudes:  print("%3.9f," % x, end='')  # Print them to look at the difference
    #print()                                            # between pyephem and pyswisseph?

for y in range(len(countYear)):   ### Collect statistics for the Control Group
    if countYear[y]==0:  continue
    for insy in insideYear:  # Here we combine every InsideYear set with every year
        longitudes = computeAll(y, insy[0], insy[1], insy[2], insy[3], insy[4])
        numObjects = min(MaxOBJECTS-1,sum([isTargetAngle((longitudes[ito] + 360 - longitudes[i]) % 360) for i in range(1,len(objects))]))
        ccg[numObjects] += countYear[y]
nl = len(insideYear)  # Number of valid lines
assert sum(ccg) == nl**2   # Sum of all ccg's is nl*nl

for i in range(MaxOBJECTS):  print("%4d " % (round(ctg[i] * 100000 / nl)), end = ('' if i<MaxOBJECTS-1 else ': '))
for i in range(MaxOBJECTS):  print("%4d " % (round(ccg[i] * 100000 / nl**2)), end='')
print(' %1.7f' % scipy.stats.chisquare(ctg,[ccg[i]/nl for i in range(MaxOBJECTS)])[1], sys.argv[1][12:-4])
#plt.plot(list(range(MaxOBJECTS)), ctg)
#plt.show()  # 51 lines, including 13 non-essential: empty lines, assertions, and #-disabled lines
