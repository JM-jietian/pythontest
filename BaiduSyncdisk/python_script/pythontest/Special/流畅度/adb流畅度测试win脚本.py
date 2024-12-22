# -*- coding:utf-8 -*-
# @Time: 2023-11-20
# @Author: j
import random
import subprocess
from pandas import DataFrame
from concurrent.futures import ThreadPoolExecutor
import shutil
import time
import os
import traceback
import adbutils

# ============初始化配置start=======================
# 安卓手机设备号
device_name = "a1fb8408"
# 存储测试报告路径
report_path = r'D:\BaiduSyncdisk\python_script\专项\流畅度\流畅度结果'
# apk包名 示例：com.heytap.music  //网易云 com.netease.cloudmusic
package_name = 'com.heytap.music'
# 是否需要自动滑动
is_move = True  # True 执行自动滑动  || False 手动滑动，只统计流畅率
# 是否在流畅度不达标时抓取Trase
is_trase = True
# 需要执行流畅度测试次数
num_max = 50
# 每隔x秒抓取一次janky_frames数据
wait_time = 10
# 测试场景数据adb shell
case_list = [
    # Android平台的坐标系是以屏幕左上角为初始坐标（0, 0）
    # swipe_pos：[[屏幕宽的初始百分比, 屏幕高的初始百分比], [屏幕宽x结束百分比, 屏幕高x结束百分比]]  示例：0.50 = 屏幕宽或高50%的位置
    # random_speed：为一次滑动的随机时间范围，单位:ms（毫秒）

    {'name': '首页', 'swipe_pos': [[0.20, 0.80], [0.80, 0.20]], 'random_speed': [200, 200], 'desc': '首页流畅度测试'},
    # {'name': '本地音乐', 'swipe_pos': [[0.50, 0.60], [0.50, 0.40]], 'random_speed': [300, 300], 'desc': '本地音乐流畅度测试'},
    # {'name': '播放页面', 'swipe_pos': [[0.90, 0.50], [0.30, 0.50]], 'random_speed': [300, 300], 'desc': '播放页面流畅度测试'},
    # {'name': '我的音乐', 'swipe_pos': [[0.50, 0.60], [0.50, 0.40]], 'random_speed': [300, 300], 'desc': '我的音乐流畅度测试'},
    # {'name': '歌单广场', 'swipe_pos': [[0.50, 0.60], [0.50, 0.40]], 'random_speed': [300, 300], 'desc': '歌单广场流畅度测试'},
    # {'name': '最近播放', 'swipe_pos': [[0.50, 0.70], [0.50, 0.30]], 'random_speed': [300, 300], 'desc': '最近播放流畅度测试'},
    # {'name': '听书页面', 'swipe_pos': [[0.50, 0.60], [0.50, 0.40]], 'random_speed': [300, 300], 'desc': '听书页面流畅度测试'},
    # {'name': '听书排行榜', 'swipe_pos': [[0.50, 0.60], [0.50, 0.40]], 'random_speed': [300, 300], 'desc': '听书排行榜流畅度测试'},
]


# ============初始化配置end==========================case_list[0]['name']
def sys_trace():
    trace_path = r"%s\%s" % (report_path, file_name)
    os.system('chcp 65001')  # 更改cmd的编码方式防止输出乱码
    cmd_trace = (r'adb push D:\BaiduSyncdisk\python_script\专项\trace\config.pbtx /data/local/tmp/config.pbtx && '
                 r'adb shell "cat /data/local/tmp/config.pbtx | perfetto --txt -c - -o /data/misc/perfetto-traces/trace.perf" && '
                 rf'adb pull /data/misc/perfetto-traces/trace.perf {trace_path}')
    subprocess.run(cmd_trace, text=True, shell=True)

    cmd_move = rf'move {trace_path}\trace.perf {trace_path}\{device_name}_{case_list[0]["name"]}_trace.perf'
    subprocess.run(cmd_move, text=True, shell=True)
    print(f"已抓取Trace文件发送至: {trace_path}")


def rand_speed(num_list):
    return round((random.randint(num_list[0], num_list[1])), 5)


def out_hand_swipe(pos_list, duration):
    conmmd = r'input swipe %s %s %s %s %s' % (pos_list[0][0], pos_list[0][1], pos_list[1][0], pos_list[1][1], duration)
    device.shell(conmmd)


