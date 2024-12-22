import os
import subprocess


import os

def add_to_path_if_not_exists(directory_path):
    # 获取系统PATH环境变量
    paths = os.environ.get('PATH', '')
    # 根据操作系统使用正确的路径分隔符
    path_separator = os.pathsep
    # 检查目录路径是否已经在PATH中
    if directory_path in paths.split(path_separator):
        print(f"路径 {directory_path} 已在PATH中。")
        return

    # 如果路径不在PATH中，将其添加进去
    if not paths.endswith(path_separator):
        new_path = paths + path_separator + directory_path
    else:
        new_path = paths + directory_path

    # 更新环境变量，这只会影响当前进程及其子进程
    os.environ['PATH'] = new_path
    print(f"路径 {directory_path} 已添加到PATH环境变量中。")

    # 如果需要永久修改环境变量，需要根据操作系统进行不同的操作
    # 以下代码以Windows系统为例，使用setx命令永久添加到系统PATH
    # 需要以管理员权限运行Python脚本
    try:
        import ctypes
        ctypes.windll.kernel32.SetEnvironmentVariableW("PATH", new_path)
        print(f"路径 {directory_path} 已永久添加到系统PATH环境变量中。")
    except Exception as e:
        print(f"添加路径到系统PATH环境变量失败：{e}")

# 使用示例
file_to_check = "C:\python\python.exe"  # 替换为你想要检查的文件名
add_to_path_if_not_exists(file_to_check)