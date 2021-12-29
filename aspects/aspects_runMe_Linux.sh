#### You can run this script as follows:  for p in aspects*.py; do (bash aspects_runMe_Linux.sh $p) done
date
for i in ../input/BIG_4_*.csv; do (echo $i; python3 $1 $i 1 >>output_4x8__$1.txt) done
echo . >>output_4x8__$1.txt
for i in ../input/BIG_4_*.csv; do (echo $i; python3 $1 $i 2 >>output_4x8__$1.txt) done
echo . >>output_4x8__$1.txt
for i in ../input/BIG_4_*.csv; do (echo $i; python3 $1 $i 3 >>output_4x8__$1.txt) done
echo . >>output_4x8__$1.txt
for i in ../input/BIG_4_*.csv; do (echo $i; python3 $1 $i 4 >>output_4x8__$1.txt) done
echo . >>output_4x8__$1.txt
for i in ../input/BIG_4_*.csv; do (echo $i; python3 $1 $i 5 >>output_4x8__$1.txt) done
echo . >>output_4x8__$1.txt
for i in ../input/BIG_4_*.csv; do (echo $i; python3 $1 $i 6 >>output_4x8__$1.txt) done
echo . >>output_4x8__$1.txt
for i in ../input/BIG_4_*.csv; do (echo $i; python3 $1 $i 7 >>output_4x8__$1.txt) done
echo . >>output_4x8__$1.txt
for i in ../input/BIG_4_*.csv; do (echo $i; python3 $1 $i 8 >>output_4x8__$1.txt) done
date
