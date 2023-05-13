import os

from PyQt5.QtWidgets import QPushButton
from lxml import etree

from PyQt5.QtCore import QThread, pyqtSignal

from src.basic import is_contains_chinese
from src.config import IMAGE_PATH


class FourthTabThread(QThread):
    run_signal = pyqtSignal(int)
    msg_signal = pyqtSignal(str, str, str)

    def __init__(self, path: str, edit_msg: list, run_btn: QPushButton):
        super(FourthTabThread, self).__init__()
        self.path = path
        self.edit_msg = edit_msg
        self.run_btn = run_btn
        self.icon_path = os.path.join(IMAGE_PATH, 'icon/1.ico')

    def run(self) -> None:
        try:
            all_paths: list = []
            if os.path.isfile(self.path):
                if '.XML' in self.path.upper():
                    all_paths.append(self.path)
            elif os.path.isdir(self.path):
                for root, dirs, files in os.walk(self.path):
                    for file in files:
                        if '.XML' in file.upper():
                            tmp_path = os.path.join(root, file)
                            all_paths.append(tmp_path)
            if len(all_paths) < 1:
                self.msg_signal.emit('错误', '未获取到xml格式文件！', self.icon_path)
                return None
            psg_count = 0
            copy_num = len(all_paths)
            count = 100 / copy_num
            self.run_signal.emit(0)
            for path in all_paths:
                try:
                    xml = etree.parse(path)
                except FileExistsError:
                    self.edit_msg.append(f'xml解析错误: {path}')
                    self.run_signal.emit(psg_count)
                    continue
                formula_list = xml.xpath('//formula//text()')
                for each in formula_list:
                    result = is_contains_chinese(each)
                    if result:
                        self.edit_msg.append(f'{each} -> {path}')
                        self.run_signal.emit(psg_count)
                psg_count += count
                self.run_signal.emit(psg_count)
            if len(self.edit_msg) > 0:
                self.edit_msg.append("程序运行结束！")
            else:
                self.edit_msg.append("程序运行结束,无错误信息！")
            self.run_signal.emit(100)
            self.msg_signal.emit('信息', '程序运行结束！', self.icon_path)
        except Exception:
            self.msg_signal.emit('错误', '程序运行错误！', self.icon_path)
        finally:
            self.run_btn.setEnabled(True)
        return None
