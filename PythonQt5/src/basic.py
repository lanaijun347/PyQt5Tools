import os
import shutil
from typing import Union

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QFileDialog, QLineEdit, QTextEdit, QMessageBox
from lxml import etree

from src.config import CURRENT_PATH, IMAGE_PATH


def delete_and_create_folder(path: Union[bytes, str]):
    """
    判断文件夹是否存在，存在则删除重新创建
    :param path: 路径
    :return: None
    """
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def write_debug(path, debug_str):
    """
    log写入
    :param path: 路径
    :param debug_str: 写入内容
    :return: None
    """
    with open(path, 'a') as f:
        f.writelines(debug_str + '\n')


def get_protocol_menu_id(path) -> list:
    """
    获取协议菜单id
    :param path: 协议菜单路径
    :return: id列表
    """
    id_list = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f.readlines():
            if '\\' in line:
                name = line.split('\\')[-2]
            elif '/' in line:
                name = line.split('/')[-2]
            else:
                name = line.replace('\n', '')
            id_list.append(name.strip())
    return id_list


def get_menu_xml_path_attribute(path) -> list:
    """
    获取xml菜单 path 属性值
    :param path: xml菜单路径
    :return: 属性值列表
    """
    tree = etree.parse(path)
    out_list = tree.xpath('//menu/@path')
    return out_list


def get_menu_xml_path_attribute_last_layer(path) -> list:
    """
    获取xml菜单的 path 属性的最后一层
    :param path: xml菜单路径
    :return:
    """
    out_list = []
    attribute_list = get_menu_xml_path_attribute(path)
    for path in attribute_list:
        if '/' in path:
            tmp_str = path.split('/')[-1]
        elif '\\' in path:
            tmp_str = path.split('\\')[-1]
        else:
            tmp_str = path
        out_list.append(tmp_str)
    return out_list


def open_folder_path(edit: Union[QLineEdit, QTextEdit]):
    """
    打开获取文件夹窗口，把选择的文件夹路径写入 QLineEdit
    :param edit: QLineEdit
    :return:
    """
    directory = QFileDialog.getExistingDirectory(None, "选取文件夹", CURRENT_PATH)
    edit.setText(directory)


def open_file_path(edit: Union[QLineEdit, QTextEdit]):
    """
    打开获取文件窗口，把选择的文件路径写入 QLineEdit
    :param edit:
    :return:
    """
    directory = QFileDialog.getOpenFileName(None, "选取文件", CURRENT_PATH, "All Files (*);;Text Files (*.txt)")
    edit.setText(directory[0])


def clear_edit(edit: Union[QLineEdit, QTextEdit]):
    """
    清空输入框
    :param edit:
    :return:
    """
    edit.setText('')


def message_box(title: str, msg: str, ico_path=''):
    """
    信息弹框
    :param title: 标题
    :param msg: 显示信息
    :param ico_path: 图标路径
    :return:
    """
    msg_box = QMessageBox(QMessageBox.Information, title, msg)
    msg_box.setWindowIcon(QIcon(ico_path))
    msg_box.exec_()


def cmd_insert_space(n: str):
    """
    给命令插入空格
    :param n: 命令字符串
    :return: 插入空格后结果
    """
    out = ''
    count = 1
    for i in n:
        if count % 2 == 0:
            out = out + i + ' '
        else:
            out += i
        count += 1
    return out


def is_contains_chinese(str_1) -> bool:
    """
    判断字符串中是否含有中文
    :param str_1:
    :return:
    """
    for _char in str_1:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False


if __name__ == '__main__':
    # p = r'F:\PythonTools\JBT项目\EV_FLYER\V19.20解析\menu\menu_新能源.xml'
    # tmp = get_menu_xml_path_attribute_last_layer(p)
    tmp = get_menu_xml_path_attribute_last_layer(r'F:\PythonTools\menu.xml')
    print(tmp)
