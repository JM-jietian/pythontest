color 0A
echo off
adb wait-for-device

adb remount
:begin
adb shell settings put global device_provisioned 0
adb shell settings put secure user_setup_complete 0
adb shell settings get global device_provisioned
adb shell settings get secure user_setup_complete
adb shell pm enable com.coloros.bootreg
adb shell pm enable com.coloros.bootreg/.activity.WelcomePage
adb shell pm clear com.coloros.bootreg
ping -n 5 127.1>nul
adb shell am start com.coloros.bootreg/.activity.WelcomePage
pause
echo ***********按任意键再次拉起***********
pause
goto begin