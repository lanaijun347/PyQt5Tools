import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

count = 0


# 工作线程
class WorkThread(QThread):
    # pyqtSignal是信号类
    timeout = pyqtSignal()  # 每隔一秒发送一个信号
    end = pyqtSignal()  # 计数完成后发送一个信号

    def run(self):
        while True:
            # 休眠1秒
            self.sleep(1)
            if count == 3:
                self.end.emit()  # 发送end信号，调用和end信号关联的方法
                break
            self.timeout.emit()  # 发送timeout信号


class Counter(QWidget):
    def __init__(self):
        super(Counter, self).__init__()

        self.setWindowTitle("用QThread编写计数器")
        self.resize(300, 200)

        layout = QVBoxLayout()
        self.line_edit = QLineEdit()
        layout.addWidget(self.line_edit)

        # QLCDNumber 用于模拟LED显示效果，类似于Label
        self.lcdNumber = QLCDNumber()
        layout.addWidget(self.lcdNumber)

        button = QPushButton("开始计数")
        layout.addWidget(button)

        self.workThread = WorkThread()
        self.workThread.timeout.connect(self.countTime)
        self.workThread.end.connect(self.end)
        button.clicked.connect(self.work)

        self.setLayout(layout)

    def countTime(self):
        global count
        count += 1
        self.lcdNumber.display(count)

    def end(self):
        QMessageBox.information(self, '消息', '计数结束', QMessageBox.Ok)

    def work(self):
        self.workThread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Counter()
    main.show()
    sys.exit(app.exec_())
