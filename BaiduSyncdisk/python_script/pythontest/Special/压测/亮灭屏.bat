@echo off
setlocal

:loop
:: ÁÁÆÁ
adb shell input keyevent 26
echo Screen turned on.
ping localhost -n 10 > nul
:: ÃðÆÁ
adb shell input keyevent 223
echo Screen turned off.
ping localhost -n 10 > nul
goto loop

endlocal