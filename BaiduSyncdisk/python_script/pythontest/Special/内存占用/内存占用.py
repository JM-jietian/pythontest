# -*- coding:utf-8 -*-
# @Time: 2023-5-28
# @Author: TJ
import os
import re
import subprocess
import time


def run_once_mem(cmd):
    try:
        # 使用subprocess.run执行命令，并捕获输出
        result = subprocess.run(cmd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            # 如果命令执行成功，返回标准输出和返回码
            return result.stdout, result.returncode
        else:
            # 如果命令执行失败，打印错误信息，并返回标准输出和返回码
            print(f"命令执行失败: {cmd}\n错误信息: {result.stderr}")
            return result.stdout, result.returncode
    except Exception as e:
        # 如果执行过程中出现异常，打印异常信息，并返回空字符串和错误码-1
        print(f"执行命令时发生错误: {e}")
        return "", -1


def parse_memory(output):
    # 使用正则表达式匹配输出中的内存使用总量
    mem = re.compile('TOTAL[ ]+(\d+)[ ]+.*')
    resmem = mem.findall(output)
    if resmem:
        # 如果匹配到，返回第一个匹配值转换为整数
        return int(resmem[0])
    return 0


if __name__ == "__main__":
    global mem_value
    file_name = 'res2.txt'
    # 如果结果文件已存在，则删除
    if os.path.exists(file_name):
        os.remove(file_name)

    # 初始化总内存使用量、计数器和临时峰值变量
    summem = countmem = 0
    tempmem = 0
    # 记录脚本开始执行的时间
    time1 = time.time()

    # 循环执行内存检测命令
    for i in range(1, 301):  # 根据测试时间修改
        cmdmem = 'adb shell dumpsys meminfo com.heytap.music'  # 构建内存检测命令
        outmem, codemem = run_once_mem(cmdmem)  # 执行命令并获取输出

        if codemem == 0:
            # 如果命令执行成功，解析输出获取内存使用量
            mem_value = parse_memory(outmem)
            summem += mem_value  # 累加内存使用量
            countmem += 1  # 计数器加1
            if mem_value > tempmem:
                # 更新内存使用峰值
                tempmem = mem_value

        # 打印每次循环的内存使用量
        print(f"Iteration {i}: Memory {mem_value} KB")

    # 记录脚本结束执行的时间，并计算总运行时间
    time2 = time.time()
    time_elapsed = time2 - time1

    # 打印运行时间、内存使用均值和峰值
    print(f'运行时间：{time_elapsed:.2f} s')
    print(f'内存均值：{summem / countmem / 1024.0:.2f} MB')
    print(f'内存峰值：{tempmem / 1024.0:.2f} MB')