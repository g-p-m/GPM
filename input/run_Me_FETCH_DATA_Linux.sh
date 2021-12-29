python3 Fetch_from_cura.free.fr.py
for n in *_TimePlace.csv; do (python3 Remove_duplicate_lines.py $n >_tmp_$n) done

mv _tmp_SportsChampions_TimePlace.csv  BIG_4_SportsChampions.csv
mv _tmp_MilitaryMen_TimePlace.csv      BIG_4_MilitaryMen.csv
mv _tmp_MentalPatients_TimePlace.csv   BIG_4_MentalPatients.csv

# In Sports Champions and Scientists Medical Doctors two are false duplicates,
# those are different people born on the same date at the same time.
# Only one is a true duplicate: Lucien Leger (born on 1912-8-29) in volumes A2 and E1.
grep -a -v "1912,8,29,1,0,0,-,-,20_bastia" _tmp_ScientistsMedicalDoctors_TimePlace.csv >BIG_4_ScientistsMedicalDoctors.csv

mkdir _unused_data_
mv *.csv  _unused_data_
mv _unused_data_/BIG_4_* .
