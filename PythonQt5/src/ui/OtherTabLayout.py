import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QLabel

from src.config import IMAGE_PATH


class OtherTabLayout:
    def __init__(self):
        self.layout = QVBoxLayout()

    def set_other_layout_1(self):
        group_box = QGroupBox()
        layout = QVBoxLayout()
        group_box.setLayout(layout)
        layout.setAlignment(Qt.AlignCenter)
        label_str = QLabel("更多功能请扫描下方二维码定制")
        label_str.setFont(QFont('黑体', 18))
        label_str.setAlignment(Qt.AlignCenter)
        pix = QPixmap(os.path.join(IMAGE_PATH, "WeChatFriendQRCode.png"))
        pix_w = pix.width()
        pix_h = pix.height()
        label_pix = QLabel("图片")
        label_pix.setPixmap(pix)
        # label_pix.setMaximumSize(pix_w, pix_h)
        label_pix.setScaledContents(True)
        layout.addWidget(label_str)
        layout.addWidget(QLabel(""))
        layout.addWidget(label_pix)
        layout.addWidget(QLabel(""))
        self.layout.addWidget(group_box)
        return self.layout

    def get_layout(self):
        return self.layout
