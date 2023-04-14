import os
import shutil
from typing import Union
from lxml import etree


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
    with open(path, 'r') as f:
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
            tmp = path.split('/')[-1]
        elif '\\' in path:
            tmp = path.split('\\')[-1]
        else:
            tmp = path
        out_list.append(tmp)
    return out_list


if __name__ == '__main__':
    # p = r'F:\PythonTools\JBT项目\EV_FLYER\V19.20解析\menu\menu_新能源.xml'
    # tmp = get_menu_xml_path_attribute_last_layer(p)
    tmp = get_menu_xml_path_attribute_last_layer(r'F:\PythonTools\menu.xml')
    print(tmp)
