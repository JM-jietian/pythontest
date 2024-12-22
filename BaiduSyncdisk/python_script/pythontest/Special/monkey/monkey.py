# _*_ coding: utf-8 _*_
# @Time : 2023/11/20
# @Author : j

import os
import subprocess
import time
import logging
from multiprocessing import Process

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# 获取设备列表
def get_device_list():
    devices_output = subprocess.check_output('adb devices', shell=True).decode('utf-8')
    deviceList = [line.split()[0] for line in devices_output.splitlines()[1:] if line]
    return deviceList


# 检查环境变量 ANDROID_HOME
def get_adb_path():
    try:
        return os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb")
    except KeyError:
        logging.error("Adb not found in $ANDROID_HOME path: %s.", os.environ.get("ANDROID_HOME", ""))
        raise


# 获取设备中的Android版本号
def get_android_version(dev_id):
    # return self.shell("getprop ro.build.version.release").strip()
    os_version_output = \
        os.popen(f"adb -s {dev_id} shell getprop ro.build.version.release").read().strip()
    return os_version_output


# 执行 shell 命令
def run_shell_command(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
        logging.info(output)
        return output.strip()
    except subprocess.CalledProcessError as e:
        logging.error("Command '%s' failed with error: %s", cmd, e.output.decode('utf-8'))
        return None


# 执行 Monkey 测试
def run_monkey_test(device_ID, packageName):
    adb_path = get_adb_path()
    monkey_count = 1000000
    output_file = f"d:\\{device_ID}_{int(time.time())}.txt"

    # 禁止调节音量
    volume_cmd = f"{adb_path} -s {device_ID} shell content insert --uri content://settings/system --bind name:s:volume_music --bind value:i:0"
    run_shell_command(volume_cmd)

    # 执行 Monkey 测试
    monkey_cmd = f"{adb_path} -s {device_ID} shell monkey -p {packageName} -s 50 --throttle 100 --pct-touch 40 --pct-motion 30 --pct-syskeys 0 --pct-anyevent 0 --pct-appswitch 20 --ignore-crashes --ignore-timeouts --monitor-native-crashes -v -v {monkey_count} > {output_file}"
    run_shell_command(monkey_cmd)


if __name__ == '__main__':
    device_list = get_device_list()
    if not device_list:
        logging.error("No devices found.")
        exit(1)

    processes = []
    for device_id in device_list:
        os_version = get_android_version(device_id)
        package_name = "com.heytap.music" if int(os_version) > 11 else "com.oppo.music"
        p = Process(target=run_monkey_test, args=(device_id, package_name))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
