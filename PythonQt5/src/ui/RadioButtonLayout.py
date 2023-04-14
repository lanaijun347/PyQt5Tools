from PyQt5.QtWidgets import QHBoxLayout, QGroupBox, QRadioButton, QLabel


class RadioButtonLayout:
    def __init__(self, tip_str='请选择模式:', *args):
        self.group_box = QGroupBox()
        self.tip_str = tip_str
        self.args = args
        self.btn_dict = {}

    def radio_button_style_1(self):
        label = QLabel(self.tip_str)
        layout = QHBoxLayout()
        layout.addWidget(label)
        key = 0
        for name in self.args:
            self.btn_dict[key] = QRadioButton(name)
            layout.addWidget(self.btn_dict[key])
            key += 1
        self.btn_dict[0].setChecked(True)
        self.group_box.setLayout(layout)
        return self.group_box
