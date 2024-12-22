import os
import subprocess
import threading


class Memory(object):
    # 内存占用
    @staticmethod
    def devices():
        """if 条件语句用于筛选出不为空的设备号。因为如果 split('\t')[0] 之后得到的字符串为空，则说明这一行并不是设备号，而是其它信息（如标题行等），需要被过滤掉"""
        return [line.split('\t')[0].strip() for line in os.popen('adb devices').readlines()[1:] if line.split('\t')[0].strip()]
    def memory(self):
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
            # 获取设备内存信息
            cmd = f'adb shell "cat /proc/meminfo | grep MemAvailable"'
            you_memory = subprocess.Popen(cmd, text=True, shell=True, stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
            memory_num = int(you_memory.communicate()[0].split()[1]) / 1024
            print(f"设备剩余内存: {memory_num}M\n")

            # 计算要占用的内存大小
            input_rom = int(input("输入需要占用的内存大小/M： "))
            rom_num = input_rom * 1048576
            print(
                f"设备运行内存占用中，占用大小: {input_rom}M，结束运行后恢复...\n"
                f"【注意：在结束占用前，重复会叠加占用的内存！！！】\n")

            # 使用 dd 命令占用内存
            rom_cmd = f'adb shell dd if=/dev/zero of=/dev/null bs={rom_num}'
            subprocess.run(rom_cmd, shell=True)

        except Exception as e:
            print(f"异常：{e}\n")


    def startMemory_threading(self):
        memory = threading.Thread(target=self.memory)
        memory.start()

if __name__ == "__main__":
    run = Memory()
    run.startMemory_threading()