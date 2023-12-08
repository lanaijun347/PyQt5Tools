import os
import re
import subprocess
import sys

import requests
from requests.exceptions import Timeout, RequestException
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget


class UpdateUi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('检查更新')
        self.resize(400, 600)
        self.layout = QVBoxLayout()
        self.edit = QTextEdit()
        self.edit_list = []
        self.edit.setText("")
        self.edit.setReadOnly(True)  # 设置为只读
        self.layout.addWidget(self.edit)
        self.setLayout(self.layout)
        self.download_thread = None

    def refresh_edit(self, msg):
        self.edit_list.append(msg)
        self.edit.setText('\n'.join(self.edit_list))
        # 更新内容,如果不更新可能没有显示新内容
        self.edit.repaint()

    def psg_edit(self, msg):
        self.edit_list[-1] = msg
        self.edit.setText('\n'.join(self.edit_list))
        # 更新内容,如果不更新可能没有显示新内容
        self.edit.repaint()

    def download_success(self, open_path):
        self.refresh_edit("正在重启App，请稍候！")
        subprocess.Popen(f"python {os.path.join(open_path, 'update.py')}", shell=True)
        self.close()

    def star_update(self, url, app_name, web_version, download_path, old_app_path):
        self.download_thread = DownloadThread(url, app_name, web_version, download_path, old_app_path)
        self.download_thread.msg_signal.connect(self.refresh_edit)
        self.download_thread.success_signal.connect(self.download_success)
        self.download_thread.psg_signal.connect(self.psg_edit)
        self.download_thread.start()


class DownloadThread(QThread):
    msg_signal = pyqtSignal(str)
    psg_signal = pyqtSignal(str)
    success_signal = pyqtSignal(str)

    def __init__(self, url, app_name, web_version, download_path, old_app_path):
        super().__init__()
        self.url = url
        self.app_name = app_name
        self.web_version = web_version
        self.download_path = download_path
        self.old_app_path = old_app_path

    def run(self) -> None:
        download_name = self.app_name + "-" + str(self.web_version) + '.exe'
        try:
            response_app = requests.get(self.url + download_name, stream=True, timeout=5)
            try:
                response_app.raise_for_status()  # 如果返回状态码不是200，则抛出异常
            except requests.exceptions.HTTPError as e:
                self.msg_signal.emit(f"App下载请求 {e.response.status_code}")
                return None
        except Timeout:
            self.msg_signal.emit("App下载请求超时")
            return None
        except RequestException as e:
            self.msg_signal.emit(f"App下载请求发生错误 {e}")
            return None
        download_app_path = os.path.join(self.download_path, download_name)
        self.msg_signal.emit(f"App保存路径: {download_app_path}")
        self.msg_signal.emit(f"开始下载最新App...")
        total_length = int(response_app.headers.get('content-length'))
        dl = 0
        with open(download_app_path, 'wb') as f:
            self.msg_signal.emit(f"App下载进度: 0%")
            for chunk in response_app.iter_content(chunk_size=8192):
                if chunk:
                    dl += len(chunk)
                    f.write(chunk)
                    f.flush()
                    progress = int((dl / total_length) * 100)
                    self.psg_signal.emit(f"App下载进度: {str(progress)}%")
        self.msg_signal.emit(f"App下载完成！")
        self.msg_signal.emit(f"开始获取更新！")
        update_py_path = self.url + "update.txt"
        try:
            response_py = requests.get(update_py_path, timeout=5)
            try:
                response_py.raise_for_status()  # 如果返回状态码不是200，则抛出异常
            except requests.exceptions.HTTPError as e:
                self.msg_signal.emit(f"更新脚本请求 {e.response.status_code}")
                return None
        except Timeout:
            self.msg_signal.emit("更新脚本获取超时")
            return None
        except Exception as e:
            self.msg_signal.emit(f"获取更新脚本请求发生错误 {e}")
            return None
        self.msg_signal.emit(f"更新脚本下载进度: 0%")
        with open(os.path.join(self.download_path, 'update.py'), 'wb') as f:
            for chunk in response_py.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        self.psg_signal.emit(f"更新脚本下载进度: 50%")
        with open(os.path.join(self.download_path, 'update.py'), 'r', encoding="utf-8") as f:
            file_str = f.read()
            replace_str = re.findall("DATA.*=.*{.*}", file_str)[0]
            data = {"url": self.url, "app_name": self.app_name, "download_path": self.download_path,
                    "old_app_path": self.old_app_path, "new_app_path": download_app_path, "pid": os.getpid()}
            new_str = file_str.replace(replace_str, f"DATA = {data}")
        self.psg_signal.emit(f"更新脚本下载进度: 75%")
        with open(os.path.join(self.download_path, 'update.py'), 'w', encoding="utf-8") as f:
            f.write(new_str)
        self.psg_signal.emit(f"更新脚本下载进度: 100%")
        self.success_signal.emit(self.download_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = UpdateUi()
    mainWindow.show()
    mainWindow.star_update('http://192.168.2.234/', "诊断开发常用工具", 202312081447, r"D:\JBT\常用工具\协议命令获取工具",
                           r"D:\JBT\常用工具\协议命令获取工具\诊断开发常用工具-202312081446 - 副本.exe")
    sys.exit(app.exec_())
