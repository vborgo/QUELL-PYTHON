CALL _INSTALL_DEPENDANCIES.bat
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