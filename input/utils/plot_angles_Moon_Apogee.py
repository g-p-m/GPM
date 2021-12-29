import sys, matplotlib, matplotlib.pyplot as plt, swisseph  # 2.8.00-1   # pip install pyswisseph   # https://pypi.org/project/pyswisseph
matplotlib.use('TkAgg')
objects = [swisseph.MOON, swisseph.INTP_APOG]
if sys.platform=='linux': swisseph.set_ephe_path('/usr/share/ephe') # set path to semo_12.se1 and semo_18.se1 from ftp.astro.com/pub/swisseph/ephe/
else:                     swisseph.set_ephe_path('\\sweph\\ephe')  # assume Windows, and set path to ephemeris files in case you run MS Windows

file = open(sys.argv[1], 'r')   # e.g. BIG_4_SportsChampions.csv
count = [0] * 360

for line in file:
    if line[0]=='#':  continue
    line = line.split(',')
    year  = int(line[0])
    month = int(line[1])
    day   = int(line[2])
    hour   = int(line[3])
    minute = int(line[4])
    second = int(line[5])
    julday = swisseph.julday(year, month, day, hour + minute/60.0 + second/3600.0)
    longitudes = [ swisseph.calc_ut(julday, obj, swisseph.FLG_SWIEPH)[0][0] for obj in objects]
    a = int(longitudes[0] + 360 - longitudes[1]) % 360  # Angle between Moon and Apogee
    count[a] += 1

c = count[:]
for i in range(360):
	s = 0
	for j in range(-7,8):
		s += count[(i + j) % 360]
	c[i] = s/15

z = [n for n in c if n]  # z is c without zeros
print(min(z), "is the minimum, at", c.index(min(z)))
print(max(z), "is the maximum, at", c.index(max(z)))
print(c)

fig, ax = plt.subplots()
ax.plot(list(range(360)), c)
ax.set_xticks([i*30 for i in range(13)], minor=False)
ax.xaxis.grid(True, which='major')
plt.show()
