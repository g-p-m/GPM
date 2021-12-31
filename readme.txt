First, please install the necessary Python packages,
pip install pyswisseph
and/or
pip install ephem
Also, scipy is a must (pip install scipy), matplotlib is optional.

Then in the subfolder 'input' please execute
either run_Me_FETCH_DATA_Linux.sh
or run_Me_FETCH_DATA_Windows.bat
according to your operating system.

After that: if you are using Linux, run
bash runMe_Linux.sh with_ephem.py
and/or
bash runMe_Linux.sh with_swisseph.py

If your OS is Windows,
runMe_Windows.bat with_ephem.py
and/or
runMe_Windows.bat with_swisseph.py

Please don't use the_expected_*.zip before generating such files,
and sharing your comments and questions with the authors,
lulg998 at g mail, especially if there are any problems.

Note after installing pyswisseph you should manually download
a couple files semo*.se1 from www.astro.com  as explained
on https://github.com/astrorigin/pyswisseph#test-suite
and in the comments in with_swisseph.py

Note in input/Fetch_from_cura.free.fr.py
you can choose whether to fetch data
from http://cura.free.fr/gauq/ or
from http://web.archive.org/web/http://cura.free.fr/gauq/

