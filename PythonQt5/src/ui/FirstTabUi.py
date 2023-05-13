import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout, QFileDialog, QSpinBox, QTextEdit, QMessageBox, QProgressBar

from src.ui.FirstThreadUi import FirstThreadUi
from src.ui.InputPathUi import *
from src.config import *
from src.ui.MyQProgressBar import MyQProgressBar


class FirstTabUi:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.layout = QVBoxLayout()
        self.debug_msg_list = list()  # 用来存放debug信息
        self._init_tip()
        self._set_path_ui()
        self._set_data_ui()
        self._set_progress_bar_ui()
        # self._set_debug_ui()

    def _init_tip(self):
        label = QLabel("使用说明:该工具只支持CAN和Kwp2000协议命令导出，且协议必须为标准导出格式（$~引脚$~引脚$~波特率$~滤波ID）.")
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)  # 自动换行
        label.setFont(QFont('黑体', 18))
        self.layout.addWidget(label)

    def _set_path_ui(self):
        self.input_path_ui = InputPathUi()
        self.run_btn = self.input_path_ui.run_btn
        self.run_btn.clicked.connect(self._start)
        self.select_btn = self.input_path_ui.select_btn
        self.select_btn.clicked.connect(self._open_dir)
        self.path_edit = self.input_path_ui.path_edit
        layout = self.input_path_ui.get_group_box()
        self.layout.addWidget(layout)

    def _set_data_ui(self):
        self.default_data = {'in_data': {'name': '进入命令回复长度：', 'min': 0, 'default': 0},
                             'idle_data': {'name': '空闲命令回复长度：', 'min': 0, 'default': 0},
                             'quit_data': {'name': '退出命令回复长度：', 'min': 0, 'default': 0},
                             'read_data': {'name': '读码命令回复长度：', 'min': 0, 'default': 20},
                             'clear_data': {'name': '清码命令回复长度：', 'min': 0, 'default': 0},
                             'info_data': {'name': '版本信息命令回复长度：', 'min': 0, 'default': 20},
                             'ds_data': {'name': '数据流命令回复长度：', 'min': 0, 'default': 7},
                             'act_data': {'name': '动作测试命令回复长度：', 'min': 0, 'default': 7},
                             'spe_data': {'name': '特殊功能命令回复长度：', 'min': 0, 'default': 7}}

        self.group_box = QGroupBox()
        self.box_layout = QGridLayout()
        x = 0
        y = 0
        self.receive_data = {}
        for key, value in self.default_data.items():
            tmp_group = QGroupBox()
            h_layout = QHBoxLayout()
            label = QLabel(value['name'])
            spin = QSpinBox()
            spin.setValue(value['default'])
            spin.setMaximum(500)
            self.receive_data[key] = spin
            h_layout.addWidget(label)
            h_layout.addWidget(spin)
            tmp_group.setLayout(h_layout)
            self.box_layout.addWidget(tmp_group, x, y, 1, 1)
            x += 1
        tmp_group = QGroupBox()
        g_layout = QGridLayout()
        self.default_btn = QPushButton("恢复默认")
        self.default_btn.setFixedSize(int(self.width // 10), int(self.height // 4))
        self.default_btn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:30px;color:#666666;}")
        self.default_btn.clicked.connect(self._set_default_data)
        self.del_btn = QPushButton('全部清零')
        self.del_btn.setFixedSize(int(self.width // 10), int(self.height // 4))
        self.del_btn.setStyleSheet("QPushButton{ font-family:'宋体';font-size:30px;color:#666666;}")
        self.del_btn.clicked.connect(self._set_min_data)
        g_layout.addWidget(self.default_btn, 0, 0, 1, 1)
        g_layout.addWidget(self.del_btn, 0, 1, 1, 1)
        tmp_group.setLayout(g_layout)
        self.box_layout.addWidget(tmp_group, 0, 2, 9, 2)
        self.group_box.setLayout(self.box_layout)
        self.layout.addWidget(self.group_box)

    def _set_debug_ui(self):
        # Debug窗口
        group_box = QGroupBox()
        h_layout = QHBoxLayout()
        self.debug_msg = QTextEdit('')
        # 设置TextEdit只读
        self.debug_msg.setReadOnly(True)
        h_layout.addWidget(self.debug_msg)
        self.debug_clear_btn = QPushButton('清空')
        self.debug_clear_btn.clicked.connect(self._clear_debug_edit)
        h_layout.addWidget(self.debug_clear_btn)
        group_box.setLayout(h_layout)
        self.layout.addWidget(group_box)

    def get_layout(self):
        return self.layout

    def _set_default_data(self):
        for key, value in self.default_data.items():
            self.receive_data[key].setValue(value['default'])

    def _set_min_data(self):
        for key, value in self.default_data.items():
            self.receive_data[key].setValue(value['min'])

    def _get_spin_value(self):
        spin_value_dict = {}
        for key, value in self.default_data.items():
            spin_value_dict[key.replace('data', 'value')] = self.receive_data[key].value()
        return spin_value_dict

    def _clear_debug_edit(self):
        self.debug_msg_list.clear()
        self.debug_msg.setText('')
        self.debug_msg.repaint()  # 更新内容,如果不更新可能没有显示新内容

    def _open_dir(self):
        directory = QFileDialog.getOpenFileName(None, "选取文件", CURRENT_PATH, "All Files (*);;Text Files (*.txt)")
        # print(directory)
        self.path_edit.setText(directory[0])

    def _write_debug(self, num):
        # 设置进度条值
        self.progress_bar_ui.setValue(num)
        # self.debug_msg.setText('\n'.join(self.debug_msg_list))
        # # 当文本内容长度超过文本框的高度时，会出现滑条，滑条始终在最底端
        # self.debug_msg.verticalScrollBar().setValue(self.debug_msg.verticalScrollBar().maximum())
        # # self.debug_msg.setText('1')
        # self.debug_msg.repaint()  # 更新内容,如果不更新可能没有显示新内容

    def _end(self, msg):
        msg_box = QMessageBox(QMessageBox.Information, "Tip", msg)
        msg_box.setWindowIcon(QIcon(os.path.join(IMAGE_PATH, 'icon/1.ico')))
        msg_box.exec_()

    def _set_progress_bar_ui(self):
        self.my_pgb = MyQProgressBar()
        self.progress_bar_ui = self.my_pgb.progress_bar_ui
        layout = self.my_pgb.get_layout()
        self.layout.addWidget(layout)

    def _start(self):
        try:
            self.run_btn.setEnabled(False)
            self.debug_msg_list = []
            input_value_dict = self._get_spin_value()
            self.path = self.path_edit.text()
            self.my_thread = FirstThreadUi(self.path, input_value_dict, self.debug_msg_list, self.run_btn)
            self.my_thread.write.connect(self._write_debug)
            self.my_thread.end.connect(self._end)
            self.my_thread.start()
        except Exception:
            self._end("运行出错了！")
            self.run_btn.setEnabled(True)
