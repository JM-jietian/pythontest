@echo off
SETLOCAL ENABLEDELAYEDEXPANSION 
for /l %%i in (1 1 11000) do (
    set var=%%i
   echo ----- !var! 
   adb shell input keyevent 85 
   timeout /t 1
)