def adb_input():
    global dict_info
    global is_on_page
    global is_start
    try:
        is_on_page = True
        if is_move:
            while is_start:
                conmmd1 = "input tap 36 146"
                device.shell(conmmd1)
                time.sleep(0.5)
                conmmd2 = "input tap 48 2100"
                device.shell(conmmd2)
                time.sleep(0.5)
    except Exception as e:
        is_on_page = False
        is_start = False
        print(f'<br>滑动方法调用异常: %s %s<br>' % (traceback.format_exc(), e))
        return


def loop_move_task():
    # 循环移动指定坐标组
    global dict_info
    global is_on_page
    global is_start
    try:
        pos_list = dict_info['swipe_pos']
        swipe_pos = [[int(int(width) * pos_list[0][0]), int(int(height) * pos_list[0][1])],
                     [int(int(width) * pos_list[1][0]), int(int(height) * pos_list[1][1])]]
        print("转换后的滑动坐标列表:%s" % swipe_pos)
        back_pos = [swipe_pos[1], swipe_pos[0]]
        random_speed = dict_info['random_speed']
        time.sleep(1)
        is_on_page = True
        if is_move:
            while is_start:
                speed = rand_speed(random_speed)
                out_hand_swipe(swipe_pos, speed)
                out_hand_swipe(back_pos, speed)
    except Exception as e:
        is_on_page = False
        is_start = False
        print(f'<br>滑动方法调用异常: %s %s<br>' % (traceback.format_exc(), e))
        return


def reset_gfxinfo():
    # 重置gfxinfo信息
    for i in range(50):
        y = device.shell("dumpsys gfxinfo %s reset" % package_name)
        ys = y.strip().splitlines()
        if len(ys) < 8:
            print(f'请检查当前测试机安装的apk包名是否与预设的包名【{package_name}】一致')
        print("[YS7]: %s" % ys[7])
        if ys[7] == 'Janky frames: 0 (0.00%)':
            print('重置完成：' + (ys[7])[:-1])
            return True
    time.sleep(2)
    return False


def get_gfxinfo():
    # gfxinfo信息分析
    t = device.shell("dumpsys gfxinfo %s" % package_name)
    tr = t.strip().splitlines()

    total_janky_frames = tr[6][22:].strip()  # 总帧数
    janky = tr[7].strip()[13:].split("(")  # 掉帧数

    return [janky[0].strip(), total_janky_frames]


