from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton
import abc


class InputPathUi:
    def __init__(self, title='文件路径:', run_btn_name="执行", select_btn_name="选择", lear_btn_name="清除",
                 edit_box_text="请输入文件/文件夹路径"):
        self.edit_box_text = edit_box_text
        self.group_box = QGroupBox()
        box_layout = QHBoxLayout()
        str_label = QLabel(title)
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText(edit_box_text)
        self.run_btn = QPushButton(run_btn_name)
        self.select_btn = QPushButton(select_btn_name)
        self.clear_btn = QPushButton(lear_btn_name)
        self.run_btn.clicked.connect(self.start)
        self.select_btn.clicked.connect(self.open_dir)
        self.clear_btn.clicked.connect(self.clear_edit)
        box_layout.addWidget(str_label)
        box_layout.addWidget(self.path_edit)
        box_layout.addWidget(self.run_btn)
        box_layout.addWidget(self.select_btn)
        box_layout.addWidget(self.clear_btn)
        self.group_box.setLayout(box_layout)

    def get_group_box(self):
        return self.group_box

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def open_dir(self):
        pass

    def clear_edit(self):
        self.path_edit.setText('')

    def get_path(self):
        return self.path_edit.text()
