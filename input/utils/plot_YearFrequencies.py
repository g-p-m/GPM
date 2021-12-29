import sys, matplotlib.pyplot as plt

file = open(sys.argv[1], 'r')  # e.g. BIG_4_SportsChampions.csv
x = range(1780,2000)
y = [0] * len(x)
for line in file:
	if line[0]=='#':  continue
	vars = line.split(',')
	year = int(vars[0]) - x[0]
	year = max(year, 0)
	year = min(year, len(y)-1)
	y[year] += 1
file.close()

z = [n for n in y if n]  # z is y without zeros
print(min(z), "is the minimum, year:", x[0] + y.index(min(z)))
print(max(z), "is the maximum, year:", x[0] + y.index(max(z)))
print(y)
fig, ax = plt.subplots()
ax.plot(x,y)
ax.set_xticks([i*10 for i in range(178,201)], minor=False)
ax.xaxis.grid(True, which='major')
plt.show()
