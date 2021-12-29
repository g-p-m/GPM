import sys
filenames = [
'902gdA1.html',
'902gdA2.html',
'902gdA3.html',
'902gdA4.html',
'902gdA5.html',
'902gdA6.html',

'902gdD6.html',
'902gdD10.html',  # Note there's 902gdD10.txt at the end of this list:
'902gdE1.html',   #    (1) Open 902gdD10.html in a web browser  (2) Copy and paste all content into 902gdD10.txt
'902gdE3.html',   #    (3) Remove everything before & after the first table  (4) Assert there are 1398 lines after the first line (the table header)

'902gdF2.html',   # Don't use it! Almost every Army Professional in this volume has a *twin* in one of the earlier volumes. Check the concatenated file ( MilitaryMen_TimePlace.csv + MilitaryMen_F2_TimePlace.csv ) with List_twins.py

'902gdA1y.html',  # A1 with names     # Helpful
'902gdA2y.html',  # A2 with names     #  to inspect
'902gdA3y.html',  # A3 with names     #   duplicates and twins
'902gdA4y.html',  # A4 with names     
'902gdA5y.html',  # A5 with names
'902gdA6y.html',  # A6 with names

'902gdD9a.html',
'902gdD9b.html',
'902gdD9c.html',

'902gdD10.txt',
]

if 1:   # change to 'if 0' to avoid the risk of damaging/overwritting html files
	import urllib.request    # works fine in Python 3.7.10
	for filename in filenames:
		try:
			file = open(filename, 'rt')
			print("Found file and skipped fetching from http://cura.free.fr to", filename)
		except OSError:
			if 0:  url = 'http://cura.free.fr/gauq/'
			else:  url = 'http://web.archive.org/web/http://cura.free.fr/gauq/' # Note if you use this, you'd probably have to manually remove from 902gdD10.html everything before <!-- END WAYBACK TOOLBAR INSERT -->, except <html>, before the four steps for making 902gdD10.txt
			print("Fetching from " + url + " to file", filename)
			html = urllib.request.urlopen(url + filename).read().decode("cp1252").replace("\r\n", "\n")
			file = open(filename, 'wt')
			file.write(html)
		file.close()


def readLinesFromFile(srcFilename, headerID):
	file = open(srcFilename, 'rt')
	lines = []
	i = indexOfPre = indexOfHeader = -1
	for line in file:
		lines.append(line)
		i += 1
		if line.find("<pre>") >= 0:  indexOfPre = i
		if indexOfPre>=0 and indexOfHeader<0 and line.find(headerID)!=-1:  indexOfHeader = i
	file.close()
	return lines, indexOfHeader

def writeOneLineToFile(file, y, m, d, ho, mi, se, lat, lon, placeNameOrCode):   # ho is an integer, all other parameters are strings
	if not (-23 <= ho <= 47):  sys.exit('Error: wrong hour')
	numDays = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	year = int(y)
	month= int(m)
	day  = int(d)
	if day > numDays[month-1] or (month==2 and day==29 and (year % 4 != 0 or (year % 100 == 0 and year % 400 != 0)) ):  # Gregorian calendar's rule for leap years 
		file.write('# !Error! ')
	file.write( str(year)+',' + str(month)+',' + str(day)+',' + str(ho)+',' + str(int(mi))+',' + str(int(se))+',' + lat+',' + lon+',' + placeNameOrCode.strip()+'\n' )

""" Vol.A   Header and sample:
NUM	NAT	DAY	MON	YEA	HOU	MIN	SEC	TMZ	LAT	LON	COD	PLA
1	F	17	9	1937	17	0	0	0	44N50	0W34	33	BORDEAUX
2	F	13	8	1889	12	20	40	0	48N50	2E20	75	PARIS 8E
3	F	16	11	1926	6	0	0	0	43N18	5E22	13	MARSEILLE
"""
def processVolA(srcFilename, dstFilename, howManyToSkip, howManyToTake): # A relatively simple format
	lines, indexOfHeader = readLinesFromFile(srcFilename, 'NUM	NAT	DAY	MON	YEA	HOU	MIN	SEC	TMZ	LAT	LON	COD	PLA')
	dest = open(dstFilename, 'wt')
	i0 = i = indexOfHeader+1 + howManyToSkip
	while len(lines[i]) > 10 and i < i0 + howManyToTake:
		line = lines[i].split('\t')
		i+=1
		day   = line[2]
		month = line[3]
		year  = line[4]
		hour  = int(line[5]) + int(line[8])  # !!! ATTN:  -23 <= hour <= 47 after this !!!
		minute= line[6]
		second= line[7]
		latitude = line[9]
		longitude= line[10]
		place = line[11] + ('_'+line[12].lower() if len(line)>12 else '')
		writeOneLineToFile(dest, year, month, day, hour, minute, second, latitude, longitude, place)
	dest.write('# End of data from Volume A, ' + str(i-i0) + ' persons\n')
	dest.close()

