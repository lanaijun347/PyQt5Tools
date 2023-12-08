import json
import os
import re
from datetime import datetime
import shutil


def change_spec_file(path, app_name):
    """
        修改 .spec 文件的 "name" 参数，修改版本号
        :param path: .spec 文件
        :return: 返回旧名称
    """
    with open(path, 'r', encoding='utf-8') as f:
        file_str = f.read()
        name = re.findall(r"name='(.*)'", file_str)[0]
        new_str = file_str.replace(name, app_name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_str)


def change_config_file(path, version):
    with open(path, 'r', encoding='utf-8') as f:
        file_str = f.read()
        current_version = re.findall(r"VERSION = (.*)", file_str)[0]
        new_str = file_str.replace(current_version, version)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_str)


def run_cmd_instruction():
    """
    执行打包命令
    :return:
    """
    print("正在打包，请稍候！")
    os.system("pyinstaller main.spec")
    # process = subprocess.Popen(["pyinstaller", "main.spec"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # # 获取命令输出和错误信息
    # stdout, stderr = process.communicate()

    # 检查命令是否成功执行
    # if process.returncode == 0:
    #     print("打包成功！")
    # else:
    #     print("打包失败！")


def del_other_app(path, name, version):
    file_list = os.listdir(path)
    for each in file_list:
        if name in each and version not in each:
            os.remove(os.path.join(path, each))


def change_web_file(copy_path, root_path, name, version):
    p1 = os.path.join(root_path, name + '-' + version + '.exe')
    p2 = os.path.join(copy_path, name + '-' + version + '.exe')
    shutil.copy(p1, p2)
    del_other_app(copy_path, name, version)
    # 修改update.json
    p3 = os.path.join(copy_path, 'update.json')
    with open(p3, 'r', encoding='utf-8') as f:
        data: dict = json.loads(f.read())
    app_info: dict = data.get(name)
    app_info["version"] = int(version)
    with open(p3, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))


def run(spec_file, cfg_file):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y%m%d%H%M")
    name_str = "诊断开发常用工具"
    name = name_str + '-' + str(formatted_time)
    change_spec_file(spec_file, name)
    change_config_file(cfg_file, formatted_time)
    # 打包
    run_cmd_instruction()
    p3 = r'./dist'
    del_other_app(p3, name_str, formatted_time)
    # 修改服务器配置版本
    print("正在修改服务器版本")
    p4 = r'D:\MyWebFile'
    change_web_file(p4, p3, name_str, formatted_time)
    print("程序运行结束")


if __name__ == '__main__':
    p1 = r'./main.spec'
    p2 = r'./src/config.py'
    run(p1, p2)
