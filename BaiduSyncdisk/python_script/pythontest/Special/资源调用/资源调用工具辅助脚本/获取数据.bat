md data
del data\* /q /f
cd data
adb pull /sdcard/Android/data/com.demo.power.profile/files/History.txt
adb pull /sdcard/Android/data/com.demo.power.profile/files/NormalBatteryStats.txt
adb pull /sdcard/Android/data/com.demo.power.profile/files/NormalPowerSippers.txt
adb pull /sdcard/Android/data/com.demo.power.profile/files/ScreenOnBatteryStats.txt
adb pull /sdcard/Android/data/com.demo.power.profile/files/ScreenOnSipper.txt
adb pull /sdcard/Android/data/com.demo.power.profile/files/ScreenOnExcessive.txt
adb pull /sdcard/Android/data/com.demo.power.profile/files/ScreenOffBatteryStats.txt
adb pull /sdcard/Android/data/com.demo.power.profile/files/ScreenOffSipper.txt
adb pull /sdcard/Android/data/com.demo.power.profile/files/ScreenOffExcessive.txt
adb pull /sdcard/Android/data/com.demo.power.profile/files/NormalExcel.csv
adb pull /sdcard/Android/data/com.demo.power.profile/files/ScreenOnExcel.csv
adb pull /sdcard/Android/data/com.demo.power.profile/files/ScreenOffExcel.csv
pause