""" Vol.D6  Header and sample:
NUM	DAY	MON	YEA	HOU	MIN	SEC	LAT	LON	NAM
1	5	1	1935	18	30	0	49N10	05E51	Adamczyk Marcel
2	15	3	1945	3	0	0	48N50	10E07	Adams Walter
3	14	11	1937	8	30	0	44N48	10E19	Adorni Vittorio
"""
def processVolD6(srcFilename, dstFilename):  # Here we have to derive time zone from longitude
	lines, indexOfHeader = readLinesFromFile(srcFilename, 'NUM	DAY	MON	YEA	HOU	MIN	SEC	LAT	LON	NAM')
	dest = open(dstFilename, 'at')
	i0 = i = indexOfHeader+2 # +2 because of an empty line after the header
	while len(lines[i]) > 10:
		line = lines[i].split('\t')
		i+=1
		day   = line[1]
		month = line[2]
		year  = line[3]
		hour  = int(line[4])
		minute= int(line[5])
		second= int(line[6])
		latitude = line[7]
		longitude= line[8]
		time = second + minute*60 + hour*3600
		longitudeParts = longitude.split('E')
		if len(longitudeParts)==1:  longitudeParts = longitude.split('W')
		zoneInLongitudeMinutes = int(longitudeParts[0])*60 + int(longitudeParts[1])
		zoneInTemporalSeconds = int(round(zoneInLongitudeMinutes / (180.0*60) * (12*3600)))
		if longitude.find('E')>=0:  time-=zoneInTemporalSeconds
		else:                       time+=zoneInTemporalSeconds
		hour   = time // 3600
		minute = (time-hour*3600) // 60
		second =  time-hour*3600-minute*60
		#if time<0: print(time, hour, minute, second)
		assert 0<=minute<=59
		assert 0<=second<=59
		writeOneLineToFile(dest, year, month, day, hour, str(minute), str(second), latitude, longitude, line[9].lower())
	dest.write('# End of data from Volume D6, ' + str(i-i0) + ' persons\n')
	dest.close()

""" Vol.D10  Header and sample:
NAM	PRO	DAY	MON	YEA	HOU	TMZ	LAT	LON	PLA
Aaron Harold	MI	21	06	1921	07:00	6h	40N29	86W8	Kokomo, IN
Aaron Henry	SP	05	02	1934	20:25	6h	30N41	88W3	Mobile, AL
Abramowicz Daniel	SP	13	07	1945	09:16	4h	40N22	80W37	Steubenville, OH
"""
def processVolD10(srcFilename, professionCode, dstFilename):  # A completely different format! Names are included.
	lines, indexOfHeader = readLinesFromFile(srcFilename, 'NAM	PRO	DAY	MON	YEA	HOU	TMZ	LAT	LON	PLA')
	dest = open(dstFilename, 'at')
	n, i = 0, indexOfHeader+1
	while i < len(lines) and len(lines[i]) > 10:
		line = lines[i].replace(' \t', '\t')
		line = line.split('\t')
		i+=1
		while len(line[1])==0: line.pop(1)
		if not line[1].startswith(professionCode):  continue
		n+=1
		day   = line[2]
		month = line[3]
		year  = line[4]
		time  = line[5]
		zone  = line[6]
		latitude = line[7]
		longitude= line[8]
		timeParts = time.split(':')
		zoneParts = zone.split('h')
		assert len(timeParts)==2
		hour,  minute = int(timeParts[0]), int(timeParts[1])
		if len(zoneParts)<2 or zone[-1]=='h':  zhour, zminute = int(zoneParts[0]), 0
		else:                                  zhour, zminute = int(zoneParts[0]), int(zoneParts[1])
		assert zhour>0
		UT = (hour + zhour)*60 + minute + zminute
		hour   = UT // 60
		minute = UT - hour*60
		assert 0<=minute<=59
		second = '0'
		writeOneLineToFile(dest, year, month, day, hour, str(minute), second, latitude, longitude, line[9].lower())
	dest.write('# End of data from Volume D10, ' + str(n) + ' persons\n')
	dest.close()

