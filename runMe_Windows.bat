time <nul
echo  This all may take ~23 minutes with Swisseph and ~50 minutes with Ephem on a system with Core i7 @2.5 GHz 
for %%i in (input\BIG*.csv); do python %1 %%i -1 12 >>output_4x3__%1.txt
echo . >>output_4x3__%1.txt
for %%i in (input\BIG*.csv); do python %1 %%i  1 12 >>output_4x3__%1.txt
echo . >>output_4x3__%1.txt
for %%i in (input\BIG*.csv); do python %1 %%i -2 12 >>output_4x3__%1.txt
time <nul