def start():
    global dict_info
    global is_start
    global is_on_page
    global is_trase
    try:
        report_name = dict_info['name']
        filename = r'%s\%s\%s.csv' % (report_path, file_name, (case_list[0]['name']))
        n = 0
        time_max = (num_max * wait_time) + 10
        time_inti = 0
        frame_drop = 0  # 累计掉帧次数
        total_frame_drop = 0  # 累计掉帧帧数
        total_frame_num = 0  # 累计绘制帧数
        # 新增指标
        min_fluency_rate = float('inf')
        max_frame_drop_single = 0
        max_frame_drop_10s = 0
        total_draw_time = 0
        total_janky_frames_10s = 0
        # csv数据准备
        title_name = {'time': "开始时间", 'janky_frames': "单次掉帧数", 'total_frames': "单次绘制帧数",
                      'fluency_rate': "应用流畅率均值(建议值≥98%)", 'frame_drop': "累计掉帧次数",
                      'total_frame_drop': "累计掉帧帧数", 'total_frame_num': "累计绘制帧数",
                      'min_fluency_rate': "应用流畅度最小值", 'max_frame_drop_single': "绘制一次的最大掉帧数",
                      'max_frame_drop_10s': "绘制10S的最大掉帧总数", 'total_draw_time': "累计绘制时间"}
        # 添加初始化 'janky_frames_list'd
        janky_frames_dict = {'time': [], 'janky_frames': [], 'total_frames': [], 'fluency_rate': [],
                             'frame_drop': [], 'total_frame_drop': [], 'total_frame_num': [],
                             'min_fluency_rate': [], 'max_frame_drop_single': [],
                             'max_frame_drop_10s': [], 'total_draw_time': []}
        # 首选清空之前的数据，并重新写入标题名称
        df = DataFrame(title_name, index=[0])
        df.to_csv(filename, mode='w', encoding="utf-8", index=False, header=False)
        report_data = {'report_name': report_name, 'fluency_rate': janky_frames_dict['fluency_rate'],
                       'frame_drop': janky_frames_dict['frame_drop'],
                       'total_frame_drop': janky_frames_dict['total_frame_drop'],
                       'total_frame_num': janky_frames_dict['total_frame_num'], 'min_fluency_rate': min_fluency_rate,
                       'max_frame_drop_single': max_frame_drop_single, 'max_frame_drop_10s': max_frame_drop_10s,
                       'total_draw_time': total_draw_time}
        while True:
            time.sleep(1)
            if n >= num_max:
                is_start = False
                is_on_page = False
                # 新增测试报告
                report_data['report_name'] = report_name
                report_data['fluency_rate'] = janky_frames_dict.get('fluency_rate', 0)
                report_data['frame_drop'] = janky_frames_dict.get('frame_drop', 0)
                report_data['total_frame_drop'] = janky_frames_dict.get('total_frame_drop', 0)
                report_data['total_frame_num'] = janky_frames_dict.get('total_frame_num', 0)
                report_data['min_fluency_rate'] = min_fluency_rate
                report_data['max_frame_drop_single'] = max_frame_drop_single
                report_data['max_frame_drop_10s'] = max_frame_drop_10s
                report_data['total_draw_time'] = total_draw_time
                df_report_end = DataFrame(report_data, index=[0])
                df_report_end.to_csv(report_file, mode='a', encoding="utf-8", index=False, header=False)
                break
            elif n < num_max:
                n += 1
                print(
                    "==========================【警告】流畅度测试期间，请不要操作手机或查看csv数据文件，以免影响数据写入！【警告】==========================")
                print("当前次数：%s,总计%s次,场景数据文件路径:%s" % (n, num_max, filename))
                jk_time = str(int(time.time()))
                time.sleep(wait_time)
                janky_frames_info = get_gfxinfo()
                janky_frames = int(janky_frames_info[0]) - total_frame_drop
                total_frames = int(janky_frames_info[1]) - total_frame_num
                print("【%s秒内-掉帧数】:%s" % (wait_time, janky_frames))
                print("【%s秒内-总绘帧数】:%s" % (wait_time, total_frames))
                if janky_frames > 0:
                    frame_drop += 1
                    # 更新最大掉帧数
                    max_frame_drop_single = max(max_frame_drop_single, janky_frames)
                    max_frame_drop_10s = max(max_frame_drop_10s, janky_frames)
                total_frame_drop = int(janky_frames_info[0])
                total_frame_num = int(janky_frames_info[1])
                fluency_rate = 1 - (total_frame_drop / total_frame_num)
                fluency_rate = round(fluency_rate, 5)
                fluency_rate = fluency_rate * 100
                print("【APP当前流畅率】:%s" % fluency_rate)
                is_trase = [True if is_trase and fluency_rate < 98 and n > 1 else False]  # 流畅度小于98不达标，且不达标次大于10次则抓取trase
                # 更新最小流畅度
                min_fluency_rate = min(min_fluency_rate, fluency_rate)
                print("【应用流畅度最小值】:%s" % min_fluency_rate)
                # 计算10s的掉帧总数和绘制时间
                total_janky_frames_10s += janky_frames
                print("【累积掉帧数】:%s" % total_janky_frames_10s)
                total_draw_time += wait_time
                print("【累计绘制时间】:%ss" % total_draw_time)
                janky_frames_dict['time'].append(jk_time)
                janky_frames_dict['janky_frames'] = janky_frames
                janky_frames_dict['total_frames'] = total_frames
                janky_frames_dict['fluency_rate'] = fluency_rate
                janky_frames_dict['frame_drop'] = frame_drop
                janky_frames_dict['total_frame_drop'] = total_frame_drop
                janky_frames_dict['total_frame_num'] = total_frame_num
                janky_frames_dict['min_fluency_rate'] = min_fluency_rate
                janky_frames_dict['max_frame_drop_single'] = max_frame_drop_single
                janky_frames_dict['max_frame_drop_10s'] = max_frame_drop_10s
                janky_frames_dict['total_draw_time'] = total_draw_time
                df = DataFrame(janky_frames_dict, columns=title_name.keys())
                df.to_csv(filename, mode='a', encoding="gbk", index=False, header=False)
            if time_inti > time_max:
                is_start = False
                is_on_page = False
                break
            time_inti += 1
    except Exception as e:
        print("统计流畅度数据异常: %s %s" % (traceback.format_exc(), e))
        is_start = False
        is_on_page = False
        return False


