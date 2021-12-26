py -m pip install setuptools
py -m pip install --upgrade pip
py -m pip install virtualenv
py -m pip install pyinstaller
py -m pip install matplotlib
py -m pip install pandas
py -m pip install uk_covid19
timeout /t 1
pyinstaller --onefile "main.py"
del main.spec
del _QUELL.exe
move dist\main.exe
RMDIR /Q/S dist
RMDIR /Q/S build
RMDIR /Q/S __pycache__
ren main.exe _QUELL.exe
pause