py -m pip install setuptools
py -m pip install --upgrade pip
py -m pip install virtualenv
py -m pip install pyinstaller
py -m pip install matplotlib
py -m pip install pandas
py -m pip install uk-covid19
timeout /t 5
pyinstaller --onefile "test.py"
del mast.spec
del _LAUNCH_MAST.exe
move dist\mast.exe
RMDIR /Q/S dist
RMDIR /Q/S build
RMDIR /Q/S __pycache__
ren mast.exe _LAUNCH_MAST.exe