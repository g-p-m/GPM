#import matplotlib, matplotlib.pyplot as plt
#matplotlib.use('TkAgg')
import sys, math, scipy.stats, ephem   # 4.1.3    # pip install ephem      # https://pypi.org/project/ephem
startPoint = int(sys.argv[2])
NumSECTORS = int(sys.argv[3])
objects = [ephem.Moon(), ephem.Sun()]  # Note the first one is the target point. Also, Lunar apogee is in the list, see +2 below, in computeAll()
years, insideYear, apogees, countYear = [], [], [], [0] * 2022
minYear, maxYear = 9999, 0
ctg, ccg = [0] * NumSECTORS, [0] * NumSECTORS   # ctg = count in Target Group, ccg = count in Control Group
assert ephem.Date((1911, 3, 2, -2, 0, 0)) == ephem.Date((1911, 2, 29, 22, 0, 0))  # Assert negative hours are OK, and on non-leap years Feb.29 => Mar.1

def calcSpeed(obj, dist, julday, step):
    step = min(1/16384, step/2)   # 86400 seconds per day, so 1/16384 of a day is approximately 5 seconds
    while 1:
        obj.compute(julday+step, epoch=julday+step)
        if dist != obj.earth_distance:  return obj.earth_distance - dist
        obj.compute(julday-step, epoch=julday-step)
        if dist != obj.earth_distance:  return dist - obj.earth_distance
        step *= 1.5  # Cannot detect speed with this small step, let's increase step

def findNextApogee(julday):
    obj = objects[0]
    obj.compute(julday, epoch=julday)
    speed = calcSpeed(obj, obj.earth_distance, julday, 1)
    for x in range(17):
        step = 4 / 2**x
        while 1:
            julday2 = julday + step  # Plus for the next apogee, minus would be previous, and signs <0 >0 below
            obj.compute(julday2, epoch=julday2)
            speed2 = calcSpeed(obj, obj.earth_distance, julday2, step)
            if speed > 0 and speed2 < 0: break  # Go to the next x, that is, to a smaller step
            speed, julday = speed2, julday2
    return julday

def binarySearchApogee(julday, low, high):   # Assuming julday is within the range {apogees[low], apogees[high]}
    mid = (low + high) // 2
    if apogees[mid] <= julday <= apogees[mid+1]: return mid
    if julday < apogees[mid]:  return binarySearchApogee(julday, low, mid)
    return binarySearchApogee(julday, mid+1, high)

def computeAll(year, month, day, hour, minute, second):
    longitudes = [0.0] * (len(objects) + 2)  # +2 due to Lunar apogee, and 0 at the end
    julday = ephem.Date((year, month, day, hour, minute, second))  # Julian day
    for index in range(len(objects)):
        obj = objects[index]
        obj.compute(julday, epoch=julday)
        longitudes[index] = float( ephem.Ecliptic(obj).lon ) / math.pi * 180
    if startPoint==-2:   # if we need the Lunar apogee
        idx = binarySearchApogee(julday, 0, len(apogees)-1)
        juldayBelow = apogees[idx]
        juldayAbove = apogees[idx+1]
        assert 26.5 < juldayAbove-juldayBelow < 28 and juldayBelow<=julday<=juldayAbove
        obj = objects[0]
        obj.compute(juldayBelow, epoch=juldayBelow)
        longitudeBelow = float( ephem.Ecliptic(obj).lon ) / math.pi * 180
        obj.compute(juldayAbove, epoch=juldayAbove)
        longitudeAbove = float( ephem.Ecliptic(obj).lon ) / math.pi * 180
        d = longitudeAbove - longitudeBelow
        if  d < -90: d += 360
        elif d > 90: d -= 360
        assert -3.5 < d < 9
        longitudes[-2] = (longitudeBelow + d*(julday-juldayBelow)/(juldayAbove-juldayBelow) + 360) % 360
    return longitudes

for line in open(sys.argv[1], 'rt'):   ### Process the input file, then collect statistics for the Target Group
    if line[0]=='#':  continue
    line = line.split(',')
    year  = int(line[0])
    month = int(line[1])
    day   = int(line[2])
    hour   = int(line[3])
    minute = int(line[4])
    second = int(line[5])
    countYear[year] += 1
    minYear = min(minYear, year)
    maxYear = max(maxYear, year)
    years.append(year)
    insideYear.append([month, day, hour, minute, second])
julday    = ephem.Date((minYear-1, 11, 1, 0,0,0))
juldayEnd = ephem.Date((maxYear+1,  2, 1, 0,0,0))
while julday < juldayEnd:
    julday = findNextApogee(julday+24)  # Because the next one is 24+ Julian days after the previous
    apogees.append(julday)
for y, insy in zip(years, insideYear):
    longitudes = computeAll(y, insy[0], insy[1], insy[2], insy[3], insy[4])
    a = (longitudes[0] + 360 - longitudes[startPoint]) % 360  # Angle between Target Object and startPoint
    ctg[ int(a * NumSECTORS / 360) ] += 1    # Sum of all ctg's is nl
    #for x in longitudes:  print("%3.9f," % x, end='')  # Print them to look at the difference
    #print()                                            # between pyephem and pyswisseph?

for y in range(minYear, maxYear+1):   ### Collect statistics for the Control Group
    if countYear[y]==0:  continue
    for insy in insideYear:  # Here we combine every InsideYear set with every year
        longitudes = computeAll(y, insy[0], insy[1], insy[2], insy[3], insy[4])
        a = (longitudes[0] + 360 - longitudes[startPoint]) % 360  # try +362 for set (MP,-2,12), here and in line a= above
        ccg[ int(a * NumSECTORS / 360) ] += countYear[y]
nl = len(years)  # Number of valid lines
assert sum(ccg) == nl**2   # Sum of all ccg's is nl*nl

ccg = [ccg[i]*1. / nl  for i in range(NumSECTORS)]
for i in range(NumSECTORS):  print("%4d" % ctg[i], end = (' ' if i<NumSECTORS-1 else ' : '))
for i in range(NumSECTORS):  print("%5d" % (round(ctg[i] * 100000 / nl)), end = ('' if i<NumSECTORS-1 else ' : '))
for i in range(NumSECTORS):  print("%4d" % (round(ccg[i] * 100000 / nl)), end=' ')
for i in range(NumSECTORS):
    pv =            scipy.stats.binom.cdf(k = ctg[i],   n = nl, p=ccg[i] / nl)
    if pv>0.5: pv = scipy.stats.binom.cdf(k = ctg[i]-1, n = nl, p=ccg[i] / nl)
    print("%c%1.7f" % (' ' if  0.01 < pv < 0.99  else '@', pv), end='')
print('  %1.7f %1.7f' % (scipy.stats.chisquare(ctg,ccg)[1], scipy.stats.power_divergence(ctg,ccg,lambda_=0)[1]), sys.argv[1][12:-4])
#plt.plot(list(range(NumSECTORS)), ctg)
#plt.show()  # 110 lines, including 17 non-essential: empty lines, assertions, and #-disabled lines
