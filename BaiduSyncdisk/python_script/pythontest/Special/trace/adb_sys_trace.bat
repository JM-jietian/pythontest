chcp 65001
@echo off
color 1f
cls
:: 桌面路径
for /f "tokens=2 delims='='" %%a in ('wmic environment where "name='USERPROFILE'" get UserProfile /value') do set "UserProfile=%%~a"
set "DESKTOP_PATH=%UserProfile%\Desktop"

:: 将config.pbt文件导入测试设备
adb push D:\BaiduSyncdisk\python_script\专项\trace\config.pbtx /data/local/tmp/config.pbtx

:: 执行perfetto抓取trace文件
adb shell "cat /data/local/tmp/config.pbtx | perfetto --txt -c - -o /data/misc/perfetto-traces/trace.perf"

:: 将抓取到的trace文件导入桌面
adb pull /data/misc/perfetto-traces/trace.perf %DESKTOP_PATH%\