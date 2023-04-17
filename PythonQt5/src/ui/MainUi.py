from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from src.ui.FirstTabUi import *
from src.ui.OtherTabLayout import OtherTabLayout
from src.ui.SecondTabLayout import SecondTabLayout
from src.ui.ThirdTabUi import ThirdTabUi


class MainUi(QWidget):
    def __init__(self):
        super(MainUi, self).__init__(parent=None)
        self.init_ui()

    def init_ui(self):
        self.desktop = QApplication.desktop()
        self.setWindowTitle('Tools')
        # 设置图标
        self.setWindowIcon(QIcon(os.path.join(IMAGE_PATH, 'icon/1.ico')))
        # 隐藏标题栏
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置背景色
        # self.setStyleSheet("background-color:rgb(84,82,120)")
        # 获取屏幕分辨率
        screenRect = self.desktop.screenGeometry()
        self.height = screenRect.height()
        self.width = screenRect.width()
        # 设置窗体大小
        self.ui_x = int(self.width * 0.8)
        self.ui_y = int(self.height * 0.8)
        self.resize(self.ui_x, self.ui_y)
        # 居中显示
        # self.move(int((self.width - self.ui_x) / 2), int((self.height - self.ui_y) / 2))
        self.move(int((self.width - self.ui_x) / 2), 20)
        # 设置主界面布局模式
        self.gridLayout = QGridLayout(self)
        self.setLayout(self.gridLayout)
        self.set_table()

    def set_table(self):
        self.tab1 = QWidget(parent=None)
        self.tab2 = QWidget(parent=None)
        self.tab3 = QWidget(parent=None)
        self.other_tab = QWidget(parent=None)
        # 创建选项卡
        self.tab_widget = QTabWidget(self)
        # 设置选项卡界面大小
        # self.tab_widget.resize(self.width, self.height)
        # 设置选项卡颜色
        # self.tab_widget.setStyleSheet("background-color:rgb(84,82,120)")
        # 添加选项卡
        self.tab_widget.addTab(self.tab1, '协议命令获取')
        self.tab_widget.addTab(self.tab2, '文件/文件夹拷贝工具')
        self.tab_widget.addTab(self.tab3, '获取帧ID和滤波ID')
        self.tab_widget.addTab(self.other_tab, '扩展服务')
        # 选项卡再主界面布局
        self.gridLayout.addWidget(self.tab_widget, 0, 0, 1, 1)
        # 加载选项卡内容
        self.init_tab1_ui()
        self.init_tab2_ui()
        self.init_tab3_ui()
        self.init_other_tab_ui()

    def init_tab1_ui(self):
        self.tab1_ui = FirstTabUi(self.ui_x, self.ui_y)
        layout = self.tab1_ui.get_layout()
        self.tab1.setLayout(layout)

    def init_tab2_ui(self):
        self.tab2_ui = SecondTabLayout()
        layout = self.tab2_ui.get_layout()
        self.tab2.setLayout(layout)

    def init_tab3_ui(self):
        self.tab3_ui = ThirdTabUi()
        layout = self.tab3_ui.get_layout()
        self.tab3.setLayout(layout)

    def init_other_tab_ui(self):
        self.other_tab_ui = OtherTabLayout()
        layout = self.other_tab_ui.set_other_layout_1()
        self.other_tab.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainUi()
    w.show()
    sys.exit(app.exec_())
