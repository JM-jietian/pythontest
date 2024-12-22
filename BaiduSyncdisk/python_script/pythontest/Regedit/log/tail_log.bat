@echo off
chcp 65001
setlocal

:: 输入apk包名
set /p apkname="Package： "
set name=%apkname:.=/%

:: 输入过滤关键字
set /p sift="sift: "
:: %errorlevel% 程序返回码,用于判断刚才的命令是否执行，成功默认值为0，命令执行出错为1
::echo %errorlevel%
if %errorlevel% == 0 (
	rem %sift%有值则过滤关键字
	adb shell tail -f /storage/emulated/0/Android/data/%apkname%/files/ws/logs/%name%/%apkname%.* | findstr '%sift%'
) else (
	rem %sift%无值则不过滤
	adb shell tail -f /storage/emulated/0/Android/data/%apkname%/files/ws/logs/%name%/%apkname%.*
)

endlocal