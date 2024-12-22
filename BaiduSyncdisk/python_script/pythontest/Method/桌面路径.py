import os


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


if __name__ == '__main__':
    # 使用示例
    Desktop_path = get_desktop_path()
    if Desktop_path:
        print(f"桌面路径是：{Desktop_path}")
    else:
        print("无法确定桌面路径，未知操作系统或不支持的操作系统。")
