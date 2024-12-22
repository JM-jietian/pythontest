# -*- coding:utf-8 -*-
# @Time: 2023/5/28  10：00
# @Author: J
import time
import os
import subprocess
import sys
from icecream import ic


class Encapsulation:
    @staticmethod
    def Version_number(cmd):
        output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if errors:
            e = errors.decode("utf-8")
            print(e)
            os.system('pause')
            return e
        else:
            o = output.decode("utf-8")
            return o

    @staticmethod
    def devices():
        """if 条件语句用于筛选出不为空的设备号。因为如果 split('\t')[0] 之后得到的字符串为空，则说明这一行并不是设备号，而是其它信息（如标题行等），需要被过滤掉"""
        dev_list = [line.split('\t')[0].strip() for line in os.popen('adb devices').readlines()[1:] if
                    line.split('\t')[0].strip()]
        return dev_list

    @staticmethod
    def device_connections():
        # 判断有无设备连接
        num_devices = len(Encapsulation.devices())
        if num_devices == 0:
            print(f"List of devices attached - Null\n")
            os.system('pause')
            return


class Install:
    """apk安装"""

    def __init__(self) -> None:
        os.system("chcp 65001")
        self.apkpath = sys.argv[1]
        self.apkName = [name for name in self.apkpath.split('\\') if ".apk" in name][0]
        self.Temporary_variables = None

    def install(self):
        Encapsulation.device_connections()  # 设备连接状态
        
        # ApkList = ['com.heytap.music', 'com.oppo.music']
        # for apk in ApkList:
        #     cmd_uninstall = f'adb uninstall {apk}'
        #     Encapsulation.Version_number(cmd_uninstall)
        # print(f'ApkPath:\t{self.apkpath}\nApkName:\t{self.apkName}')
        
        for device_ID in Encapsulation.devices():  # device_ID 设备ID
            cmd_Version = f'adb -s {device_ID} shell getprop ro.build.version.release'
            apk_Version = Encapsulation.Version_number(cmd_Version)  # apkVersion 安卓版本号
            print(f'DeviceID:\t{device_ID}\nVersion:\t{apk_Version}')

            try:
                if '40.' in self.apkName:
                    if int(apk_Version) >= 11:
                        cmd_install = f'adb -s {device_ID} install -r -d -t {self.apkpath}'
                        print('Directives:', cmd_install)
                        Installation = Encapsulation.Version_number(cmd_install)
                        print(Installation)
                    else:
                        ic('Installation failed......')
                        os.system('pause')
                        continue
                elif '50.' in self.apkName:
                    if 10 <= int(apk_Version) < 11 and 'oppo' in self.apkName:
                        self.Temporary_variables = self.apkpath
                    elif 9 <= int(apk_Version) < 10 and 'media' in self.apkName and 'old' not in self.apkName:
                        self.Temporary_variables = self.apkpath
                    elif int(apk_Version) < 9 and 'mediaold' in self.apkName:
                        self.Temporary_variables = self.apkpath
                    else:
                        ic('Installation failed......')
                        os.system('pause')
                        continue
                    cmd_install = f'adb -s {device_ID} install -r -d -t {self.Temporary_variables}'
                    print('Directives:', cmd_install)
                    Installation = Encapsulation.Version_number(cmd_install)
                    print(Installation)
                else:
                    cmd_install = f'adb -s {device_ID} install -r -d -t {self.apkName}'
                    print('Directives:', cmd_install)
                    Installation = Encapsulation.Version_number(cmd_install)
                    print(Installation)
            except Exception as e:
                ic(f'Installation failed......\n{e}')
                os.system('pause')
                continue


if __name__ == "__main__":
    run = Install()
    run.install()
