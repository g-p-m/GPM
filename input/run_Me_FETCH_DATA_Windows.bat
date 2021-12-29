python Fetch_from_cura.free.fr.py
for %%n in (*.csv); do @echo %%n
for %%n in (*.csv); do python.exe Remove_duplicate_lines.py %%n >_tmp_%%n

ren _tmp_SportsChampions_TimePlace.csv  BIG_4_SportsChampions.csv
ren _tmp_MilitaryMen_TimePlace.csv      BIG_4_MilitaryMen.csv
ren _tmp_MentalPatients_TimePlace.csv   BIG_4_MentalPatients.csv
 
@md _unused_data_
@move *.csv  _unused_data_
@move _unused_data_\BIG_4_* .

: In Sports Champions and Scientists Medical Doctors two are false duplicates,
: those are different people born on the same date at the same time.
: Only one is a true duplicate: Lucien Leger (born on 1912-8-29) in volumes A2 and E1.
"C:\Program Files\Git\usr\bin\grep.exe" -a -v "1912,8,29,1,0,0,-,-,20_bastia" _unused_data_\_tmp_ScientistsMedicalDoctors_TimePlace.csv >>BIG_4_ScientistsMedicalDoctors.csv
@echo Now, if you do not have grep, you must do the following manually (normally with symbol " instead of '):
@echo "grep -a -v '1912,8,29,1,0,0,-,-,20_bastia' _unused_data_\_tmp_ScientistsMedicalDoctors_TimePlace.csv >>BIG_4_ScientistsMedicalDoctors.csv