""" Vol.E1 and E3  Header and sample:
NUM     PRO      NAM                             DAY   MON   YEA     HOU      PLA                       COD        MO VE MA JU SA
0001    PH       ABELY Xavier                    24    03    1890    08:00    Verdun sur Garonne        82         36 03 17 09 24
0002    EX       ABILE-GAL Jean Baptiste         10    02    1901    11:00    Carmaux                   81         20 10 23 14 12
0002b   PH       ABONNEUC Louis André            14    10    1883    18:00    St Sébastien              38         03 19 26 26 33
0003    PH       ACHER DUBOIS Xavier             18    04    1914    17:00    La Roche sur Yon          85         25 14 03 24 12
"""
def processVolE(srcFilename, professionCode, dstFilename):  # A format similar to D10, but no '\t' except in the header !
	lines, indexOfHeader = readLinesFromFile(srcFilename, 'NUM     PRO      NAM                             DAY   MON   YEA     HOU      PLA                       COD        MO VE MA JU SA')
	dest = open(dstFilename, 'at')
	n, i = 0, indexOfHeader+2 # +2 because of an empty line after the header
	while len(lines[i]) > 10:
		line = lines[i]
		i+=1
		if not line[8:].startswith(professionCode):  continue
		n+=1
		day   = line[49:51]
		month = line[55:57]
		year  = line[61:65]
		hour  = int(line[69:71])
		minute=     line[72:74]
		second = '0'
		latitude = longitude ='-'
		writeOneLineToFile(dest, year, month, day, hour, minute, second, latitude, longitude, line[104:107].strip()+'_' + line[78:104].strip().lower())
	dest.write('# End of data from Volume E1, ' + str(n) + ' persons\n')
	dest.close()

""" Vol.F2  Header and sample:
NUM	DAY	MON	YEA	H	MN	SEC	TZ      LAT     LON     COD
3	08	07	1824	18	0	0	0	47N19	5E02	21
4	24	04	1849	12	0	0	-1	44N12	0E38	47
5	03	01	1821	19	0	0	0	48N07	5E08	52
"""
def processVolF2(srcFilename, dstFilename):  # A format similar to A1 ... A6
	lines, indexOfHeader = readLinesFromFile(srcFilename, 'NUM	DAY	MON	YEA	HOU	MIN	SEC	TMZ	LAT	LON')
	dest = open(dstFilename, 'at')
	i0 = i = indexOfHeader+2+616+5 # an empty line after the header, then 616 Liberation Fighters, then 5 more lines
	while len(lines[i]) > 10:
		line = lines[i].split('\t')
		i+=1
		day   = line[1]
		month = line[2]
		year  = line[3]
		hour  = int(line[4]) + int(line[7])  # !!! ATTN:  -23 <= hour <= 47 after this !!!
		minute= line[5]
		second= line[6]
		latitude = line[8]
		longitude= line[9]
		writeOneLineToFile(dest, year, month, day, hour, minute, second, latitude, longitude, line[10].strip())
	dest.write('# End of data from Volume F2, ' + str(i-i0) + ' persons\n')
	dest.close()


