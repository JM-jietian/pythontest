# -*- coding:utf-8 -*-
# @Time:
# @Author: TJ
import os
import subprocess
import random
import time


class TcpConnect:
    """adb tcpip - connect 连接设备"""

    def __init__(self):
        self.id = None  # 设备id
        self.ip = None  # 设备ip地址
        self.port = None  # 连接端口
        self.ID = None  # 标记
        self.IP = None  # 标记

    def devices_id(self):
        try:
            # 获取设备id
            self.id = [line.split('\t')[0].strip() for line in os.popen('adb devices').readlines()[1:] if
                               line.split('\t')[0].strip()]
            if not self.id:
                print(f"\t没有已连接的设备！！！\n")
                self.ID = True
                return
        except Exception as e:
            print(f"\t没有已连接的设备: {e}\n")
            self.ID = True
            return

    def devices_ip(self, did):
        try:
            # 获取设备ip地址
            self.ip = [line.split('/')[0].strip().strip("inet ") for line in
                               os.popen(f'adb -s {did} shell ip addr show wlan0 | findstr "inet"').readlines()[:1]]
            if not self.id:
                print(f"\t没有已连接的设备！！！\n")
                self.IP = True
                return
        except Exception as e:
            print(f"\t设备没有网络连接: {e}")
            self.IP = True
            return

    def tcp_server(self):
        self.devices_id()  # 获取设备id
        if self.ID:  # 标记为True时结束运行
            return
        try:
            for d_id in self.id:  # 循环创建连接
                print(f"设备ID：{d_id}\t开始建立连接~\n")
                self.devices_ip(d_id)  # 获取设备ip地址
                if self.IP:  # 标记为True时结束运行
                    return
                self.port = random.randrange(3000, 65500, 2)  # 随机数，作为连接端口用
                # adb tcpip & adb connect创建连接
                cmd = f"adb -s {d_id} tcpip {self.port} & adb -s {d_id} connect {self.ip[0]}:{self.port}"
                output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                                  stderr=subprocess.PIPE).communicate()
                time.sleep(3)
                if errors:
                    print(f"\t连接失败~\nDevice ID:{self.id[0]}\n错误:{errors.decode('utf-8')}\n")
                else:
                    print(f"\t连接成功~\nID：{d_id}\nIP：{self.ip[0]}\n接口：{self.port}\n")
        except Exception as e:
            print(f"\t异常: {e}\n")
        except UnicodeDecodeError as e:
            print(f"\t异常: {e}\n")


if __name__ == "__main__":
    run = TcpConnect()
    run.tcp_server()