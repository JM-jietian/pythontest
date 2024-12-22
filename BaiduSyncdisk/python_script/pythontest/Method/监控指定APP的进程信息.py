# -*- coding: utf-8 -*-
# @Time: 2023/7/25  10：00
# @Author: j
import tkinter as tk
from tkinter import scrolledtext
import time
import subprocess
import threading
import os

waiting_message_shown = False
stop_event = threading.Event()  # 用于通知线程停止的 Event 对象
running_process = None  # 用于存储运行的线程对象


def clear_text():
    """清空多行文本框内容"""
    Output.delete(1.0, tk.END)


def Output_insert(txt):
    Output.insert(tk.END, txt)
    root.update()  # 更新文本框
    Output.see(tk.END)  # 将文本框滚动到最底部


def get_desktop_path():
    # 获取当前操作系统类型
    operating_system = os.name

    # 根据操作系统获取桌面路径
    if operating_system == 'posix':  # Linux, Unix, macOS
        desktop_path = os.path.expanduser('~/Desktop')
    elif operating_system == 'nt':  # Windows
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    else:
        # 其他操作系统暂不考虑
        desktop_path = None

    return desktop_path


def check_device_connection():
    try:
        # 使用subprocess模块执行adb devices命令并获取输出
        cmd = "adb devices"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            device_lines = result.stdout.splitlines()
            if len(device_lines) >= 3:
                return True
    except Exception as e:
        Output_insert(f"检查设备连接状态发生错误: {e}")
    return False


# 写入状态信息到文件
def write_status_to_file(output_file, status):
    current_time = time.strftime("%H:%M:%S", time.localtime())
    with open(output_file, "a") as f:
        f.write(f"{current_time}\t{status}\n")


# 监控指定APP的进程信息
def monitoring_app_process(package_name):
    global waiting_message_shown, running_process
    desktop = get_desktop_path()
    output_file = rf"{desktop}\{package_name}_ps.txt"
    with open(output_file, "w") as f:
        f.write("时间戳\t进程信息\n")

    connected = False
    pause_monitoring = False
    last_disconnected_time = None

    while not stop_event.is_set():  # 检查 Event 是否被设置
        try:
            if not connected:
                if check_device_connection():
                    status = "设备已连接"
                else:
                    status = "等待连接设备..."
                    if not waiting_message_shown:
                        Output_insert(status + "\n")
                        waiting_message_shown = True
                    time.sleep(5)
                    continue

                Output_insert(status + "\n")
                connected = True
                waiting_message_shown = False

            if connected:
                cmd = "adb shell ps | findstr {package_name}".format(package_name=package_name)
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=False)

                if result.returncode == 0:
                    process_lines = result.stdout.splitlines()
                else:
                    process_lines = []

                current_time = time.strftime("%H:%M:%S", time.localtime())
                with open(output_file, "a") as f:
                    if not process_lines:
                        f.write(f"{current_time}\t未找到进程\n")
                        Output_insert(f"{current_time}\t未找到进程\n")

                    else:
                        for process_info in process_lines:
                            f.write(f"{current_time}\t{process_info}\n")
                            Output_insert(f"{current_time}\t{process_info}\n")

            if connected and not check_device_connection():
                if last_disconnected_time is None or time.time() - last_disconnected_time >= 10:
                    status = "设备已断开连接"
                    Output_insert(status + "\n")
                    last_disconnected_time = time.time()
                    connected = False
                    waiting_message_shown = False
        except Exception as e:
            Output_insert(f"发生错误: {e}")

        time.sleep(3)


def start_monitoring():
    user_input = entry_var.get()
    label.config(text="接收到的输入： " + user_input)
    Output_insert("正在运行......\n")
    outcome = "运行结果：\n"
    Output_insert(outcome)
    Output.see(tk.END)  # 将文本框滚动到最底部

    global running_process
    stop_event.clear()  # 清除 Event 状态
    running_process = threading.Thread(target=monitoring_app_process, args=(user_input,))
    running_process.start()


def stop_monitoring():
    global stop_event
    stop_event.set()  # 设置 Event，通知线程停止
    Output_insert("监控结束\n")


if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    root.title("Process monitoring")
    # 设置主窗口的最小宽度和最小高度
    root.minsize(width=800, height=800)
    # 设置主窗口的最大宽度和最大高度
    root.maxsize(width=2500, height=2500)

    # 创建 StringVar 对象，用于关联 Entry 的文本
    entry_var = tk.StringVar()

    # 创建一个多行文本框，指定宽度和高度，并允许随着主窗口变化而变化
    Output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
    Output.pack(padx=10, pady=10, expand=True, fill="both")

    # 创建标签、文本框和按钮
    label = tk.Label(root, text="输入要监控的程序名:")
    entry = tk.Entry(root, textvariable=entry_var)
    # 创建 "开始运行" 按钮
    start_button = tk.Button(root, text="开始运行", command=start_monitoring)
    # 创建 "结束运行" 按钮
    stop_button = tk.Button(root, text="结束运行", command=stop_monitoring)
    # 创建 "结束运行" 按钮
    clear_text_button = tk.Button(root, text="清空文本", command=clear_text)

    # 布局管理
    label.pack()
    entry.pack(padx=400, fill="both")
    clear_text_button.pack(pady=5)
    start_button.pack(side='left', padx=(400, 0), pady=5, expand=True, fill="both")
    stop_button.pack(side='right', padx=(0, 400), pady=5, expand=True, fill="both")

    # 运行主循环
    root.mainloop()
