# !/usr/bin/python
# -*- coding: utf-8 -*-
# @Time: 2024/7/18
# @Author: j
import os
import subprocess
import logging
import threading
import time
import uiautomator2 as u2
from pathlib import Path

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Tool_encapsulation:
    def __init__(self):
        self.apk_path = os.path.abspath(Tool_encapsulation.walk_directory(Path("./apk"))[0])  # apk路径
        self.apk_name = [name for name in self.apk_path.split('\\') if ".apk" in name][0].split('.apk')[0]
        self.outcome_path = r'results'  # 结果
        self.Permissions_list_path = r'text\Permissions_list.txt'  # 权限列表

        self.jadx_path = r'tool\jadx-1.4.7\bin\jadx_py'  # jadx
        self.apktool_path = r'tool\apktool'  # apktool
        self.Static_outcome_path = r'text\Static_outcome.txt'  # 静态扫描结果

        self.device_id = "127.0.0.1:62025"  # 设备id
        self.d = u2.connect_usb(self.device_id)
        self.Dynamic_outcome_path = r'text\Dynamic_outcome.txt'  # 动态扫描结果
        self.text = None

    @staticmethod
    def walk_directory(folder_path):
        # 使用 rglob 获取所有文件，然后筛选出文件
        files = [file for file in folder_path.rglob('*.apk') if file.is_file()]
        # 返回文件的绝对路径
        return [str(file) for file in files]

    @staticmethod
    def version_number(cmd):
        logging.info(f'执行指令：{cmd}')
        try:
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode('gbk')
            logging.info(output)
            return output.strip()
        except subprocess.CalledProcessError as e:
            logging.error("Command '%s' failed with error: %s", cmd, e.output.decode('gbk'))
            return None

    @staticmethod
    def queries(target_text, Permissions_text, outcome_text):
        try:
            # 打开目标文件
            with open(target_text, 'r', encoding='utf-8') as target:
                content_target = target.readlines()
            with open(Permissions_text, 'r', encoding='utf-8') as Permissions:
                content_Permissions = Permissions.readlines()
            with open(outcome_text, 'w', encoding='utf-8') as outcome:
                for blur in content_Permissions:
                    blur = blur.strip('\n')  # 去除关键字的换行符
                    try:
                        blurs = blur.rsplit(':', 1)[1]  # 去掉关键字签的中文注释,若无注释则跳过
                    except IndexError:
                        pass
                    for line in content_target:  # 按行遍历目标文件
                        if blurs in line:  # 判断，如果关键字在这一行中则写入到要写入文件中
                            outcome.write(f"Title:{blur}\n{line}\n----------------------------------------\n")
            logging.info("Query results: pass")
        except Exception as e:
            logging.error(f"Query results: fail - {e}")


class Static_scanning(Tool_encapsulation):
    """静态扫描，使用jadx反编译apk获取AndroidManifest.xml文件
    apktool.jar： https://bitbucket.org/iBotPeaches/apktool/downloads/
    apktool.bat ： https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/windows/apktool.bat"""

    def __init__(self):
        super().__init__()

    def run(self):
        print('-------------------------------------------开始静态扫描-------------------------------------------')
        self.static_scanning()
        self.results()
        print('-------------------------------------------静态扫描结束-------------------------------------------')

    def static_scanning(self):
        # 运行jadx获取AndroidManifest.xml文件
        # jadx_cmd = f"{self.jadx_path} -d {self.outcome_path} -j 8 -v {self.apk_path}"  # jadx反编译apk
        # self.version_number(jadx_cmd)
        # os.system(f"{self.jadx_path} -d {self.outcome_path} -j 8 -v {self.apk_path}")
        # apktool_cmd = rf'{self.apktool_path}\apktool d {self.apk_path} -o {self.outcome_path}\resources'
        # self.version_number(apktool_cmd)
        os.system(rf'{self.apktool_path}\apktool d {self.apk_path} -o {self.outcome_path}\resources')

        move_cmd = rf'move {self.outcome_path}\resources\AndroidManifest.xml {self.outcome_path}\AndroidManifest.txt'
        self.version_number(move_cmd)

    def results(self):
        # 保存结果
        self.queries(
            rf'{self.outcome_path}\AndroidManifest.txt',
            f'{self.Permissions_list_path}',
            f'{self.Static_outcome_path}'
        )

        rmdir_resources = rf'rd /s /q {self.outcome_path}\resources'
        self.version_number(rmdir_resources)

        copy_cmd = rf'copy {self.Static_outcome_path} {self.outcome_path}\{self.apk_name}静态扫描结果.txt'
        self.version_number(copy_cmd)

        move_cmd = rf'move {self.outcome_path}\AndroidManifest.txt {self.outcome_path}\AndroidManifest.xml'
        self.version_number(move_cmd)


