from src.ui.MainUi import *

app = QApplication(sys.argv)
window = MainUi()
window.show()
# 全屏
# window.showFullScreen()
sys.exit(app.exec_())
