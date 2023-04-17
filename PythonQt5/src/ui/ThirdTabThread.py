import os
from ctypes import Union

from PyQt5.QtCore import QThread, pyqtSignal

from src.config import CURRENT_PATH, IMAGE_PATH


class ThirdTabThread(QThread):
    run_signal = pyqtSignal(int)
    msg_signal = pyqtSignal(str, str, str)

    def __init__(self, path: str, edit_msg: list):
        super(ThirdTabThread, self).__init__()
        self.path = path
        self.out_dir = os.path.join(CURRENT_PATH, 'out')  # 文件路径输出
        self.out_file_dir = os.path.join(self.out_dir, 'frame_id.txt')
        self.icon_path = os.path.join(IMAGE_PATH, 'icon/1.ico')

    def run(self) -> None:
        try:
            all_paths: list = []
            if os.path.isdir(self.path):
                for each in os.listdir(self.path):
                    path = os.path.join(self.path, each)
                    if os.path.isfile(path):
                        all_paths.append(path)
            elif os.path.isfile(self.path):
                all_paths.append(self.path)
            else:
                self.msg_signal.emit('错误', '文件路径非文件或文件夹！', self.icon_path)
                return None
            if len(all_paths) < 1:
                self.msg_signal.emit('错误', '未获取到文件夹中协议或xml文件！', self.icon_path)
                return None
            psg_count = 0
            copy_num = len(all_paths)
            count = 100 / copy_num
            self.run_signal.emit(0)
            for cur_path in all_paths:
                psg_count += count
                self.run_signal.emit(psg_count)
            self.run_signal.emit(100)
        except Exception:
            self.msg_signal.emit('错误', '程序运行错误！', self.icon_path)
