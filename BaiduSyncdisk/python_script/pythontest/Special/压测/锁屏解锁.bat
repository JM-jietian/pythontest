@echo off
chcp 65001
title 锁屏密码解锁压力测试
color 1f
cls

echo.
echo.
echo                ★★★ 锁屏解锁压力测试 ★★★
echo.
echo.
echo    步骤：1.先进入设置--安全设置--锁屏，设置数字锁密码，比如123456
echo          2.打开手机的USB调试模式
echo          3.连接USB后，手机锁屏并灭屏
echo.
echo.

set /p b=请输入测试的次数：
set count=%b%
echo.
echo.
set /p x=请输入密码：
echo.
echo.
set /p delay=请输入灭屏前的等待时间（秒）：

for /l %%i in (1,1,%count%) do (
    :: 模拟按下电源键来唤醒屏幕
    adb shell input keyevent 26
    ping -n 1 127.0.0.1>nul
	timeout /t 2
    
    :: 模拟滑动解锁
    adb shell input swipe 450 1100 450 550
    ping -n 1 127.0.0.1>nul
    
    :: 输入密码
    adb shell input text %x%
    ping -n 1 127.0.0.1>nul
    
    :: 模拟按下回车键提交密码
    adb shell input keyevent 66
    ping -n 1 127.0.0.1>nul
    
    :: 模拟按下电源键来关闭屏幕
    adb shell input keyevent 26
	timeout /t %delay%
  
	
    cls
    echo.
    echo.
    echo               ★★★ 锁屏解锁压力测试 %b%次★★★
    echo.
    echo                   已测试次数：第%%i%次
)

echo.
echo              ------测试完毕------
pause