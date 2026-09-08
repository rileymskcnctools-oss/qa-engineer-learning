@echo off
cd /d "%~dp0"
echo Packing all homework folders (skipping .venv / .idea / cache)...
echo.
for /d %%d in (homework*-appium-basic) do (
    python pack_homework.py "%%d"
)
echo.
echo Done. Zip files are saved in this folder.
pause
