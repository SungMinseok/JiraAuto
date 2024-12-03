@echo off
REM Activate the virtual environment
call C:\myvenv\jiraauto\Scripts\activate.bat

REM Run PyInstaller with the specified options
pyinstaller --upx-dir C:\upx-4.2.4-win64 -F -w -i ico.ico --name JiraAuto index.py

REM Pause to see the output if running manually
pause
