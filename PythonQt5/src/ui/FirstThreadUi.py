import os
import re
import shutil
import time
from typing import Union

import chardet
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QPushButton

from src.config import *
import src.basic as bs


class FirstThreadUi(QThread):
    write = pyqtSignal(int)
    end = pyqtSignal(str)

    def __init__(self, path: Union[bytes, str], data: dict, info_msgs: list, run_btn: QPushButton):
        super(FirstThreadUi, self).__init__()
        self.path = path
        self.data = data
        self.info_msgs = info_msgs
        self.run_btn = run_btn
        self.in_value = data['in_value']
        self.idle_value = data['idle_value']
        self.quit_value = data['quit_value']
        self.read_value = data['read_value']
        self.clear_value = data['clear_value']
        self.info_value = data['info_value']
        self.ds_value = data['ds_value']
        self.act_value = data['act_value']
        self.spe_value = data['spe_value']
        self.out_dir = os.path.join(CURRENT_PATH, 'out')  # 文件路径输出
        self.out_file_dir = os.path.join(self.out_dir, '协议命令')
        self.error_path = os.path.join(CURRENT_PATH, 'out\\error.txt')  # 错误信息文件

    def run(self):
        try:
            # 判断获取路径
            path_list = []
            if os.path.exists(self.path):
                if os.path.isfile(self.path):
                    path_list.append(self.path)
                elif os.path.isdir(self.path):
                    for file_path, dir_names, file_names in os.walk(self.path):
                        for file_name in file_names:
                            path = os.path.join(file_path, file_name)
                            path_list.append(path)
                else:
                    self.end.emit('非法路径！')
                    return None
            else:
                self.end.emit('路径输入错误！')  # 触发信号
                return None
            # 文件处理
            self.init_out_dir()  # 初始输出路径
            list_len = len(path_list)
            tmp = 100 / list_len
            count = 0
            for path in path_list:
                count += tmp
                self.info_msgs.append(path)
                self.file_handle(path)
                self.write.emit(count)  # 触发信号
            self.write.emit(100)
            self.end.emit('运行结束！')
        except Exception:
            self.end.emit('运行出错！')
        finally:
            self.run_btn.setEnabled(True)
        return None

    def init_out_dir(self):
        if not os.path.exists(self.out_dir):
            os.mkdir(self.out_dir)
        if not os.path.exists(self.out_file_dir):
            os.mkdir(self.out_file_dir)
        else:
            shutil.rmtree(self.out_file_dir)
            os.mkdir(self.out_file_dir)
        if os.path.exists(self.error_path):
            os.remove(self.error_path)

    def file_handle(self, path):
        # with open(path, 'rb') as f:
        #     file_encoding = chardet.detect(f.read())["encoding"]
        get_protocol_flag = True
        protocolType = -1
        ans = -1
        fiterId = ''
        clearDtcCmdList = []
        readDtcCmdlist = []
        ecuCmdList = []
        dsCmdList = []
        actCmdList = []
        speCmdList = []
        inCmdList = []
        idleCmdList = []
        quitCmdList = []
        bps_list = ['500000', '250000', '125000', '500K', '250K', '125K', '10400', '9600']
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            try:
                for line in f.readlines():
                    line = line.replace("：", ":")
                    if "$~" in line and get_protocol_flag:
                        if ans == -1:
                            protocolType = self.get_protocol_type(line)
                        else:
                            protocolType = 0
                        if protocolType == 0:  # CAN
                            fiterId = (line.split("$~")[-1]).replace('\n', '')
                            if fiterId.upper() in bps_list:
                                ans = 0
                            else:
                                if ans == -1:
                                    get_protocol_flag = False
                            if 'ANS' in line and ans == 0:
                                fiterId = line.split(':')[-1].split(' ')[0]
                                ans = -1
                                get_protocol_flag = False
                        elif protocolType == 1:  # Kwp2000
                            fiterId = ''
                            get_protocol_flag = False
                        else:
                            self.info_msgs.append("未能识别通讯类型")
                            bs.write_debug(self.error_path, f"未能识别通讯类型：{path}")
                            break
                    if "REQ" in line and "$" in line and ":" in line:
                        if "$$" in line:
                            betweenStrRe = re.compile(r'[R](.*?)[$]', re.S)
                            betweenStr = re.findall(betweenStrRe, line)[0]
                        else:
                            betweenStrRe = re.compile(r'[$](.*?)[$]', re.S)
                            betweenStr = re.findall(betweenStrRe, line)[0]
                        cmdStr = (betweenStr.split(':')[1]).replace('XX', "00").strip()
                        if protocolType == 0:
                            cmdStr = self.can_cmd(cmdStr, fiterId)
                        elif protocolType == 1:
                            cmdStr = self.kwp200_cmd(cmdStr)
                        else:
                            self.info_msgs.append("未能识别命令")
                            bs.write_debug(self.error_path, f"未能识别命令：{line}")
                            break
                        if "$~" in line:
                            if self.in_value == 0:
                                self.in_value = ''
                            inCmdList.append(f'{cmdStr};{self.in_value}\n')
                        elif "$!" in line:
                            if self.idle_value == 0:
                                self.idle_value = ''
                            idleCmdList.append(f'{cmdStr};{self.idle_value}\n')
                        elif "$@" in line:
                            if self.quit_value == 0:
                                self.quit_value = ''
                            quitCmdList.append(f'{cmdStr};{self.quit_value}\n')
                        elif "$#" in line:
                            if self.read_value == 0:
                                self.read_value = ''
                            readDtcCmdlist.append(f'{cmdStr};{self.read_value}\n')
                        elif "$$" in line:
                            if self.clear_value == 0:
                                self.clear_value = ''
                            clearDtcCmdList.append(f'{cmdStr};{self.clear_value}\n')
                        elif "$%" in line:
                            if self.info_value == 0:
                                self.info_value = ''
                            ecuCmdList.append(f'{cmdStr};{self.info_value}ecu\n')
                        elif "$^" in line:
                            if self.act_value == 0:
                                self.act_value = ''
                            actCmdList.append(f'{cmdStr};{self.act_value}\n')
                        elif "$&" in line:
                            if self.spe_value == 0:
                                self.spe_value = ''
                            speCmdList.append(f'{cmdStr};{self.spe_value}\n')
                        elif "$FC" in line:
                            continue
                        else:
                            if self.ds_value == 0:
                                self.ds_value = ''
                            dsCmdList.append(f'{cmdStr};{self.ds_value}ds\n')
            except:
                self.info_msgs.append("无法获取协议类型")
                bs.write_debug(self.error_path, f"无法获取协议类型：{path}")
        inCmdList.extend(idleCmdList)
        inCmdList.extend(quitCmdList)
        inCmdList.extend(readDtcCmdlist)
        inCmdList.extend(clearDtcCmdList)
        inCmdList.extend(ecuCmdList)
        inCmdList.extend(dsCmdList)
        inCmdList.extend(actCmdList)
        inCmdList.extend(speCmdList)
        if len(inCmdList) < 1:
            self.info_msgs.append("无法获取协议类型")
            bs.write_debug(self.error_path, f"无法获取协议类型：{path}")
            return None
        # name = os.path.split(path)[-1]
        if os.path.isdir(self.path):
            name = path.replace(self.path, '')
            tmp_list = name.split('\\')
            tmp_path = self.out_file_dir
            for each in tmp_list[0: -1]:
                tmp_path = os.path.join(tmp_path, each)
                if not os.path.exists(tmp_path):
                    os.mkdir(tmp_path)
            out_path = os.path.join(tmp_path, tmp_list[-1])
        else:
            name = os.path.split(path)[-1]
            out_path = os.path.join(self.out_file_dir, name)
        with open(out_path, 'w', encoding='utf-8', errors='ignore') as f1:
            for line in inCmdList:
                f1.writelines(line)
        return None

    def get_protocol_type(self, line):
        result = -1
        count = line.count("$~")
        if count > 2:
            tmpList = line.split("$~")
            if tmpList[1] == tmpList[2]:
                result = 1  # KWP2000
            else:
                result = 0  # CAN
        return result

    def can_cmd(self, cmdStr, fiterId):
        data = cmdStr.split(" ")
        keyByte = hex(int(data[2], 16) + 0x40).replace('0x', '')
        data[0] = fiterId
        data[2] = keyByte
        receiveCmdStr = ''
        for tmp in data:
            receiveCmdStr = receiveCmdStr + tmp + ' '
        return f"{cmdStr.ljust(30, ' ')}{' ' * 20}{receiveCmdStr.ljust(30, ' ')}"

    def kwp200_cmd(self, cmdStr):
        cmdStr = cmdStr.strip()
        tmpList = cmdStr.split(" ")
        tmp = tmpList[1]
        tmpList[1] = tmpList[2]
        tmpList[2] = tmp
        receiveCmdStr = ''
        if int(tmpList[0], 16) & 0x0F:
            keyBytes = hex(int(tmpList[3], 16) + 0x40).replace('0x', '').upper()
            tmpList[3] = keyBytes
        else:
            keyBytes = hex(int(tmpList[4], 16) + 0x40).replace('0x', '').upper()
            tmpList[4] = keyBytes
        for i in tmpList:
            receiveCmdStr = receiveCmdStr + i + " "
        receiveCmdStr = receiveCmdStr.strip()
        return f"{cmdStr.ljust(30, ' ')}{' ' * 20}{receiveCmdStr.ljust(30, ' ')}"
