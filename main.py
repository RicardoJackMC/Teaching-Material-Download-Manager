"""
Copyright 2023 by RicardoJackMC
Teaching Material Download Manager 使用 GPLv3 许可证
本文件是 Teaching Material Download Manager 的一部分
请自行前往 https://github.com/RicardoJackMC/Teaching-Material-Download-Manager 根据版本号校验本文件MD5
"""

import sys
from PyQt5 import QtCore

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication
from qfluentwidgets import setTheme, Theme


import Window
from Window import Ui_MainWindow

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    # setTheme(Theme.AUTO)

    app = QApplication(sys.argv)

    MainWindow = Ui_MainWindow()

    MainWindow.set_DISPLAY_MODE()
    if Window.DISPLAY_MODE == 1:
        setTheme(Theme.LIGHT)
    else:
        setTheme(Theme.DARK)
    MainWindow.setupUi(QWidget)
    MainWindow.show()
    MainWindow.welcome_dialog()
    app.exec_()
