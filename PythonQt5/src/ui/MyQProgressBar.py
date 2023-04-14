from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QProgressBar


class MyQProgressBar:
    def __init__(self, title='执行进度：'):
        self.group_box = QGroupBox()
        layout = QHBoxLayout()
        self.group_box.setLayout(layout)
        label = QLabel(title)
        self.progress_bar_ui = QProgressBar()
        self.progress_bar_ui.setMinimum(0)
        self.progress_bar_ui.setMaximum(100)
        self.progress_bar_ui.setStyleSheet(
            "QProgressBar { border: 2px solid grey; border-radius: 5px; background-color: #FFFFFF; text-align: center;}QProgressBar::chunk {background:QLinearGradient(x1:0,y1:0,x2:2,y2:0,stop:0 #666699,stop:1  #DB7093); }")
        layout.addWidget(label)
        layout.addWidget(self.progress_bar_ui)

    def get_layout(self):
        return self.group_box
