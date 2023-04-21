"""
This script seemingly reproduces one of the key results of the War Initiators study
from http://web.archive.org/web/20070623142631/http://users.livejournal.com/_soal/
that is, the rightmost column of the 1st long table.

Input files must contain only the date-time-place lines, for example, from this file:
http://web.archive.org/web/20040205114722/http://ukr-inter.net/~sasha/db/initiate.zbs
"""

import sys, swisseph as swe  # 2.8.00-1   # pip install pyswisseph   # https://pypi.org/project/pyswisseph
objects = [swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS, swe.JUPITER, swe.SATURN, swe.URANUS,  swe.TRUE_NODE, swe.OSCU_APOG]
swe.set_ephe_path('/usr/share/ephe' if sys.platform=='linux' else '\\sweph\\ephe') # set path to data files semo_1*.se1 and sepl_1*.se1 you got from ftp.astro.com/pub/swisseph/ephe/
targetAngles = [360 / 1, 360 / 2, 360 / 4, 360 / 8, 360 / 8 * 3]  # 0, 180, 90, 45, 135 degrees
width = 5
assert swe.julday(1911, 3, 2, -2) == swe.julday(1911, 2, 29, 22)  # Assert negative hours are OK, and on non-leap years Feb.29 => Mar.1

def computeAll(year, month, day, hour, minute, second):
    julday = swe.julday(year, month, day, hour + minute/60.0 + second/3600.0)  # Julian day
    return [ swe.calc_ut(julday, obj, swe.FLG_SWIEPH)[0][0] for obj in objects]

def isTargetAngle(a):
    for targetAngle in targetAngles:
        if abs(    targetAngle - a) <= width:  return (width - abs(    targetAngle - a))*100
        if abs(360-targetAngle - a) <= width:  return (width - abs(360-targetAngle - a))*100
    return 0

m = n = s = 0
for line in open(sys.argv[1], 'rt'):   ### Process the input file, collect statistics for the Target Group
    if line[0]=='#':  continue
    line = line.split(',')
    year  = int(line[0])
    month = int(line[1])
    day   = int(line[2])
    hour   = int(line[3])
    minute = int(line[4])
    second = int(line[5])
    longitudes = computeAll(year, month, day, hour, minute, second)
    numObjects = sum([isTargetAngle((longitudes[-1] + 360 - longitudes[i]) % 360) for i in range(len(objects)-1)])
    m = max(m,numObjects)     
    n += 1
    if len(sys.argv)<3: print("%4d" % round(numObjects))  # skip printing if that's specified from command line 
    s += numObjects
print('Sum=', s, '  numLines=', n, '  Average=', s/n, '  Maximum=', m)
