import sys, matplotlib, matplotlib.pyplot as plt, swisseph  # 2.8.00-1   # pip install pyswisseph   # https://pypi.org/project/pyswisseph
matplotlib.use('TkAgg')
objects = [swisseph.MOON, swisseph.INTP_APOG]
if sys.platform=='linux': swisseph.set_ephe_path('/usr/share/ephe') # set path to semo_12.se1 and semo_18.se1 from ftp.astro.com/pub/swisseph/ephe/
else:                     swisseph.set_ephe_path('\\sweph\\ephe')  # assume Windows, and set path to ephemeris files in case you run MS Windows
ctg,ccg = [0] * 360, [0] * 360
insideYear, countYear = [], [0] * 2022
maxYear, file = 0, open(sys.argv[1], 'r')   # e.g. BIG_4_SportsChampions.csv

for line in file:
    if line[0]=='#':  continue
    line = line.split(',')
    year  = int(line[0])
    month = int(line[1])
    day   = int(line[2])
    hour   = int(line[3])
    minute = int(line[4])
    second = int(line[5])
    countYear[year] += 1
    maxYear = max(maxYear, year)
    insideYear.append([month, day, hour, minute, second])
    julday = swisseph.julday(year, month, day, hour + minute/60.0 + second/3600.0)
    longitudes = [ swisseph.calc_ut(julday, obj, swisseph.FLG_SWIEPH)[0][0] for obj in objects]
    a = int(longitudes[0] + 360 - longitudes[1]) % 360  # Angle between Moon and Apogee
    ctg[a] += 1

for y in range(len(countYear)):
    if countYear[y]==0:  continue
    print(y, '/', maxYear)
    for insy in insideYear:  # Here we combine every InsideYear set with every year
        julday = swisseph.julday(y, insy[0], insy[1], insy[2] + insy[3]/60.0 + insy[4]/3600.0)
        longitudes = [ swisseph.calc_ut(julday, obj, swisseph.FLG_SWIEPH)[0][0] for obj in objects]
        a = int(longitudes[0] + 360 - longitudes[1]) % 360  # Angle between Moon and Apogee
        ccg[a] += countYear[y]
nl = len(insideYear)  # Number of valid lines
assert sum(ctg)==nl and sum(ccg) == nl**2   # Sum of all ccg's is nl*nl

c, t1, t2 = [],[],[sum(ctg[i*30 : i*30+30])/30 for i in range(12)]
for i in range(360):
	st1 = sc = 0
	for j in range(-5,6):
		st1 += ctg[(i + j) % 360]
		sc  += ccg[(i + j) % 360]
	t1.append(st1 / 11)
	c.append( sc  / (11*nl))

z = [n for n in ctg if n]  # z is t1 without zeros
print(min(z), "is the minimum, at", ctg.index(min(z)))
print(max(z), "is the maximum, at", ctg.index(max(z)))
print(ctg)

fig, ax = plt.subplots()
ax.plot(list(range(360)), c)
ax.plot(list(range(360)), t1)
ax.plot([i*30 + 15 for i in range(12)], t2)
ax.set_xticks([i*30 for i in range(13)], minor=False)
ax.xaxis.grid(True, which='major')
plt.show()
