@echo off
setlocal

:: ����������
:: adb shell input keyevent 24
:: ����������
:: adb shell input keyevent 25
:: ������
:: adb shell input keyevent 164

:: ����Ŀ����������0-100��
set TARGET_VOLUME=20
:: ��ȡ��ǰ����
for /f "tokens=2 delims=:" %%a in ('adb shell getprop sys.volume.level') do set CURRENT_VOLUME=%%a
:: ת��Ϊ����
set /a CURRENT_VOLUME=%CURRENT_VOLUME%
:: �Ƚϵ�ǰ������Ŀ��������������Ҫ���ӻ����
if %CURRENT_VOLUME% lss %TARGET_VOLUME% (
    echo Increasing volume...
    adb shell input keyevent 24
) else if %CURRENT_VOLUME% gt %TARGET_VOLUME% (
    echo Decreasing volume...
    adb shell input keyevent 25
)
echo Current volume is %CURRENT_VOLUME%.
endlocal