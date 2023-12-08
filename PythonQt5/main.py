import subprocess

from src.ui.MainUi import *

from src.update.UpdateUi import *

# 保存当前app路径
from src.update.update import check_update

run_app_name = os.path.basename(sys.argv[0])
current_app_path = os.path.join(CURRENT_PATH, run_app_name)
# 检查更新
web_version = check_update(URL, APP_NAME, VERSION)

if web_version:
    app = QApplication(sys.argv)
    mainWindow = UpdateUi()
    mainWindow.show()
    mainWindow.star_update(URL, APP_NAME, web_version, CURRENT_PATH, current_app_path)
    sys.exit(app.exec_())
else:
    if os.path.exists(os.path.join(CURRENT_PATH, 'update.py')):
        os.remove(os.path.join(CURRENT_PATH, 'update.py'))
    app = QApplication(sys.argv)
    window = MainUi()
    window.show()
    # 全屏
    # window.showFullScreen()
    sys.exit(app.exec_())
