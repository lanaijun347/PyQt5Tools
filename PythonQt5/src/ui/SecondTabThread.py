import os
import shutil
from typing import Union

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QPushButton

from src.ui.MyEnum import MyEnum


class SecondTabThread(QThread):
    run_signal = pyqtSignal(int)
    msg_signal = pyqtSignal(str, str)

    def __init__(self, copy_type: int, from_path: list, copy_file: list, copy_path: Union[bytes, str], edit_msg: list,
                 run_btn: QPushButton):
        super(SecondTabThread, self).__init__()
        self.copy_type = copy_type
        self.from_path = from_path
        self.copy_file = copy_file
        self.copy_path = copy_path
        self.edit_msg = edit_msg
        self.run_btn = run_btn

    def run(self) -> None:
        try:
            pgb_value = 0
            self.run_signal.emit(pgb_value)
            copy_num = len(self.copy_file)
            count = 100 / copy_num
            if self.copy_type == MyEnum.File_type.value:
                self.file_type_copy(pgb_value, count)
            elif self.copy_type == MyEnum.Dir_type.value:
                self.folder_type_copy(pgb_value, count)
            else:
                self.msg_signal.emit('错误', "未知拷贝类型。")
                return None
            self.run_signal.emit(100)
            self.msg_signal.emit("Tip", "执行成功")
        except Exception:
            self.msg_signal.emit("错误", "拷贝出错")
        finally:
            self.run_btn.setEnabled(True)
        return None

    def file_type_copy(self, pgb_value, count):
        file_format = ''
        file_name = ''
        tmp_list = list(set(self.copy_file))
        root_list = self.from_path[0].strip().split('\\')
        if not root_list[-1]:
            del root_list[-1]
        del root_list[-1]
        for file in tmp_list:
            flag = False
            file_format = self.from_path[0].split('.')[-1]
            current_file = file + '.' + file_format
            tmp_path = os.path.join('\\'.join(root_list), current_file)
            if os.path.exists(tmp_path):
                copy_path = os.path.join(self.copy_path, current_file)
                shutil.copyfile(tmp_path, copy_path)
                flag = True
            if not flag:
                self.edit_msg.append(f'警告：源路径未找到名为 {file} 的文件。')
                self.run_signal.emit(pgb_value)
            else:
                # self.edit_msg.append(f"{file_name}.{file_format} 拷贝成功。")
                self.run_signal.emit(pgb_value)
            pgb_value += count
            self.run_signal.emit(pgb_value)

    def folder_type_copy(self, pgb_value, count):
        folder_name = ''
        tmp_list = list(set(self.copy_file))
        for file in tmp_list:
            flag = False
            for path in self.from_path:
                folder_name = os.path.split(path)[-1]
                if file.upper() == folder_name.upper():
                    copy_path = os.path.join(self.copy_path, folder_name)
                    shutil.copytree(path, copy_path)
                    flag = True
                    break
            if not flag:
                self.edit_msg.append(f'警告：源路径未找到名为 {file} 的文件夹。')
                self.run_signal.emit(pgb_value)
            else:
                # self.edit_msg.append(f"{folder_name} 拷贝成功。")
                self.run_signal.emit(pgb_value)
            pgb_value += count
            self.run_signal.emit(pgb_value)
