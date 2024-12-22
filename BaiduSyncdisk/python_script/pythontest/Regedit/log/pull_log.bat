@echo off
chcp 65001
setlocal

:: 用户输入apk包名
set /p apkname="Package： "
set name=%apkname:.=/%

:: 桌面路径
for /f "tokens=2 delims='='" %%a in ('wmic environment where "name='USERPROFILE'" get UserProfile /value') do set "UserProfile=%%~a"
set "DESKTOP_PATH=%UserProfile%\Desktop"

:: 导出日志
adb pull /storage/emulated/0/Android/data/%apkname%/files/ws/logs/%name% %DESKTOP_PATH%\
:: 使用Notepad打开
start Notepad++.exe %DESKTOP_PATH%\music\%apkname%.*

endlocal