if 1:
	processVolA(  filenames[0],                'SportsChampions_TimePlace.csv',   0, 9999)   # 2087
	processVolA(  filenames[1],       'ScientistsMedicalDoctors_TimePlace.csv',   0, 9999)   # 3643
	processVolA(  filenames[2],                    'MilitaryMen_TimePlace.csv',   0, 9999)   # 3045, not 3046, because 1 has an invalid date of birth: 1869-Feb-29
	processVolA(  filenames[3],                       'Painters_TimePlace.csv',   0, 1473)   # 1473
	processVolA(  filenames[3],                      'Musicians_TimePlace.csv', 1473,9999)   # 1247, not 1248, because 1 is a true duplicate: name either Leon Ghilain or Alexandre Kah, born on 1839-Sep-5 in Nevers
	processVolA(  filenames[4],                         'Actors_TimePlace.csv',   0, 1409)   # 1407, not 1408, because 1 is a true duplicate: Francois Victor Arthur Gilles de Saint Germain, born on 1832-Jan-12, see also https://fr.wikipedia.org/wiki/Gilles_de_Saint-Germain
	processVolA(  filenames[4],                    'Politicians_TimePlace.csv', 1409,9999)   # 1001, not 1002, because 1 has an invalid date of birth: 1888-Jun-31
	processVolA(  filenames[5],                        'Writers_TimePlace.csv',   0, 1352)   # 1352
	processVolA(  filenames[5],                    'Journalists_TimePlace.csv', 1352,9999)   #  674

	processVolD6( filenames[6],                'SportsChampions_TimePlace.csv')   # 449

	processVolD10(filenames[-1], 'SP',          'SportsChampions_TimePlace.csv')   # 350
	processVolD10(filenames[-1], 'SC', 'ScientistsMedicalDoctors_TimePlace.csv')   #  98
	processVolD10(filenames[-1], 'MI',              'MilitaryMen_TimePlace.csv')   # 245
	processVolD10(filenames[-1], 'AR',                 'Painters_TimePlace.csv')   #  89
	processVolD10(filenames[-1], 'AC',                   'Actors_TimePlace.csv')   # 228
	processVolD10(filenames[-1], 'WR',                  'Writers_TimePlace.csv')   # 103
	processVolD10(filenames[-1], 'PO',              'Politicians_TimePlace.csv')   # 134

	processVolE(  filenames[8], 'PH', 'ScientistsMedicalDoctors_TimePlace.csv')   # 974, not 975, because 1 is a true duplicate: Lucien Leger, born on 1912-Aug-29
	processVolE(  filenames[8], 'MI',              'MilitaryMen_TimePlace.csv')   # 629

	processVolE(  filenames[9], 'PAI',                'Painters_TimePlace.csv')   #  91
	processVolE(  filenames[9], 'AC',                   'Actors_TimePlace.csv')   # 125
	processVolE(  filenames[9], 'WR',                  'Writers_TimePlace.csv')   # 210, not 211, because 1 is a true duplicate: Daniel Boulanger, born on 1922-Jan-24
	processVolE(  filenames[9], 'PO',              'Politicians_TimePlace.csv')   # 641, not 642, because 1 is a true duplicate: Raymond Marcellin, born on 1914-Aug-19 in Sezanne
	processVolE(  filenames[9], 'JO',              'Journalists_TimePlace.csv')   # 344
	processVolE(  filenames[9], 'MUS',               'Musicians_TimePlace.csv')   #  83

	processVolF2( filenames[10],                   'MilitaryMen_F2_TimePlace.csv')   # Don't use it! Almost every Army Professional in this volume has a *twin* in one of the earlier volumes. Check the concatenated file ( MilitaryMen_TimePlace.csv + MilitaryMen_F2_TimePlace.csv ) with List_twins.py


"""  Vol.D9b header and sample:
CMD	NUM	SEX	DAY	MON	YEA	HOU	MIN	SEC	TMZ	LAT	LON	COD

ACD	1	M	13	3	1894	20	20	40	0	50N39	3E 5	59
ACD	2	M	20	6	1896	16	50	40	0	46N40	1W25	85
ACD	3	F	26	3	1897	17	50	40	0	43N18	0W22	64
ACD	4	F	2	2	1899	15	50	40	0	48N18	4E 5	10

     Vol.D9a,D9c header and sample:
NUM	SEX	DAY	MON	YEA	HOU	MIN	SEC	TMZ	LAT	LON	COD

1	M	21	1	1819	15	47	40	0	50N39	3E 5	59
2	M	8	11	1825	21	35	12	0	48N42	6E12	54
3	M	18	12	1830	9	47	40	0	50N39	3E 5	59
"""
def processVolD9(srcFilename, dstFilename, howManyToSkip, howManyToTake, idxDayColumn): # A relatively simple format
	lines, indexOfHeader = readLinesFromFile(srcFilename, 'NUM	SEX	DAY	MON	YEA	HOU	MIN	SEC	TMZ	LAT	LON	COD')
	dest = open(dstFilename, 'wt')
	i0 = i = indexOfHeader+2 + howManyToSkip  # +2 because of an empty line after the header
	while len(lines[i]) > 10 and i < i0 + howManyToTake:
		line = lines[i].split('\t')
		i+=1
		day   = line[idxDayColumn]
		month = line[idxDayColumn+1]
		year  = line[idxDayColumn+2]
		hour  = int(line[idxDayColumn+3]) + int(line[idxDayColumn+6])  # !!! ATTN:  -23 <= hour <= 47 after this !!!
		minute= line[idxDayColumn+4]
		second= line[idxDayColumn+5]
		latitude = line[idxDayColumn+7]
		longitude= line[idxDayColumn+8]
		writeOneLineToFile(dest, year, month, day, hour, minute, second, latitude, longitude, line[idxDayColumn+9].strip()+'_'+line[idxDayColumn-1])
	dest.write('# End of data from Volume D9b, ' + str(i-i0) + ' persons\n')
	dest.close()

if 1:
	processVolD9(filenames[-4], 'FrenchMurderers_TimePlace.csv',  0, 9999, 2)  # 622
	processVolD9(filenames[-3], 'MentalPatients_TimePlace.csv',   0, 9999, 3)  # 4521
	processVolD9(filenames[-2], 'FrenchAlcoholics_TimePlace.csv', 0, 9999, 2)  # 1793
