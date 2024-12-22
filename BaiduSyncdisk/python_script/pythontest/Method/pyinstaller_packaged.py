# -*- coding:utf-8 -*-
# @Time: 2024/3/25  16：00
# @Author: J
import sys
import subprocess


# 运行示例：python pyinstaller_pack.py C:\Users\86173\Desktop\物料\exe.ico D:\BaiduSyncdisk\python_script\Tool\Assistant\Assistant.py

class Pack:
    """打包"""

    @staticmethod
    def pyinstaller_pack():
        if len(sys.argv) < 3:
            print(
                f"缺少必填参数!!!\n正确格式:python pyinstaller_pack.py icon.ico myapp.py myscript.py\n文件名称为空则默认使用需要打包的py文件的文件名")
            return
        try:
            # icon :exe文件icon图标; Name :exe文件名称; Mypy :需要打包的py文件
            (icon, Name, Mypy) = (sys.argv[1], None, sys.argv[2]) if len(sys.argv) == 3 else (
                sys.argv[1], sys.argv[2], sys.argv[3])

            # 文件名称为空则默认使用需要打包的py文件的文件名
            Name = [path.split('.')[0] for path in Mypy.split('\\') if '.py' in path][0] if Name is None else Name

            PT = ("pyinstaller -F -w --clean --icon=%s --name=%s %s" % (icon, Name, Mypy))
            print(f"开始执行打包指令~\n指令:{PT}\n")
            subprocess.run(PT)
        except Exception as e:
            print(
                f"{e}\n参数错误!!!\n正确格式:python pyinstaller_pack.py icon.ico myapp.py myscript.py\n文件名称为空则默认使用需要打包的py文件的文件名")


if __name__ == "__main__":
    run = Pack()
    run.pyinstaller_pack()
