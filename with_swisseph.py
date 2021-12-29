#import matplotlib, matplotlib.pyplot as plt
#matplotlib.use('TkAgg')
import sys, scipy.stats, swisseph as swe   # 2.8.00-1 aka 20200427    # pip install pyswisseph   # https://pypi.org/project/pyswisseph
objects = [swe.MOON, swe.SUN, swe.INTP_APOG]
swe.set_ephe_path('/usr/share/ephe' if sys.platform=='linux' else '\\sweph\\ephe') # set path to semo_12.se1 and semo_18.se1 from ftp.astro.com/pub/swisseph/ephe/
ito = 0  # index of the Target Object (that is, Moon)
startPoint = int(sys.argv[2])
NumSECTORS = int(sys.argv[3])
insideYear, countYear = [], [0] * 2022
ctg, ccg = [0] * NumSECTORS, [0] * NumSECTORS   # ctg = count in Target Group, ccg = count in Control Group
assert swe.julday(1911, 3, 2, -2) == swe.julday(1911, 2, 29, 22)  # Assert negative hours are OK, and on non-leap years Feb.29 => Mar.1

def computeAll(year, month, day, hour, minute, second):
    julday = swe.julday(year, month, day, hour + minute/60.0 + second/3600.0)  # Julian day
    return [swe.calc_ut(julday, obj, swe.FLG_SWIEPH)[0][0] for obj in objects] + [0]  # 0 at the end is the Vernal Equinox point

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
    a = (longitudes[ito] + 360 - longitudes[startPoint]) % 360  # Angle between Target Object and startPoint
    ctg[ int(a * NumSECTORS / 360) ] += 1    # Sum of all ctg's is nl
    #for x in longitudes:  print("%3.9f," % x, end='')  # Print them to look at the difference
    #print()                                            # between pyephem and pyswisseph?

for y in range(len(countYear)):   ### Collect statistics for the Control Group
    if countYear[y]==0:  continue
    for insy in insideYear:  # Here we combine every InsideYear set with every year
        longitudes = computeAll(y, insy[0], insy[1], insy[2], insy[3], insy[4])
        a = (longitudes[ito] + 360 - longitudes[startPoint]) % 360  # try +362 for set (MP,-2,12), here and in line a= above
        ccg[ int(a * NumSECTORS / 360) ] += countYear[y]
nl = len(insideYear)  # Number of valid lines
assert sum(ccg) == nl**2   # Sum of all ccg's is nl*nl

#for i in range(NumSECTORS):  print("%4d " % ctg[i], end = ('' if i<NumSECTORS-1 else ':'))
#for i in range(NumSECTORS):  print("%7d " % ccg[i], end='')
for i in range(NumSECTORS):  print("%4d " % (round(ctg[i] * 100000 / nl)), end = ('' if i<NumSECTORS-1 else ': '))
for i in range(NumSECTORS):  print("%4d " % (round(ccg[i] * 100000 / nl**2)), end='')
#for i in range(NumSECTORS):
#    pv =            scipy.stats.binom.cdf(k = ctg[i],   n = nl, p=ccg[i] / nl**2)
#    if pv>0.5: pv = scipy.stats.binom.cdf(k = ctg[i]-1, n = nl, p=ccg[i] / nl**2)
#    print("%c%1.7f" % (' ' if  0.01 < pv < 0.99  else '@', pv), end='')
print(' %1.7f' % scipy.stats.chisquare(ctg,[ccg[i] / nl  for i in range(NumSECTORS)])[1], sys.argv[1][12:-4])
#plt.plot(list(range(NumSECTORS)), ctg)
#plt.show()  # 53 lines, including 18 non-essential: empty lines, assertions, and #-disabled lines
