import os
import re
import threading


def find_file_partial(file_pattern, search_path='/'):
    # 输出指定文件完整路径
    found = None
    found_event = threading.Event()

    def search_files():
        nonlocal found
        for root, dirs, files in os.walk(search_path):
            for file_name in files:
                if re.search(file_pattern, file_name):
                    found = os.path.abspath(root)  # 返回文件的完整路径
                    # found = os.path.join(root, file_name)  # 相对路径
                    found_event.set()  # 通知主线程
                    return

    thread = threading.Thread(target=search_files)
    thread.start()
    found_event.wait()  # 等待搜索完成
    thread.join()  # 确保线程结束
    return found


if __name__ == '__main__':
    path = find_file_partial('.log')
    print(path)
