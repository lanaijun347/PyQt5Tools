import os
import re
import shutil
from ctypes import Union
from typing import Dict

import chardet
from PyQt5.QtCore import QThread, pyqtSignal
from lxml import etree

from src.basic import cmd_insert_space
from src.config import CURRENT_PATH, IMAGE_PATH


class ThirdTabThread(QThread):
    run_signal = pyqtSignal(int)
    msg_signal = pyqtSignal(str, str, str)

    def __init__(self, path: str, edit_msg: list, file_type: int):
        super(ThirdTabThread, self).__init__()
        self.edit_msg = edit_msg
        self.path = path
        self.file_type = file_type
        self.out_dir = os.path.join(CURRENT_PATH, 'out')  # 文件路径输出
        self.out_file = os.path.join(self.out_dir, 'frame_id.txt')
        self.icon_path = os.path.join(IMAGE_PATH, 'icon/1.ico')

    def run(self) -> None:
        try:
            out_str: str = ''
            all_paths: list = []
            out_dict: Dict[str, str] = {}
            if os.path.isfile(self.path):
                if self.file_type == 0:
                    if ".ASM" in self.path.upper() or ".TXT" in self.path.upper():
                        all_paths.append(self.path)
                else:
                    if 'VCICFG.XML' == self.path.upper():
                        all_paths.append(self.path)
            if os.path.isdir(self.path):
                for file_path, dir_names, file_names in os.walk(self.path):
                    for file_name in file_names:
                        path = os.path.join(file_path, file_name)
                        if self.file_type == 0:
                            if ".ASM" in file_name.upper() or ".TXT" in file_name.upper():
                                all_paths.append(path)
                        else:
                            if 'VCICFG.XML' == file_name.upper():
                                all_paths.append(path)
            if len(all_paths) < 1:
                self.msg_signal.emit('错误', '未获取asm/txt/xml格式文件！', self.icon_path)
                return None
            psg_count = 0
            copy_num = len(all_paths)
            count = 100 / copy_num
            self.run_signal.emit(0)
            for cur_path in all_paths:
                try:
                    if os.path.split(cur_path)[-1].split('.')[-1].upper() == "XML":
                        protocol_frame, protocol_filter = self.get_xml_id(cur_path)
                    else:
                        protocol_frame, protocol_filter = self.get_protocol_id(cur_path)
                    if not protocol_frame:
                        continue
                    if protocol_frame not in out_dict.keys():
                        out_dict[protocol_frame] = protocol_filter
                except Exception:
                    self.edit_msg.append(f"文件解析错误: {cur_path}")
                    continue
                psg_count += count
                self.run_signal.emit(psg_count)
            n = 0
            for key, value in out_dict.items():
                protocol_frame = key.rjust(8, '0')
                protocol_filter = value.rjust(8, '0')
                protocol_frame = cmd_insert_space(protocol_frame)
                protocol_filter = cmd_insert_space(protocol_filter)
                out_str = out_str + "05        " + protocol_frame + "   " + protocol_filter + "   00 ;" + hex(
                    n).replace('0x', '').rjust(3, '0') + '\n'
                n += 1
            self.init_out_dir()
            with open(self.out_file, 'w', encoding='utf-8') as f:
                f.write(out_str)
            self.edit_msg.append(f'\n输出路径: {self.out_file}')
            if len(self.edit_msg) > 1:
                self.edit_msg.append("程序运行结束！")
            else:
                self.edit_msg.append("程序运行结束,无错误信息！")
            self.run_signal.emit(100)
            self.msg_signal.emit('信息', '程序运行结束！', self.icon_path)
        except Exception:
            self.msg_signal.emit('错误', '程序运行错误！', self.icon_path)
            return None

    def get_protocol_id(self, path) -> tuple:
        result = ("", "")
        with open(path, 'rb') as f:
            file_encoding = chardet.detect(f.read())["encoding"]
        with open(path, 'r', encoding=file_encoding) as f:
            try:
                protocol_type: tuple = re.findall(r'\$~([0-9]{2}|[0-9]{1})\$~([0-9]{2}|[0-9]{1})(.*)', f.read())[0]
                if protocol_type[0].strip() == protocol_type[1].strip():
                    self.edit_msg.append(f"非CAN线路径： {path}")
                    return result
                protocol_filter = protocol_type[2].split('$~')[-1].split(",")[0].split("~")[0].strip().upper().replace(
                    '0X', '')
                f.seek(0)
                for line in f.readlines():
                    if "REQ" in line:
                        protocol_frame = line.split(':')[-1].split(' ')[0].strip().upper().replace('0X', '')
                        break
                if len(protocol_frame) < 1:
                    self.edit_msg.append(f'通讯线获取解析错误: {path}')
                    return result
                else:
                    return protocol_frame, protocol_filter
            except IndexError:
                self.edit_msg.append(f'通讯线获取解析错误: {path}')
                return result

    def get_xml_id(self, path) -> tuple:
        try:
            xml = etree.parse(path)
            receive_pin = xml.xpath("//receive_pin/text()")[0]
            send_pin = xml.xpath("//send_pin/text()")[0]
            if receive_pin == send_pin:
                self.edit_msg.append(f'非CAN线路径: {path}')
                return '', ''
            filter_str = xml.xpath("//CAN_filter_id/text()")[0]
            cmd_list = xml.xpath("//command/text()")[0]
        except Exception:
            self.edit_msg.append(f'xml解析错误: {path}')
            return '', ''
        filter_value = int(filter_str.split(",")[-1].strip().upper().replace('0X', ''), 16)
        frame_list = cmd_list.split(',')
        if filter_value > 0xffff:
            byte_num = 4
        else:
            byte_num = 2
        filter_id = hex(filter_value).replace('0x', '').upper().rjust(8, '0')
        frame_id = (''.join(frame_list[0:byte_num])).upper().replace('0X', '').rjust(8, '0')
        return frame_id, filter_id

    def init_out_dir(self):
        if os.path.exists(self.out_dir):
            shutil.rmtree(self.out_dir)
        os.mkdir(self.out_dir)


if __name__ == '__main__':
    pass
