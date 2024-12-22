import os


def delete_files_with_extension(folder_path, extension):
    # 检查文件夹路径是否存在
    if not os.path.exists(folder_path):
        print("文件夹路径不存在")
        return

    # 确保扩展名以点开头
    if not extension.startswith('.'):
        extension = '.' + extension

    # 遍历文件夹及其子文件夹中的所有文件
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)

            # 检查文件后缀名
            if filename.endswith(extension):
                try:
                    os.unlink(file_path)
                    print(f"已删除文件：{file_path}")
                except Exception as e:
                    print(f"删除文件 {file_path} 时出错：{e}")


# 使用示例
folder_path = '/path/to/your/folder'
extension = '.txt'  # 假设我们要删除所有.txt文件
delete_files_with_extension(folder_path, extension)