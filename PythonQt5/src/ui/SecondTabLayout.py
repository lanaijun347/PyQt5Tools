import os.path

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QFileDialog, QGroupBox, QHBoxLayout, QPushButton, QGridLayout, \
    QMessageBox

from src.config import *
from src.ui.MyEnum import MyEnum
from src.ui.MyQProgressBar import MyQProgressBar
from src.ui.OutInfoLayout import OutInfoLayout
from src.ui.PathLayout import PathLayout
from src.ui.RadioButtonLayout import RadioButtonLayout
import src.basic as Bs
from src.ui.SecondTabThread import SecondTabThread


class SecondTabLayout:
    def __init__(self):
        self.layout = QVBoxLayout()
        self.edit_info_list = []
        self._set_tip_layout()
        self._set_input_menu_path_layout()
        self._set_input_from_path_layout()
        self._set_input_copy_path_layout()
        self._select_type_layout()
        self._set_progress_bar_layout()
        self._set_output_info_layout()
        self._set_run_layout()

    def _set_tip_layout(self):
        tip_label = QLabel("使用说明:\n\t1.该工具根据 协议菜单/xml菜单 拷贝 文件/文件夹 到指定路径；\n\t"
                           "2.仅支持txt、asm、xml格式菜单，请先把文件转换成 UTF-8 格式；\n\t"
                           "3.协议菜单只选取最后一层，xml菜单只选path属性最后一层。")
        tip_label.setFont(QFont('黑体', 18))
        tip_label.setWordWrap(True)
        self.layout.addWidget(tip_label)

    def get_layout(self):
        return self.layout

    def _set_input_menu_path_layout(self):
        self.menu_layout = PathLayout(edit_box_text='请输入协议菜单/xml菜单文件', title='菜单路径:')
        layout = self.menu_layout.set_path_style_1()
        self.menu_select_btn = self.menu_layout.select_btn
        self.menu_clear_btn = self.menu_layout.clear_btn
        self.menu_path_edit = self.menu_layout.path_edit
        self.menu_select_btn.clicked.connect(lambda: self._push_select_file_btn(self.menu_path_edit))
        self.menu_clear_btn.clicked.connect(lambda: self._push_clear_path(self.menu_path_edit))
        self.layout.addWidget(layout)

    def _set_input_from_path_layout(self):
        self.from_layout = PathLayout(edit_box_text='请输入源文件夹路径', title='源文件夹路径:')
        layout = self.from_layout.set_path_style_1()
        self.from_select_btn = self.from_layout.select_btn
        self.from_clear_btn = self.from_layout.clear_btn
        self.from_path_edit = self.from_layout.path_edit
        self.from_select_btn.clicked.connect(lambda: self._push_select_folder_btn(self.from_path_edit))
        self.from_clear_btn.clicked.connect(lambda: self._push_clear_path(self.from_path_edit))
        self.layout.addWidget(layout)

    def _set_input_copy_path_layout(self):
        self.copy_layout = PathLayout(edit_box_text='请输入拷贝文件夹路径', title='拷贝文件夹路径:')
        layout = self.copy_layout.set_path_style_1()
        self.copy_select_btn = self.copy_layout.select_btn
        self.copy_clear_btn = self.copy_layout.clear_btn
        self.copy_path_edit = self.copy_layout.path_edit
        self.copy_select_btn.clicked.connect(lambda: self._push_select_folder_btn(self.copy_path_edit))
        self.copy_clear_btn.clicked.connect(lambda: self._push_clear_path(self.copy_path_edit))
        self.layout.addWidget(layout)

    def _select_type_layout(self):
        radio_group_box = QGroupBox()
        radio_group_box_layout = QHBoxLayout()
        self.menu_radio_layout = RadioButtonLayout('请选择菜单类型：', "协议菜单", "XML菜单")
        menu_radio_layout = self.menu_radio_layout.radio_button_style_1()
        self.menu_radio_data = self.menu_radio_layout.btn_dict
        self.copy_radio_layout = RadioButtonLayout('请选择拷贝类型：', "文件拷贝", "文件夹拷贝")
        copy_radio_layout = self.copy_radio_layout.radio_button_style_1()
        self.copy_radio_data = self.copy_radio_layout.btn_dict
        radio_group_box_layout.addWidget(menu_radio_layout)
        radio_group_box_layout.addWidget(copy_radio_layout)
        radio_group_box.setLayout(radio_group_box_layout)
        self.layout.addWidget(radio_group_box)

    def _set_progress_bar_layout(self):
        self.my_pgb = MyQProgressBar(title='拷贝进度：')
        self.progress_bar_ui = self.my_pgb.progress_bar_ui
        layout = self.my_pgb.get_layout()
        self.layout.addWidget(layout)

    def _set_output_info_layout(self):
        self.edit_layout = OutInfoLayout()
        layout = self.edit_layout.output_info_style_1()
        self.edit = self.edit_layout.text_edit
        self.edit.setText('\n\n\t调试信息窗口，仅显示拷贝出错信息。')
        self.layout.addWidget(layout)

    def _set_run_layout(self):
        group_box = QGroupBox()
        layout = QGridLayout()
        self.run_btn = QPushButton('执行')
        self.clear_btn = QPushButton('清除')
        layout.addWidget(QLabel(''), 0, 1)
        layout.addWidget(QLabel(''), 0, 2)
        layout.addWidget(self.run_btn, 0, 3)
        layout.addWidget(self.clear_btn, 0, 4)
        layout.addWidget(QLabel(''), 0, 5)
        layout.addWidget(QLabel(''), 0, 6)
        group_box.setLayout(layout)
        self.layout.addWidget(group_box)
        self.clear_btn.clicked.connect(self._clear_edit_info)
        self.run_btn.clicked.connect(self._run)

    def _push_select_file_btn(self, edit):
        directory = QFileDialog.getOpenFileName(None, "选取文件", CURRENT_PATH, "All Files (*);;Text Files (*.txt)")
        edit.setText(directory[0])

    def _push_select_folder_btn(self, edit):
        directory = QFileDialog.getExistingDirectory(None, "选取文件夹", CURRENT_PATH)
        edit.setText(directory)

    def _push_clear_path(self, edit):
        edit.setText('')

    def _clear_edit_info(self):
        self.edit_info_list.clear()
        self.edit.setText('')
        self.edit.repaint()  # 更新内容,如果不更新可能没有显示新内容

    def message_box(self, title, msg):
        msg_box = QMessageBox(QMessageBox.Information, title, msg)
        msg_box.setWindowIcon(QIcon(os.path.join(IMAGE_PATH, 'icon/1.ico')))
        msg_box.exec_()

    def path_exists(self, path_title, path):
        if not os.path.exists(path):
            self.message_box('错误', f'{path_title}路径不存在。')
            return False
        return True

    def match_path_and_radio(self, path) -> tuple:
        """
        判读路径下文件/问价夹与按钮选择类型是否一致
        :param path:
        :return: bool
        """
        result = True
        file_list = []
        cp_type = 0
        # 0：文件拷贝类型  1：文件夹拷贝类型
        copy_type: bool = self.copy_radio_data[MyEnum.File_type.value].isChecked()
        for file_name in os.listdir(path):
            tmp_path = os.path.join(path, file_name)
            if copy_type:  # 文件拷贝类型
                cp_type = MyEnum.File_type.value
                if os.path.isfile(tmp_path):
                    file_list.append(tmp_path)
            else:  # 文件夹拷贝类型
                cp_type = MyEnum.Dir_type.value
                if os.path.isdir(tmp_path):
                    file_list.append(tmp_path)
        if len(file_list) < 1:
            if copy_type:
                self.message_box("警告", "源文件路径无该文件，请确认拷贝类型是否选择正确!")
            else:
                self.message_box("警告", "源文件路径无文件夹，请确认拷贝类型是否选择正确!")
            result = False
        return result, cp_type, file_list

    def menu_parsing(self, path) -> tuple:
        # 0：为协议菜单  1：XML菜单
        result = True
        protocol_type: bool = self.menu_radio_data[MyEnum.Protocol_type.value].isChecked()
        file_name_list = []
        protocol_file_format = ['TXT', 'ASM']
        xml_file_format = ['XML']
        try:
            file_format = os.path.split(path)[-1].split('.')[-1]
            if protocol_type:  # 协议菜单
                if file_format.upper() in protocol_file_format:
                    file_name_list = Bs.get_protocol_menu_id(path)
            else:  # XML菜单
                if file_format.upper() in xml_file_format:
                    file_name_list = Bs.get_menu_xml_path_attribute_last_layer(path)
            if len(file_name_list) < 1:
                if protocol_type:
                    self.message_box("警告", "协议菜单未获取到文件拷贝信息，请确认菜单文件/格式/类型选择是否有误!")
                else:
                    self.message_box("警告", "XML菜单未获取到文件拷贝信息，请确认菜单文件/格式/类型选择是否有误!")
                result = False
        except Exception:
            self.message_box("错误", "菜单解析出错，请确认是否是UTF-8格式!")
            result = False
        finally:
            return result, file_name_list

    def _write_edit_msg(self, num):
        # 设置进度条值
        self.progress_bar_ui.setValue(num)
        self.edit.setText('\n'.join(self.edit_info_list))
        # 当文本内容长度超过文本框的高度时，会出现滑条，滑条始终在最底端
        self.edit.verticalScrollBar().setValue(self.edit.verticalScrollBar().maximum())
        # self.debug_msg.setText('1')
        self.edit.repaint()  # 更新内容,如果不更新可能没有显示新内容

    def _run(self):
        try:
            self.edit.setText('')
            self.run_btn.setEnabled(False)
            if not self.path_exists(self.menu_layout.title, self.menu_path_edit.text()):
                return None
            if not self.path_exists(self.from_layout.title, self.from_path_edit.text()):
                return None
            if not self.path_exists(self.copy_layout.title, self.copy_path_edit.text()):
                return None
            parsing_result, file_name_list = self.menu_parsing(self.menu_path_edit.text())
            if not parsing_result:
                return None
            compare_result, copy_type, from_path_list = self.match_path_and_radio(self.from_path_edit.text())
            if not compare_result:
                return None
            self.edit_info_list.clear()
            self.thread = SecondTabThread(copy_type, from_path_list, file_name_list, self.copy_path_edit.text(),
                                          self.edit_info_list, self.run_btn)
            self.thread.run_signal.connect(self._write_edit_msg)
            self.thread.msg_signal.connect(self.message_box)
            self.thread.start()
        except Exception:
            self.message_box("错误", "运行出错!")
        finally:
            self.run_btn.setEnabled(True)
