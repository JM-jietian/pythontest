# -*- coding:utf-8 -*-
# @Time:
# @Author: TJ
import os
import subprocess

# adb安装路径
adb_path = 'adb'

if "ANDROID_HOME" in os.environ:
    command = os.path.join(
        os.environ["ANDROID_HOME"],
        "platform-tools",
        "adb")
else:
    raise EnvironmentError(
        "在 $ANDROID_HOME 中找不到 Adb : %s." %
        os.environ["ANDROID_HOME"])

class ADB:
    # 参数: device
    def __init__(self, device):
        self.device = "-s %s" % device

    @staticmethod
    def cmd_invoke(cmd):
        output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if errors:
            e = errors.decode("gbk")
            return e
        else:
            o = output.decode("gbk")
            return o

    def adb(self, args):
        cmd = "%s %s %s" % (adb_path, self.device, str(args))
        return self.cmd_invoke(cmd)

    def shell(self, args):
        cmd = "%s %s shell %s" % (adb_path, self.device, str(args))
        return self.cmd_invoke(cmd)

    def get_device_state(self):
        """
        获取设备状态： offline | bootloader | device
        """
        return self.adb("get-state").strip()

    def get_device(self):
        """
        获取设备id号，return serialNo
        """
        return self.adb("get-serialno").strip()

    def get_android_version(self, is_big_version=False):
        """
        获取设备中的Android版本号，如4.2.2
        如果is_big_version=True 则只获取大版本号，如1-14
        """
        return self.shell("getprop ro.build.version.release").strip()

    def get_sdk_version(self):
        """
        获取设备SDK版本号，如：24
        """
        return self.shell("getprop ro.build.version.sdk").strip()

    def get_product_brand(self):
        """
        获取设备品牌，如：HUAWEI
        """
        return self.shell("getprop ro.product.brand").strip()

    def get_product_model(self):
        """
        获取设备型号，如：MHA-AL00
        """
        return self.shell("getprop ro.product.model").strip()

    def get_product_rom(self):
        """
        获取设备ROM名，如：MHA-AL00C00B213
        """
        return self.shell("getprop ro.build.display.id").strip()