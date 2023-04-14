from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QGroupBox, QLabel


class PathLayout:
    def __init__(self, title='文件路径:', select_btn_name="选择", lear_btn_name="清除",
                 edit_box_text="请输入文件/文件夹路径", **kwargs):
        self.group_box = QGroupBox()
        self.title = title
        self.select_btn_name = select_btn_name
        self.lear_btn_name = lear_btn_name
        self.edit_box_text = edit_box_text
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText(self.edit_box_text )
        self.select_btn = QPushButton(self.select_btn_name)
        self.clear_btn = QPushButton(self.lear_btn_name)

    def set_path_style_1(self):
        name_label = QLabel(self.title)
        layout = QHBoxLayout()
        layout.addWidget(name_label)
        layout.addWidget(self.path_edit)
        layout.addWidget(self.select_btn)
        layout.addWidget(self.clear_btn)
        self.group_box.setLayout(layout)
        return self.group_box
