# -*- coding:utf-8 -*-
# @Time: 
# @Author: TJ
import os
import subprocess
import threading


class Storage(object):
    # 填充存储
    def __init__(self):
        self.FilePath = None
        self.FileSize = None
        self.NumberOfFiles = None
    
    @staticmethod
    def devices():
        """if 条件语句用于筛选出不为空的设备号。因为如果 split('\t')[0] 之后得到的字符串为空，则说明这一行并不是设备号，而是其它信息（如标题行等），需要被过滤掉"""
        return [line.split('\t')[0].strip() for line in os.popen('adb devices').readlines()[1:] if
                line.split('\t')[0].strip()]

    def storage(self):
        try:
            if len(self.devices()) == 0:
                return print(f"没有已连接的设备.\n")  # 判断有无设备连接
            elif len(self.devices()) > 1:
                return print(f"多设备连接，运行此功能时请确保仅连接一台设备！！！\n")
            for device in self.devices():
                print(f"当前设备：{device}\t状态：", end='')
                adb_d = os.system(f"adb -s {device} get-state")
                if adb_d:
                    print(f'设备{device}\t已断开连接\n')
                    continue
            try:
                self.FilePath = input("填充文件路径： ")
                self.FileSize = int(input("填充文件大小： "))
                self.NumberOfFiles = int(input("填充文件数量： "))
            except ValueError:
                return print(f"FileSize & NumberOfFiles 请输入正整数！！！\n")

            storage = 'adb shell df -h /data/media'
            you_storage = subprocess.Popen(storage, text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"设备剩余存储：\n{you_storage.communicate()[0]}\n")

            FP = f'adb shell mkdir {self.FilePath}'
            FP_text = subprocess.Popen(FP, text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if 'Read-only file system' in FP_text.communicate()[1]:
                return print(f"文件[{self.FilePath}]\t创建失败，请检查输入的路径是否正确！！！\n")

            print(f"文件[{self.FilePath}]\t正在创建中，请稍后...\n")
            Name = 1
            for i in range(self.NumberOfFiles):
                create = f'adb shell dd if=/dev/zero of={self.FilePath}FileName{Name} bs=1048576 count={self.FileSize}'
                create_num = subprocess.Popen(create, text=True, shell=True, stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
                print(f"{create_num.communicate()[1]}\n")
                Name += 1
            you_storage = subprocess.Popen(storage, text=True, shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
            print(f"创建完成，设备剩余存储：\n{you_storage.communicate()[0]}")
            del_FilePath = input("yes.清除填充文件|no.退出\n： ")
            if del_FilePath == "yes":
                self.del_storage()
            else:
                return print(f"结束运行，填充的文件路径：{self.FilePath}")

        except Exception as e:
            return print(f"{e}\t缺少必填参数！！！\n")

    def del_storage(self):
        # 删除填充的文件夹  /storage/emulated/0//Music/song/
        del_FilePath = f'adb shell rm -r {self.FilePath}'
        subprocess.Popen(del_FilePath, shell=True)
        print(f"文件[{self.FilePath}]\t已清除~\n")

    def storage_threading(self):
        storage = threading.Thread(target=self.storage)
        storage.start()

if __name__ == "__main__":
    run = Storage()
    run.storage_threading()