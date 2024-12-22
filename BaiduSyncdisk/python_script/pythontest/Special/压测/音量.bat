@echo off
setlocal

:: 增加音量：
:: adb shell input keyevent 24
:: 减少音量：
:: adb shell input keyevent 25
:: 静音：
:: adb shell input keyevent 164

:: 设置目标音量级别（0-100）
set TARGET_VOLUME=20
:: 获取当前音量
for /f "tokens=2 delims=:" %%a in ('adb shell getprop sys.volume.level') do set CURRENT_VOLUME=%%a
:: 转换为整数
set /a CURRENT_VOLUME=%CURRENT_VOLUME%
:: 比较当前音量与目标音量，根据需要增加或减少
if %CURRENT_VOLUME% lss %TARGET_VOLUME% (
    echo Increasing volume...
    adb shell input keyevent 24
) else if %CURRENT_VOLUME% gt %TARGET_VOLUME% (
    echo Decreasing volume...
    adb shell input keyevent 25
)
echo Current volume is %CURRENT_VOLUME%.
endlocal