class Dynamic_scanning(Tool_encapsulation):
    """动态扫描，使用模拟器+xposed插件手动操作app扫描"""

    def __init__(self):
        super().__init__()
        install_cmd = rf'adb -s {self.device_id} install {self.apk_path}'  # 安卓要测试的apk
        self.version_number(install_cmd)

    def run(self):
        print('------------------------------------------开始动态扫描-------------------------------------------')
        states = {
            0: '同意用户须知前',
            1: '基础模式',
            2: '同意并继续',
            3: '不同意'
        }
        for i in range(len(states)):
            self.text = states[i]
            self.environment_setup()
            self.clear_data(f'{self.text}')
            self.operate()
            self.results()
        print('-------------------------------------------动态扫描结束-------------------------------------------')

    def environment_setup(self):
        # 环境搭建
        os.system(f"adb connect {self.device_id}")
        uiautomator2_cmd = "python -m uiautomator2 init"  # 下载atx-agent，推送到手机
        self.version_number(uiautomator2_cmd)
        logging.info(self.d.info)  # 查看设备基本信息，测试是否连接成功

        with open(rf'{self.outcome_path}\music.log', 'w') as f:  # 在桌面创建music.log文件,导入模拟器/data/local/tmp
            f.close()
        push_cmd = rf'adb -s {self.device_id} push {self.outcome_path}\music.log /data/local/tmp'
        self.version_number(push_cmd)

        # web_cmd = 'python -m weditor'  # 打开浏览器可视化界面，需要调试时放开
        # self.version_number(web_cmd)

    def clear_data(self, text):
        # 清除apk数据
        self.d.press("home")  # 回到桌面
        self.d(text="音乐").long_click()  # 长按apk桌面图标5s，触发操作面板
        self.d.xpath('//*[@text="应用信息"]').click()
        self.d.xpath('//*[@text="存储"]').click()
        self.d.xpath('//*[@text="清除数据"]').click()
        self.d.xpath('//*[@resource-id="android:id/button1"]').click()  # 点击 确认，执行清除操作
        self.d.press("home")  # 回到桌面
        time.sleep(1)
        self.d.xpath('//*[@text="音乐"]').click()  # 音乐桌面图标，启动音乐
        time.sleep(1)
        if text == '同意用户须知前':
            return
        elif text == '基础模式':
            self.d.xpath(f'//*[@text="同意并继续"]').click()  # 不同意/同意，触发部分功能受限须知弹窗
            time.sleep(1)
            input('请开启基础服务模式后输入任意字符继续测试......')
        else:
            self.d.xpath(f'//*[@text="{text}"]').click()
            time.sleep(1)
            if text == '不同意':
                if self.d.exists(text='使用游客模式'):
                    self.d.xpath('//*[@text="使用游客模式"]').click()  # 进入应用，进入应用首页
                else:
                    self.d.xpath('//*[@text="进入应用"]').click()

    def operate(self):
        # 在apk内的操作
        os.system('chcp 65001')
        os.system(f'start adb -s {self.device_id} shell tail -f /data/local/tmp/music.log')
        print(f'**{self.text}**执行动态扫描~')
        input('操作完成后输入任意字符继续......')
        self.d.press("home")  # 回到桌面

    def results(self):
        pull_music_log = rf'adb -s {self.device_id} pull /data/local/tmp/music.log {self.outcome_path}'  # 导出模拟器/data/local/tmp中的music.log文件
        self.version_number(pull_music_log)

        move = rf'move {self.outcome_path}\music.log {self.outcome_path}\music.txt'  # 修改music.log文件后缀为.txt
        self.version_number(move)

        self.queries(
            rf'{self.outcome_path}\music.txt',
            f'{self.Permissions_list_path}',
            rf'{self.Dynamic_outcome_path}'
        )

        copy_cmd = rf'copy {self.Dynamic_outcome_path} {self.outcome_path}\{self.apk_name}_{self.text}_动态扫描结果.txt'
        self.version_number(copy_cmd)

        move_cmd = rf'move {self.outcome_path}\music.txt {self.outcome_path}\{self.text}_music.txt'
        self.version_number(move_cmd)


if __name__ == "__main__":
    run_Static = Static_scanning()
    run_Dynamic = Dynamic_scanning()
    run_Static.run()
    # run_Dynamic.run()

    # static_threading = threading.Thread(target=run_Static.run)  # 静态扫描
    # Dynamic_threading = threading.Thread(target=run_Dynamic.run)  # 动态扫描
    # static_threading.start()
    # Dynamic_threading.start()
    # static_threading.join()
    # Dynamic_threading.join()
