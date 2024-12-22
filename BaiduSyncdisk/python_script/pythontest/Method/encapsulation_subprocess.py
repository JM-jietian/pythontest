import logging
import subprocess

# 设置日志
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Log(object):
    def __init__(self, ):
        self.log_file = 'LOG.log'
        # 初始化日志记录器
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # 创建文件处理器，并设置级别为INFO
        # fh = logging.FileHandler(self.log_file, mode='w', encoding='utf-8')  # 存储到日志文件
        fh = logging.StreamHandler()  # 控制台输出
        fh.setLevel(logging.INFO)

        # 创建并设置日志格式
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)

        # 添加处理器到日志记录器
        self.logger.addHandler(fh)


class Subprocess(Log):
    def run(self, cmd):
        logging.info(f'执行指令：{cmd}')
        try:
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode('gbk')
            self.logger.info(output)
            return output.strip()
        except subprocess.CalledProcessError as e:
            self.logger.error("Command '%s' failed with error: %s", cmd, e.output.decode('gbk'))
            return None
