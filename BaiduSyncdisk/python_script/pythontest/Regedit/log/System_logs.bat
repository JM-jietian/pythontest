@echo off
chcp 65001
setlocal

:: 桌面路径
for /f "tokens=2 delims='='" %%a in ('wmic environment where "name='USERPROFILE'" get UserProfile /value') do set "UserProfile=%%~a"
set "DESKTOP_PATH=%UserProfile%\Desktop"

:: 导出日志
adb pull /storage/emulated/0/Android/data/com.oplus.logkit/files/Log/ %DESKTOP_PATH%\

endlocal