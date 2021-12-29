import sys
lines = []
inpfile = open(sys.argv[1], 'r')
logfile = open("log_of_duplicates_remover.txt", 'at')

for line in inpfile:
	if line in lines:
		logfile.write("From file "+sys.argv[1]+' : '+line)
		continue
	lines.append(line)
	print(line.strip())

inpfile.close()
logfile.close()
