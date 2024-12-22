# -*- coding:utf-8 -*-
import base64
import os
import time
import requests
import pyautogui
import pyperclip
import webbrowser
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SignatureService:
    def __init__(self):
        self.d = None
        self.wait = None
        self.href = None
        self.download_links = []
        self.webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/f628e2ab-2ad1-442f-a911-22ccbf13f0c0"  # 飞书机器人的Webhook URL
        self.url = 'https://noah.myoas.com/micro-app/scbs/signature/signatureApplication/add-signature'
        self.path_list = self.walk_directory(Path(r'E:\feishu\signature'))
        self.accounts = {"username": "13760638450", "password": "Aa121314&"}
        self.disposition_list = [{"签名包": "heytap", "签名类型": "heytap_music", "签名项目": "PSW/MSM1901_11.0/19065",
                                  "签名种类": "V3_single"},
                                 {"签名包": "oppo_v3", "签名类型": "oppo_music", "签名项目": "PSW/MSM1802_10.0/18097",
                                  "签名种类": "V3_double"},
                                 {"签名包": "media_v3", "签名类型": "oppo_music", "签名项目": "PSW/MSM8940/16061",
                                  "签名种类": "V3_double"},
                                 {"签名包": "media_old", "签名类型": "media", "签名项目": "PSW/MSM8916_5.1/15036",
                                  "签名种类": "V2_single"}, ]
        # 设置 Chrome 选项
        options = Options()
        # options.add_argument('--headless')  # 启用无头模式
        options.add_argument("--window-size=1920,1080")  # 设置窗口大小为 1920x1080
        options.add_argument("--disable-gpu")  # 禁用GPU硬件加速
        options.add_argument("--disable-software-rasterizer")  # 禁用软件光栅化
        options.add_argument("--remote-allow-origins=*")  # 允许远程访问
        # 设置用户代理，模拟普通浏览器访问
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')

        # 初始化 WebDriver
        self.d = webdriver.Chrome(options=options)
        self.d.get(self.url)
        self.wait = WebDriverWait(self.d, 30, 2)  # 等待元素加载完成，最多240秒

    @staticmethod
    def walk_directory(path):
        # 使用 rglob 获取所有文件，然后筛选出文件
        files = [file for file in path.rglob('*.apk') if file.is_file()]
        # 返回文件的绝对路径
        return [str(file) for file in files]

    @staticmethod
    def mark_signed_apk(apk_path):
        # 获取文件的目录和文件名
        directory, filename = os.path.split(apk_path)
        # 分割文件名和扩展名
        name, extension = os.path.splitext(filename)
        # 创建新的文件名，添加前缀
        new_filename = f"signed_{name}{extension}"
        # 构建新的文件路径
        new_apk_path = os.path.join(directory, new_filename)
        # 重命名文件
        os.rename(apk_path, new_apk_path)
        return new_apk_path

    @staticmethod
    def save_and_open_html(download_links):
        # 初始化HTML内容，包括HTML和body标签
        html_content = "<html><body>"
        # 对于每个链接，创建一个包含签名信息和下载链接的HTML段落，使用格式化字符串插入文件名、签名包名称和下载链接
        for filename, link, disposition in download_links:
            html_content += f"<p><b>已签名-{filename}-{disposition['签名包']}</b><br><a href='{link}'>{link}</a></p>"
        # 添加结束body和html标签
        html_content += "</body></html>"
        # 将HTML内容写入文件
        with open("signature_results.html", "w", encoding="utf-8") as file:
            file.write(html_content)
        # 打开HTML文件：使用webbrowser模块打开生成的HTML文件，os.path.realpath获取文件的绝对路径
        webbrowser.open("file://" + os.path.realpath("signature_results.html"))

    def requests(self):
        for filename, disposition, link in self.download_links:
            # 构建消息内容
            message = {
                "msg_type": "post",
                "content": {
                    "post": {
                        "zh_cn": {
                            "title": "签名完成通知!",
                            "content": [
                                [{
                                    "tag": "text",
                                    "text": f"签名包 - {filename}\n"
                                }, {
                                    "tag": "a",
                                    "text": "点击下载",
                                    "href": f"{link}"
                                }, {
                                    "tag": "at",
                                    "user_id": "all"
                                }]
                            ]
                        }
                    }
                }
            }
            # 发送POST请求给飞书机器人
            headers = {"Content-Type": "application/json"}
            try:
                response = requests.post(url=self.webhook_url, headers=headers, json=message)
                response.raise_for_status()  # 如果请求返回错误状态码，抛出异常
                print("发送成功！")
            except requests.exceptions.RequestException as e:
                print(f"发送失败：{e}")

    def login(self):
        # 登录
        pyautogui.hotkey("F11")  # 浏览器全屏
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='username']"))).send_keys(self.accounts["username"])
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='password']"))).send_keys(self.accounts["password"])
        self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                    "//body/div[1]/div[3]/div[3]/div[1]/div[4]/div[1]/form[1]/button[1]"))).click()

    def signature(self):
        download_links = []

        if len(self.path_list) == 0:
            return print('没有可签名的文件！')

        # 遍历apk路径列表
        for apk in self.path_list:
            directory, filename = os.path.split(apk)
            classify_list = []
            temporary_list = []
            # 判断是否以指定字符开头
            if filename.startswith('Music_40'):
                classify_list.append(self.disposition_list[0])
            elif filename.startswith('Music_50'):
                temporary_list.extend(self.disposition_list[1:])
                classify_list = temporary_list
            else:
                self.d.quit()
                return print('没有可签名的文件！')

            self.login()  # 登录
            time.sleep(1)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'签名服务')]"))).click()  # 切换到签名服务栏

            # 签名
            num = 1
            for disposition in classify_list:
                # 签名类型
                types = self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                            "//body/div[@id='udp-app']/div[1]/section[1]/section[1]/main[1]/div[1]/div[1]/section[1]/div[1]/div[1]/section[1]/main[1]/div[2]/form[1]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]")))
                types.send_keys(disposition['签名类型'])
                time.sleep(1)
                self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[text() = '{disposition['签名类型']}']"))).click()
                time.sleep(1)

                # 签名项目
                project = self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                      "//body/div[@id='udp-app']/div[1]/section[1]/section[1]/main[1]/div[1]/div[1]/section[1]/div[1]/div[1]/section[1]/main[1]/div[2]/form[1]/div[3]/div[1]/div[1]/div[1]/input[1]")))
                project.send_keys(disposition['签名项目'].split('/')[2])
                time.sleep(1)
                self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[(text()='{disposition['签名项目']}')]"))).click()
                time.sleep(1)

                # 签名种类
                kinds = self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                    "//body/div[@id='udp-app']/div[1]/section[1]/section[1]/main[1]/div[1]/div[1]/section[1]/div[1]/div[1]/section[1]/main[1]/div[2]/form[1]/div[5]/div[1]/div[1]/div[1]/input[1]")))
                kinds.send_keys(disposition['签名种类'])
                time.sleep(1)
                self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(),'{disposition['签名种类']}')]"))).click()
                time.sleep(1)

                # Music_50开头apk签名，只上传一次签名文件
                if filename.startswith('Music_50') and num != 1:
                    pass
                else:
                    # 上传签名文件
                    self.wait.until(EC.element_to_be_clickable((By.XPATH, "//em[contains(text(),'点击上传')]"))).click()
                    time.sleep(3)

                    pyperclip.copy(apk)
                    pyautogui.hotkey("ctrl", "v")
                    pyautogui.press("enter", presses=1)  # 输入两次enter键，防止出错

                    # 等待上传时间元素加载，判断是否上传完成
                    self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'上传时间')]")))
                    time.sleep(1)

                # 签名
                self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                            "//body[1]/div[1]/div[1]/section[1]/section[1]/main[1]/div[1]/div[1]/section[1]/div[1]/div[1]/section[1]/main[1]/div[2]/form[1]/div[8]/div[1]/button[1]/span[1]"))).click()
                time.sleep(1)
                while True:
                    if self.href is None:
                        break
                    elif self.href != self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "personListlink"))).get_attribute('href'):
                        break
                    else:
                        continue
                # 等待签名文件元素加载，判断是否签名完成
                self.wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'签名文件：')]")))
                time.sleep(1)
                # 签名完成后获取下载链接
                download_href = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "personListlink"))).get_attribute('href')
                self.href = download_href
                self.download_links.append((filename, f"{disposition['签名包']}", download_href))
                print(f"{filename} - {disposition['签名包']} 签名完成\n下载链接：【{download_href}】")
                download_links.append((filename, download_href, disposition))

                num += 1
                time.sleep(3)

            pyautogui.hotkey("ctrl", "R")  # 刷新
            self.mark_signed_apk(apk)  # 修改apk文件名前缀，标记为已签名
        # self.save_and_open_html(download_links)  # 将签名完成后的href加入.html文件中并在浏览器打开
        self.requests()  # 发送下载地址给飞书机器人
        self.d.quit()


if __name__ == "__main__":
    run = SignatureService()
    run.signature()