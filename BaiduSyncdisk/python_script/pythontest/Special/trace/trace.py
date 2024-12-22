# -*- coding:utf-8 -*-
# @Time: 2023-10-12
# @Author: j
import os
import subprocess

def get_desktop_path():
    # 获取当前操作系统类型
    operating_system = os.name

    # 根据操作系统获取桌面路径
    if operating_system == 'posix':  # Linux, Unix, macOS
        path = os.path.expanduser('~/Desktop')
    elif operating_system == 'nt':  # Windows
        path = os.path.join(os.path.expanduser('~'), 'Desktop')
    else:
        # 其他操作系统暂不考虑
        path = None

    return path

def revise_config():
    input_duration = int(input('设置抓取时间(单位/秒)： '))
    duration = input_duration * 1000
    # 读取文件内容
    with open('config.pbtx', 'r', encoding='utf-8') as file:
        content = file.readlines()  # 读取所有行到一个列表中
    # 替换第一行内容
    if content:  # 确保文件不为空
        content[0] = f'duration_ms: {duration}\n'
    # 写入新内容
    with open('config.pbtx', 'w', encoding='utf-8') as file:
        file.writelines(content)  # 写入所有行

def sys_trace(path):
    revise_config()
    try:
        cmd_trace = (
            f'adb push config.pbtx /data/local/tmp/config.pbtx && '
            'adb shell -tt "cat /data/local/tmp/config.pbtx | perfetto --txt -c - -o /data/misc/perfetto-traces/trace.perf" && '
            f'adb pull /data/misc/perfetto-traces/trace.perf {os.path.join(path, "trace.perf")}'
        )
        print(cmd_trace)
        subprocess.run(cmd_trace, check=True, shell=True, text=True)
        print("已将Trace文件发送至桌面：" + path)
    except subprocess.CalledProcessError as e:
        print("命令执行失败：", e)
    except Exception as e:
        print("发生错误：", e)

if __name__ == '__main__':
    desktop_path = get_desktop_path()
    if desktop_path:
        sys_trace(desktop_path)
    else:
        print("无法确定桌面路径")