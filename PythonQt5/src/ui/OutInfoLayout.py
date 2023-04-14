from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QTextEdit


class OutInfoLayout:
    def __init__(self, edit_str=''):
        self.text_edit = QTextEdit(edit_str)
        self.group_box = QGroupBox()

    def output_info_style_1(self):
        layout = QHBoxLayout()
        self.text_edit.setReadOnly(True)  # 设置为只读
        layout.addWidget(self.text_edit)
        self.group_box.setLayout(layout)
        return self.group_box
