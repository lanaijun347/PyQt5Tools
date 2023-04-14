import sys
import time
from time import sleep

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import *


class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle('测试QThread')
        self.resize(600, 600)
        self.layout = QVBoxLayout()
        self.line_edit = QLineEdit()
        self.btn = QPushButton('执行')
        self.btn.clicked.connect(self.my_run)
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.btn)
        self.setLayout(self.layout)
        self.my_thread = MyThread(self.text_edit)
        self.my_thread.timeout.connect(self.countTime)
        # self.my_thread.end.connect(self.end)
        self.i = 0

    def my_run(self):
        # self.my_thread = MyThread(self.text_edit)
        # i = 0
        # while i < 100:
        #     i -= 1
        # for i in range(0, 10):
        #     self.my_thread.start()
        self.my_thread.start()

    def countTime(self):
        self.text_edit.setText('执行' + str(self.i))
        self.text_edit.repaint()
        self.i += 1


class MyThread(QThread):
    timeout = pyqtSignal()  # 每隔一秒发送一个信号
    end = pyqtSignal()  # 计数完成后发送一个信号

    def __init__(self, text_edit):
        super(MyThread, self).__init__()
        # self.text_edit = text_edit

    def run(self) -> None:
        # for i in range(0, 100):
        #     print('执行.')
        #     self.text_edit.setText('执行' + str(i))
        #     self.text_edit.repaint()
        #     sleep(1)
        i = 0
        while i < 100:
            sleep(1)
            add1 = AddNum()
            flag = add1.add_num(i)
            if flag:
                self.timeout.emit()  # 发送timeout信号
            # self.timeout.emit()  # 发送timeout信号
            i += 1


class AddNum:
    def __init__(self):
        pass

    def add_num(self, num):
        if num % 2 == 0:
            return True
        else:
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())
