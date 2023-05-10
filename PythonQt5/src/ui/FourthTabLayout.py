import os
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLabel

from src.basic import open_folder_path, clear_edit, message_box
from src.config import IMAGE_PATH
from src.ui.FourthTabThread import FourthTabThread
from src.ui.MyQProgressBar import MyQProgressBar
from src.ui.OutInfoLayout import OutInfoLayout
from src.ui.PathLayout import PathLayout


class FourthTabLayout:
    def __init__(self):
        self.layout = QVBoxLayout()
        self.edit_info_list: List[str] = []
        self._set_tip_layout()
        self._input_path_layout()
        self._set_progress_bar_layout()
        self._set_output_info_layout()

    def _set_tip_layout(self):
        tip_label = QLabel("使用说明:\n\t1.该工具用于识别诊断xml协议中的公式是否存在中文。")
        tip_label.setFont(QFont('黑体', 18))
        tip_label.setWordWrap(True)
        # tip_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(tip_label)

    def get_layout(self):
        return self.layout

    def _input_path_layout(self):
        self.path_layout = PathLayout()
        layout = self.path_layout.set_path_style_2()
        self.run_btn = self.path_layout.run_btn
        self.select_btn = self.path_layout.select_btn
        self.clear_btn = self.path_layout.clear_btn
        self.path_edit = self.path_layout.path_edit
        self.run_btn.clicked.connect(self._start)
        self.select_btn.clicked.connect(lambda: open_folder_path(self.path_edit))
        self.clear_btn.clicked.connect(lambda: clear_edit(self.path_edit))
        self.layout.addWidget(layout)

    def _set_progress_bar_layout(self):
        self.my_pgb = MyQProgressBar(title='执行进度：')
        self.progress_bar_ui = self.my_pgb.progress_bar_ui
        layout = self.my_pgb.get_layout()
        self.layout.addWidget(layout)

    def _set_output_info_layout(self):
        self.edit_layout = OutInfoLayout()
        layout = self.edit_layout.output_info_style_1()
        self.edit = self.edit_layout.text_edit
        self.edit.setText('\n\n\t调试信息窗口，仅显有中文的公式信息。')
        self.layout.addWidget(layout)

    def _write_edit_msg(self, num):
        # 设置进度条值
        self.progress_bar_ui.setValue(num)
        self.edit.setText('\n'.join(self.edit_info_list))
        # 当文本内容长度超过文本框的高度时，会出现滑条，滑条始终在最底端
        self.edit.verticalScrollBar().setValue(self.edit.verticalScrollBar().maximum())
        self.edit.repaint()  # 更新内容,如果不更新可能没有显示新内容

    def _start(self):
        try:
            self.edit.setText('')
            self.edit_info_list.clear()
            self.progress_bar_ui.setValue(0)
            self.run_btn.setEnabled(False)
            if not os.path.exists(self.path_edit.text()):
                message_box("错误", "无效路径！", os.path.join(IMAGE_PATH, 'icon/1.ico'))
                return None
            self.thread = FourthTabThread(self.path_edit.text(), self.edit_info_list)
            self.thread.run_signal.connect(self._write_edit_msg)
            self.thread.msg_signal.connect(message_box)
            self.thread.start()
        except Exception:
            message_box("错误", "执行出错！", os.path.join(IMAGE_PATH, 'icon/1.ico'))
            return None
        finally:
            self.run_btn.setEnabled(True)
