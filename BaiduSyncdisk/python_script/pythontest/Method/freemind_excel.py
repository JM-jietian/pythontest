# -*- coding:utf-8 -*-
# @Time: 2023/5/26  12：00
# @Author: J

import pandas as pd
import xml.etree.ElementTree as ET
from tqdm import tqdm


def parse_node(node):
    node_text = node.attrib.get('TEXT', '')  # 获取节点文本
    children_data = []
    for child in node:
        children_data.extend(parse_node(child))  # 递归解析子节点
    if children_data:
        # 将节点文本和子节点数据合并到一个列表
        return [[node_text] + row for row in children_data]
    else:
        # 只有节点文本
        return [[node_text]]


def free_mind_to_excel(input_file, output_file):
    # 解析FreeMind文件
    tree = ET.parse(input_file)
    root = tree.getroot()

    # 解析节点数据
    data = parse_node(root)

    # 确定最大列数
    max_columns = max(len(row) for row in data)

    # 填充缺失的列
    for row in data:
        row.extend([''] * (max_columns - len(row)))

    # 创建DataFrame对象
    df = pd.DataFrame(data)

    # 设置列名
    column_names = ['all', '版本', '编写人员', '需求', '测试点', '一级模块', '二级模块', '前置条件', '操作步骤',
                    '预期结果', '用例严重程度']
    if max_columns < len(column_names):
        column_names = column_names[:max_columns]
    elif max_columns > len(column_names):
        column_names.extend(['all'] * (max_columns - len(column_names)))
    df.columns = column_names

    # 删除列名为all的空列表
    df.drop(['all'], axis=1, inplace=True)

    # 保存为Excel文件
    with tqdm(total=len(df), desc="正在保存Excel文件") as pbar:
        for i, row in df.iterrows():
            # 处理每一行数据
            ...
            # 更新进度条
            if int(i) % 10 == 0:
                pbar.update(int(i))
                if pbar.n >= pbar.total:
                    pbar.set_postfix({"状态": "已完成"})

                else:
                    pbar.set_postfix({"状态": "未完成"})
        df.to_excel(output_file, index=False, engine='xlsxwriter', encoding='utf-8')


if __name__ == '__main__':
    free_mind_path = r'C:\Users\Administrator\Desktop\oppo海外在线音乐15.7.20版本需求用例编写.mm'
    free_mind_to_excel(free_mind_path, free_mind_path.split('mm')[0] + 'xlsx')  # 将xlsx文件保存在.mm文件同目录下

    # 删除原文件
    # os.remove(r'C:\Users\Administrator\Downloads\Sheet1.mm')
