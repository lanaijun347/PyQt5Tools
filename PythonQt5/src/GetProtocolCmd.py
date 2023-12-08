import re


class GetProtocolCmd:
    def __init__(self, path):
        self.path = path
        self.file_str = ''

        self.init_file()

    def init_file(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            self.file_str = f.read()

    def get_cmd_type(self) -> str:
        cmd_type = ''
        activation_line = ''
        if re.findall(r'\$CAN+1', self.file_str):
            # CAN关键字节后移一个字节的协议
            cmd_type = "CAN+1"
            return cmd_type
        if re.findall(r'\$EXCAN', self.file_str):
            # 自定义扩展CAN协议（目前沃尔沃遇到）
            cmd_type = "EXCAN"
            return cmd_type
        if re.findall(r'\$TP1.6', self.file_str):
            # TP1.6协议
            cmd_type = "TP1.6"
            return cmd_type
        if re.findall(r'\$TP2.0', self.file_str):
            # TP2.0协议
            cmd_type = "TP2.0"
            return cmd_type
        if re.findall(r'\$D2(KWPD3B0)', self.file_str):
            # 与KW2000类似，只是帧长是两个字节计算（目前沃尔沃遇到）
            cmd_type = "D2(KWPD3B0)"
            return cmd_type
        if re.findall(r'\$NEKW', self.file_str):
            # 负逻辑串行协议（目前日产遇到）
            cmd_type = "NEKW"
            return cmd_type
        if re.findall(r'\$J1939', self.file_str):
            # J1939协议
            cmd_type = "J1939"
            return cmd_type
        activation_list = re.findall(r"\$~.*\n", self.file_str)
        for line in activation_list:
            tmp_list = re.findall(r'\$~', line)
            if len(tmp_list) >= 3:
                activation_line = line
                break
        # print(activation_list)


if __name__ == '__main__':
    p = r'D:\xiaolan\github_347\PyQt5Tools\PythonQt5\dist\ECM_A83108_CAN_6E_07E8_AS24.asm'
    cmd = GetProtocolCmd(p)
    cmd.get_cmd_type()
