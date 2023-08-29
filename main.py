# -*- coding: utf-8 -*-

"""
Copyright 2023 by RicardoJackMC
Teaching Material Download Manager 使用 GPLv3 许可证
本文件是 Teaching Material Download Manager 的一部分
请自行前往
https://github.com/RicardoJackMC/Teaching-Material-Download-Manager
或
https://gitee.com/RicardoJackMC/Teaching-Material-Download-Manager
根据版本号校验本文件MD5
"""
import multiprocessing

import UI
import DOWNLOAD_FUNC
from multiprocessing import Process, Queue, freeze_support
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication
from qfluentwidgets import setTheme, Theme


def start_ui(queue, queue_admin, queue_command):
    print('ui')
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    ui = UI.Ui_MainWindow()
    ui.queue = queue
    ui.queue_admin = queue_admin
    ui.queue_command = queue_command

    ui.set_DISPLAY_MODE()
    if UI.DISPLAY_MODE == 1:
        setTheme(Theme.LIGHT)
    else:
        setTheme(Theme.DARK)

    ui.setupUi(QWidget)
    ui.show()
    ui.welcome_dialog()
    app.exec_()


def start_manager(queue, queue_admin, queue_command):
    print('manager')
    manager = DOWNLOAD_FUNC.Downloader()
    manager.queue = queue
    manager.queue_admin = queue_admin
    manager.queue_command = queue_command
    manager.run()


if __name__ == '__main__':
    freeze_support()
    queue = Queue()
    queue_admin = Queue()
    queue_command = Queue()
    Manager_Process = Process(target=start_manager, args=(queue, queue_admin, queue_command,))
    UI_Process = Process(target=start_ui, args=(queue, queue_admin, queue_command,))
    Manager_Process.start()
    UI_Process.start()
    Manager_Process.join()
    UI_Process.join()