if __name__ == '__main__':
    dict_info = {}
    device_name = str(device_name)
    print("device设备号:%s" % device_name)

    adb = adbutils.AdbClient()  # 创建ADB客户端对象
    device = adb.device(serial=device_name)  # 获取指定设备

    # 获取手机分辨率
    size_text = device.shell("wm size")
    output = size_text.strip()
    resolution = output.split(' ')[2]
    width, height = resolution.split('x')
    print('手机分辨率:', resolution)
    # 开始之前，删除旧的测试报告目录
    start_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))  # 获取当前时间
    file_name = "%s_%s_%s" % (f"fluency_test_{(case_list[0]['name'])}", device_name, start_time)
    if os.path.isdir("%s/%s" % (report_path, file_name)):  # 先判断下是否有旧目录
        shutil.rmtree("%s/%s" % (report_path, file_name))  # 有的话会删除之前的目录
        time.sleep(1)
    os.mkdir("%s/%s" % (report_path, file_name))  # 再创建这个设备号的对应目录，存放性能测试数据csv文件
    # 创建线程池执行器
    executor = ThreadPoolExecutor(max_workers=5)  # 使用多线程玩法
    # 创建测试报告csv文件
    report_title = {'report_name': "场景名称", 'fluency_rate': "应用流畅率均值(建议值≥98%)",
                    'frame_drop': "累计掉帧次数", 'total_frame_drop': "累计掉帧帧数",
                    'total_frame_num': "累计绘制帧数", 'min_fluency_rate': "应用流畅度最小值",
                    'max_frame_drop_single': "绘制一次的最大掉帧数", 'max_frame_drop_10s': "绘制10S的最大掉帧总数",
                    'total_draw_time': "累计绘制时间"}

    report_file = '%s/%s/%s_report.csv' % (report_path, file_name, (case_list[0]['name']))
    df_report = DataFrame(report_title, index=[0])  # 会按顺序添加 , 这里加了个索引设置，防止报错
    df_report.to_csv(report_file, mode='w', encoding="utf-8", index=False, header=False)  # 这里是覆盖写入，会清空之前的数据
    tmp_dir = "%s/%s" % (report_path, file_name)
    for case in case_list:
        dict_info = case
        is_start = True  # 是否开始
        start_status = False  # 是否可以开始统计掉帧信息
        if reset_gfxinfo() is False:
            print('提示：adb重置手机掉帧率统计记录失败，请检查【开发者模式】-【dumpsys gfxinfo统计】是否开启！！！')
            break
        if is_move:  # 开始测试前-先重置手机设备上的历史掉帧率相关记录
            is_on_page = False  # 是否进入页面
            executor.submit(loop_move_task)  # 开始执行模拟人工场景操作
        else:
            is_on_page = True  # 不执行自动滑动操作
        while True:
            # 这里加个等待逻辑，需要上一个用例场景测试完成后，再执行下一个
            time.sleep(1)
            if is_start is False:
                # 需要判断当前流畅度数据已统计和trace报告已生成后，再开始下一个用例
                time.sleep(5)  # 等待5s，防止太快会报错
                print('当前用例场景测试已完成！')
                if is_trase:
                    executor.submit(sys_trace)
                break
            elif is_on_page and start_status is False:
                print("开始监控帧率数据以及写入csv表格")
                executor.submit(start)  # 开始监控janky数据以及写入csv表格
                start_status = True
    time.sleep(2)
    # 因挂载的ftp目录有写入权限报错问题，需要先把报告文件写在临时目录里，结束后再把报告文件移动到ftp目录去
    print('temp_dir:%s' % tmp_dir)
    print("==========================全部场景流畅度测试已完成，请查看测试数据和报告对比！==========================")
