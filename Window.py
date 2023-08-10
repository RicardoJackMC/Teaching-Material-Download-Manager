"""
Copyright 2023 by RicardoJackMC
Teaching Material Download Manager 使用 GPLv3 许可证
本文件是 Teaching Material Download Manager 的一部分
请自行前往 https://github.com/RicardoJackMC/Teaching-Material-Download-Manager 根据版本号校验本文件MD5
"""

import json
import os
import sys
import webbrowser
import winreg
import resources_rc

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication, QThread, pyqtSignal, Qt, QEvent
from PyQt5.QtGui import QPainter, QColor, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidgetItem, QPushButton, QLabel, QListWidget
from qfluentwidgets import CardWidget, IconWidget, BodyLabel, CaptionLabel, TransparentToolButton, FluentIcon, \
    CheckBox, ComboBox, LineEdit, ListWidget, PushButton, Dialog, InfoBar, InfoBarPosition, SubtitleLabel, \
    setThemeColor, PopupTeachingTip, TeachingTipTailPosition, FlyoutViewBase, RoundMenu, Action, MenuAnimationType

from Textbook_File import TEXTBOOK_FILE

textbook_file = None
data_dictionary = {}
kill = 0
DISPLAY_MODE = 0


class RoundWindow(QWidget):

    def __init__(self, parent=None):
        super(RoundWindow, self).__init__(parent)
        self.border_width = 8

    def paintEvent(self, event):
        global DISPLAY_MODE
        pat = QPainter(self)
        pat.setRenderHint(pat.Antialiasing)
        if DISPLAY_MODE == 1:
            pat.setBrush(QColor(243, 243, 243, 255))
        else:
            pat.setBrush(QColor(32, 32, 32, 255))
        pat.setPen(Qt.transparent)

        rect = self.rect()
        rect.setLeft(9)
        rect.setTop(9)
        rect.setWidth(rect.width() - 9)
        rect.setHeight(rect.height() - 9)
        pat.drawRoundedRect(rect, 15, 15)


class CustomFlyoutView(FlyoutViewBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.label = BodyLabel(
            '如果你在使用本软件时遇到了任何问题, 或对本软件有任何建议, 请务必告诉开发者。 \n您可以在本软件的GitHub仓库中提出issue, \n或发送电子邮件到ricardojackmc@gmail.com。')
        self.tranparentToolButton = TransparentToolButton(FluentIcon.MAIL, self)
        self.tranparentToolButton.clicked.connect(self.mail)
        self.tranparentToolButton.setFixedWidth(32)
        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.setContentsMargins(20, 16, 20, 16)
        self.vBoxLayout.addWidget(self.label)
        self.vBoxLayout.addWidget(self.tranparentToolButton)

    def paintEvent(self, e):
        pass

    def mail(self):
        webbrowser.open_new('mailto:ricardojackmc@gmail.com')


class AppCard(CardWidget):
    """ App card """

    def __init__(self, icon, title, content, url=None, parent=None):
        super().__init__(parent)
        self.url = url
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        self.tranparentToolButton = TransparentToolButton(FluentIcon.LINK, self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(20, 20)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        self.tranparentToolButton.setFixedWidth(32)
        self.hBoxLayout.addWidget(self.tranparentToolButton, 0, Qt.AlignRight)

        self.hBoxLayout.setContentsMargins(20, 11, 11, 11)
        self.hBoxLayout.setSpacing(15)
        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.tranparentToolButton, 0, Qt.AlignRight)
        if self.url == 'feedback':
            self.tranparentToolButton.clicked.connect(self.feedback)
        else:
            self.tranparentToolButton.clicked.connect(self.open_url)

    def open_url(self):
        webbrowser.open_new(self.url)

    def feedback(self):
        PopupTeachingTip.make(
            target=self.tranparentToolButton,
            view=CustomFlyoutView(),
            tailPosition=TeachingTipTailPosition.TOP,
            duration=10000,
            parent=self
        )


class AboutWindow(RoundWindow, QWidget):

    def setupUi(self, QWidget):
        self.setObjectName("About")
        self.setWindowTitle('About')
        self.setWindowIcon(QIcon(':/recourse/logo.ico'))
        self.resize(540, 900)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.centralwidget = QtWidgets.QWidget(self)

        QtCore.QMetaObject.connectSlotsByName(self)

        ICON = QLabel(self.centralwidget)
        ICON.setGeometry(QtCore.QRect(180, 40, 200, 200))
        pixmap = QPixmap(':/recourse/logo.png')
        ICON.setPixmap(pixmap)
        ICON.setScaledContents(True)

        title = SubtitleLabel('Teaching Material Download Manager', self.centralwidget)
        title.setGeometry(QtCore.QRect(97, 240, 350, 30))

        copyright_label = BodyLabel('Copyright 2023 by RicardoJackMC', self.centralwidget)
        copyright_label.setGeometry(QtCore.QRect(164, 270, 211, 20))

        version = CaptionLabel('Ver.1.0.0_202308101622', self.centralwidget)
        version.setGeometry(QtCore.QRect(206, 294, 127, 10))

        tip = CaptionLabel('请前往本项目GitHub仓库获取更新或根据版本号校验MD5', self.centralwidget)
        tip.setGeometry(QtCore.QRect(115, 305, 310, 20))

        Subtitle_1 = BodyLabel('关于本软件', self.centralwidget)
        Subtitle_1.setGeometry(QtCore.QRect(41, 344, 460, 30))

        card_about_gpl = AppCard(FluentIcon.CERTIFICATE, "本软件使用 GPLv3 许可证",
                                 "点击右侧按钮阅读GPLv3许可证原文",
                                 'https://www.gnu.org/licenses/gpl-3.0.html#license-text', self.centralwidget)
        card_about_gpl.setGeometry(QtCore.QRect(40, 374, 460, 80))

        card_source_code = AppCard(FluentIcon.CODE, "获取源代码",
                                   "点击右侧按钮访问本软件GitHub仓库",
                                   'https://github.com/RicardoJackMC/Teaching-Material-Download-Manager',
                                   self.centralwidget)
        card_source_code.setGeometry(QtCore.QRect(40, 449, 460, 80))

        card_feedback = AppCard(FluentIcon.FEEDBACK, "反馈",
                                "帮助完善此软件",
                                url='feedback', parent=self.centralwidget)
        card_feedback.setGeometry(QtCore.QRect(40, 524, 460, 80))

        card_website = AppCard(FluentIcon.HOME_FILL, "惰猫の小窝",
                               "点击右侧按钮前往作者的个人网站",
                               'https://ricardojackmc.github.io/', self.centralwidget)
        card_website.setGeometry(QtCore.QRect(40, 599, 460, 80))

        Subtitle_2 = BodyLabel('本软件的诞生离不开下列项目的支持', self.centralwidget)
        Subtitle_2.setGeometry(QtCore.QRect(41, 682, 460, 30))

        card_qfluentwidgets = AppCard(':/recourse/qfluentwidgets_logo.png', "PyQt-Fluent-Widgets",
                                      '本软件界面基于此项目开发',
                                      'https://github.com/zhiyiYo/PyQt-Fluent-Widgets', self.centralwidget)
        card_qfluentwidgets.setGeometry(QtCore.QRect(41, 712, 460, 30))

        card_icon = AppCard(FluentIcon.GITHUB, "fluentui-system-icons",
                            "本软件图标基于此项目制作",
                            "https://github.com/microsoft/fluentui-system-icons", self.centralwidget)
        card_icon.setGeometry(QtCore.QRect(41, 787, 460, 30))

        pushButton_close = QPushButton(self.centralwidget)
        pushButton_close.setGeometry(QtCore.QRect(20, 20, 15, 15))
        pushButton_close.setMinimumSize(QtCore.QSize(15, 15))
        pushButton_close.setMaximumSize(QtCore.QSize(15, 15))
        pushButton_close.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        pushButton_close.setFocusPolicy(QtCore.Qt.NoFocus)
        pushButton_close.setStyleSheet(
            "QPushButton{background:#F76677;border-radius:7px;}\n"
            "QPushButton:hover{background:red;}")
        pushButton_close.setText("")
        pushButton_close.setObjectName("pushButton_close")

        pushButton_maximize = QPushButton(self.centralwidget)
        pushButton_maximize.setGeometry(QtCore.QRect(40, 20, 15, 15))
        pushButton_maximize.setMinimumSize(QtCore.QSize(15, 15))
        pushButton_maximize.setMaximumSize(QtCore.QSize(15, 15))
        pushButton_maximize.setFocusPolicy(QtCore.Qt.NoFocus)
        pushButton_maximize.setStyleSheet(
            "QPushButton{background:#F7D674;border-radius:7px;}\n"
            "QPushButton:hover{background:yellow;}")
        pushButton_maximize.setText("")
        pushButton_maximize.setObjectName("pushButton_maximize")
        pushButton_maximize.setEnabled(False)

        pushButton_minimize = QPushButton(self.centralwidget)
        pushButton_minimize.setGeometry(QtCore.QRect(60, 20, 15, 15))
        pushButton_minimize.setMinimumSize(QtCore.QSize(15, 15))
        pushButton_minimize.setMaximumSize(QtCore.QSize(15, 15))
        pushButton_minimize.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        pushButton_minimize.setFocusPolicy(QtCore.Qt.NoFocus)
        pushButton_minimize.setStyleSheet(
            "QPushButton{background:#6DDF6D;border-radius:7px;}\n"
            "QPushButton:hover{background:green;}")
        pushButton_minimize.setText("")
        pushButton_minimize.setObjectName("pushButton_minimize")

        pushButton_close.clicked.connect(self.close)
        pushButton_minimize.clicked.connect(self.showMinimized)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_flag = True
            self.mouse_Position = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.mouse_flag:
            self.move(QMouseEvent.globalPos() - self.mouse_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.mouse_flag = False


class update_data_func(QThread):
    update_listwidget_signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.switch = True
        self.previous = {}
        self.dictionary = {}

    def run(self):
        global textbook_file, kill, data_dictionary
        data_dictionary = {}
        kill = 0
        while kill == 0:
            try:
                data_dictionary.update(textbook_file.result_data)
                if self.previous != textbook_file.result_data:
                    self.update_listwidget_signal.emit(textbook_file.result_data)
                    self.previous.update(textbook_file.result_data)
            except:
                pass

    def switch_off(self):
        self.switch = False


class download_func(QThread):
    warning_signal = pyqtSignal()
    error_signal = pyqtSignal()
    ID_A_warning_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.url = None
        self.save_mode = None
        self.save_path = None
        self.list_enable_value = None

    def run(self):
        global textbook_file, data_dictionary
        textbook_file.save_mode = self.save_mode
        textbook_file.save_path = self.save_path
        get_ID_A_result = textbook_file.get_ID_A(self.url)
        if get_ID_A_result:
            textbook_file.analyse_json_url()
            download_pdf_file_result = textbook_file.download_pdf_file()
            if download_pdf_file_result:
                if textbook_file.warning == 1:
                    self.warning_signal.emit()
            else:

                self.error_signal.emit()
        else:
            self.ID_A_warning_signal.emit()


class download_manager_func(QThread):
    send_update_listwidget_signal_frommanager = pyqtSignal(dict)

    send_ID_A_warning_signal = pyqtSignal()
    send_warning_signal = pyqtSignal()
    send_error_signal = pyqtSignal()
    send_single_download_finish = pyqtSignal(str)
    send_all_download_finish = pyqtSignal()
    list_download_signal = pyqtSignal()
    auto_download_signal = pyqtSignal()
    single_download_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setting_finished = False
        self.auto_download_enable_value = None
        self.list_enable_value = None
        self.keep = False
        self.manual = False
        self.save_mode = None
        self.save_path = None
        self.url = None
        self.url_list = None
        self.infor_finish = False
        self.start_download = False

    def run(self):
        global textbook_file
        self.download_thread = download_func()
        self.download_thread.ID_A_warning_signal.connect(self.get_ID_A_warning_signal)
        self.download_thread.warning_signal.connect(self.get_warning_signal)
        self.download_thread.error_signal.connect(self.get_error_signal)

        if self.manual:
            if self.list_enable_value == 0:
                self.single_download_signal.emit()
                while not self.setting_finished:
                    pass
                self.download_thread.save_mode = self.save_mode
                self.download_thread.save_path = self.save_path
                self.download_thread.url = self.url
                textbook_file = TEXTBOOK_FILE()
                update_data_thread = update_data_func()
                update_data_thread.update_listwidget_signal.connect(self.get_update_listwidget_signal)
                update_data_thread.start()
                self.download_thread.start()
                self.download_thread.wait()
                update_data_thread.wait()
                self.send_single_download_finish.emit(self.url)
                self.send_all_download_finish.emit()
                self.setting_finished = False
                self.manual = False

            elif self.list_enable_value == 1:
                if self.auto_download_enable_value == 0:
                    self.infor_finish = False
                    self.list_download_signal.emit()
                    while not self.setting_finished:
                        pass
                    url_list = self.url_list.copy()
                    for self.url in url_list:
                        self.download_thread.save_mode = self.save_mode
                        self.download_thread.save_path = self.save_path
                        self.download_thread.url = self.url
                        textbook_file = TEXTBOOK_FILE()
                        update_data_thread = update_data_func()
                        update_data_thread.update_listwidget_signal.connect(self.get_update_listwidget_signal)
                        update_data_thread.start()
                        self.download_thread.start()
                        self.download_thread.wait()
                        update_data_thread.wait()
                        self.send_single_download_finish.emit(self.url)
                    self.send_all_download_finish.emit()
                    self.setting_finished = False
                    self.manual = False

        while self.auto_download_enable_value == 1:
            if self.start_download:
                self.auto_download_signal.emit()
                while not self.setting_finished:
                    pass
                url_list = self.url_list.copy()
                for self.url in url_list:
                    self.download_thread.save_mode = self.save_mode
                    self.download_thread.save_path = self.save_path
                    self.download_thread.url = self.url
                    textbook_file = TEXTBOOK_FILE()
                    update_data_thread = update_data_func()
                    update_data_thread.update_listwidget_signal.connect(self.get_update_listwidget_signal)
                    update_data_thread.start()
                    self.download_thread.start()
                    self.download_thread.wait()
                    update_data_thread.wait()
                    self.send_single_download_finish.emit(self.url)

    def get_update_listwidget_signal(self, dictionary):
        self.send_update_listwidget_signal_frommanager.emit(dictionary)

    def get_ID_A_warning_signal(self):
        self.send_ID_A_warning_signal.emit()

    def get_warning_signal(self):
        self.send_warning_signal.emit()

    def get_error_signal(self):
        self.send_error_signal.emit()

    def get_single_download_finish(self):
        self.send_single_download_finish.emit()

    def keep_on(self):
        self.keep = True

    def keep_off(self):
        self.keep = False


class Ui_MainWindow(RoundWindow, QWidget):

    def setupUi(self, QWidget):
        self.folder = ''
        self.config = {}
        self.list = []
        self.download_data = {}
        self.warning = 0
        self.error = 0
        self.ID_A_warning = 0
        self.delete_menu_enable = True

        if os.path.isfile('.\\config.json'):
            with open('config.json', 'r') as f:
                self.config = json.load(f)

        self.list_enable_value = self.config['list_enable_value']
        self.auto_download_enable_value = self.config['auto_download_enable_value']
        self.open_folder_value = self.config['open_folder_value']
        self.save_mode = self.config['save_mode']
        self.folder = self.config['folder']
        self.first_open = self.config['first_open']



        self.setObjectName("Main")
        self.setWindowTitle("Teaching Material Download Manager")
        self.setWindowIcon(QIcon(':/recourse/logo.ico'))
        self.resize(1000, 540)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        theme_color = self.get_windows_theme_color()
        if theme_color != None:
            setThemeColor(QColor(theme_color[0], theme_color[1], theme_color[2]))
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.listWidget = ListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(510, 95, 450, 350))
        self.listWidget.setObjectName("listWidget")

        self.label_2 = SubtitleLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 145, 450, 30))
        self.label_2.setObjectName("label_2")

        self.lineEdit = LineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(40, 180, 340, 45))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setFixedSize(340, 45)

        self.pushButton = PushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(390, 180, 45, 45))
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = PushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(450, 180, 45, 45))
        self.pushButton_2.setObjectName("pushButton_2")
        if os.path.isdir(self.folder):
            self.pushButton_2.setEnabled(False)
            self.lineEdit.setText(self.folder)

        self.lineEdit_2 = LineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(40, 40, 450, 45))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setFixedSize(450, 45)

        self.pushButton_3 = PushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 95, 220, 45))
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = PushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(270, 95, 220, 45))
        self.pushButton_4.setObjectName("pushButton_4")

        self.checkBox = CheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(40, 295, 220, 25))
        self.checkBox.setObjectName("checkBox")

        self.checkBox_2 = CheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(40, 265, 220, 25))
        self.checkBox_2.setObjectName("checkBox_2")

        self.checkBox_3 = CheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(40, 235, 220, 25))
        self.checkBox_3.setObjectName("checkBox_3")

        self.label = BodyLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(270, 235, 220, 25))
        self.label.setObjectName("label")

        self.comboBox = ComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(270, 260, 220, 30))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        self.pushButton_5 = PushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(740, 40, 220, 45))
        self.pushButton_5.setObjectName("pushButton_5")

        self.pushButton_6 = PushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(510, 40, 220, 45))
        self.pushButton_6.setObjectName("pushButton_6")

        self.pushButton_7 = PushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(510, 455, 450, 45))
        self.pushButton_7.setObjectName("pushButton_7")

        self.listWidget_2 = ListWidget(self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(40, 330, 450, 170))
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_2.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget_2.customContextMenuRequested.connect(self.show_delete_menu)
        self.listWidget_2.installEventFilter(self)
        self.listWidget_2.setSelectionMode(QListWidget.MultiSelection)

        self.pushButton_close = QPushButton(self.centralwidget)
        self.pushButton_close.setGeometry(QtCore.QRect(20, 20, 15, 15))
        self.pushButton_close.setMinimumSize(QtCore.QSize(15, 15))
        self.pushButton_close.setMaximumSize(QtCore.QSize(15, 15))
        self.pushButton_close.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_close.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_close.setStyleSheet(
            "QPushButton{background:#F76677;border-radius:7px;}\n"
            "QPushButton:hover{background:red;}")
        self.pushButton_close.setText("")
        self.pushButton_close.setObjectName("pushButton_close")

        self.pushButton_maximize = QPushButton(self.centralwidget)
        self.pushButton_maximize.setGeometry(QtCore.QRect(40, 20, 15, 15))
        self.pushButton_maximize.setMinimumSize(QtCore.QSize(15, 15))
        self.pushButton_maximize.setMaximumSize(QtCore.QSize(15, 15))
        self.pushButton_maximize.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_maximize.setStyleSheet(
            "QPushButton{background:#F7D674;border-radius:7px;}\n"
            "QPushButton:hover{background:yellow;}")
        self.pushButton_maximize.setText("")
        self.pushButton_maximize.setObjectName("pushButton_maximize")
        self.pushButton_maximize.setEnabled(False)

        self.pushButton_minimize = QPushButton(self.centralwidget)
        self.pushButton_minimize.setGeometry(QtCore.QRect(60, 20, 15, 15))
        self.pushButton_minimize.setMinimumSize(QtCore.QSize(15, 15))
        self.pushButton_minimize.setMaximumSize(QtCore.QSize(15, 15))
        self.pushButton_minimize.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_minimize.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_minimize.setStyleSheet(
            "QPushButton{background:#6DDF6D;border-radius:7px;}\n"
            "QPushButton:hover{background:green;}")
        self.pushButton_minimize.setText("")
        self.pushButton_minimize.setObjectName("pushButton_minimize")

        self.pushButton.clicked.connect(self.choose_folder)
        self.pushButton_2.clicked.connect(self.confirm_folder)
        self.pushButton_3.clicked.connect(self.add_to_list)
        self.pushButton_4.clicked.connect(self.start)
        self.pushButton_5.clicked.connect(self.clear_data)
        self.pushButton_6.clicked.connect(self.export_data)
        self.pushButton_7.clicked.connect(self.about_dialog)
        self.lineEdit.textChanged.connect(self.folder_changed)
        self.lineEdit.returnPressed.connect(self.path_enter_pressed)
        self.lineEdit_2.returnPressed.connect(self.url_enter_pressed)
        self.checkBox_3.clicked.connect(self.list_enable)
        self.checkBox_2.clicked.connect(self.auto_download_enable)
        self.checkBox.clicked.connect(self.open_folder)
        self.pushButton_close.clicked.connect(self.Close_Window)
        self.pushButton_minimize.clicked.connect(self.showMinimized)
        self.comboBox.currentIndexChanged.connect(self.combobox_changed)

        if self.list_enable_value == 0:
            self.pushButton_3.setEnabled(False)
            self.checkBox_3.setChecked(False)
            self.checkBox_2.setChecked(False)
            self.checkBox_2.setEnabled(False)
            self.checkBox.setEnabled(True)
            self.listWidget_2.addItem('队列已停用')
            self.listWidget_2.setEnabled(False)
            if self.open_folder_value == 0:
                self.checkBox.setChecked(False)
            else:
                self.checkBox.setChecked(True)
        else:
            self.pushButton_3.setEnabled(True)
            self.listWidget_2.setEnabled(True)
            self.checkBox_3.setChecked(True)
            self.checkBox_2.setEnabled(True)
            if self.auto_download_enable_value == 0:
                self.checkBox_2.setChecked(False)
                self.checkBox.setEnabled(True)
                if self.open_folder_value == 0:
                    self.checkBox.setChecked(False)
                else:
                    self.checkBox.setChecked(True)
            else:
                self.checkBox_2.setChecked(True)
                self.checkBox.setChecked(False)
                self.checkBox.setEnabled(False)
                self.pushButton_4.setEnabled(False)

        self.download_manage_thread = download_manager_func()
        self.download_manage_thread.auto_download_signal.connect(self.auto_download_slot)
        self.download_manage_thread.list_download_signal.connect(self.list_download_slot)
        self.download_manage_thread.single_download_signal.connect(self.single_download_slot)
        self.download_manage_thread.send_warning_signal.connect(self.warning_slot)
        self.download_manage_thread.send_error_signal.connect(self.error_slot)
        self.download_manage_thread.send_ID_A_warning_signal.connect(self.ID_A_warning_slot)
        self.download_manage_thread.send_single_download_finish.connect(self.single_download_finish_slot)
        self.download_manage_thread.send_all_download_finish.connect(self.all_download_finish_slot)
        self.download_manage_thread.send_update_listwidget_signal_frommanager.connect(self.update_listwidget_slot)
        self.download_manage_thread.auto_download_enable_value = self.auto_download_enable_value

        if self.auto_download_enable_value == 0:
            self.download_manage_thread.keep = False
        elif self.auto_download_enable_value == 1:
            self.download_manage_thread.keep = True
            while not os.path.exists(self.folder):
                self.path_wrong_warning_dialog()
        self.download_manage_thread.list_enable_value = self.list_enable_value
        self.download_manage_thread.start()

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self._translate = QtCore.QCoreApplication.translate

        self.lineEdit.setPlaceholderText(self._translate("MainWindow", "输入保存教材的文件夹的路径"))
        self.lineEdit_2.setPlaceholderText(self._translate("MainWindow", "输入教材的网址"))
        self.pushButton.setText(self._translate("MainWindow", "..."))
        self.pushButton_2.setText(self._translate("MainWindow", "OK"))
        self.pushButton_3.setText(self._translate("MainWindow", "添加到队列"))

        if self.list_enable_value == 0:
            self.pushButton_4.setText(self._translate("MainWindow", "开始下载"))
            self.pushButton_3.setEnabled(False)
        else:
            self.pushButton_4.setText(self._translate("MainWindow", "开始队列"))
            self.pushButton_3.setEnabled(True)

        self.checkBox.setText(self._translate("MainWindow", "完成当前队列后打开文件夹"))
        self.checkBox_2.setText(self._translate("MainWindow", "自动下载队列内容"))
        self.checkBox_3.setText(self._translate("MainWindow", "启用队列"))
        self.label.setText(self._translate("MainWindow", "当出现同名文件时:"))
        self.label_2.setText(self._translate("MainWindow", "请务必完成下列设置后再下载:"))
        self.pushButton_5.setText(self._translate("MainWindow", "清空下载日志"))
        self.pushButton_6.setText(self._translate("MainWindow", "导出下载日志"))
        self.pushButton_7.setText(self._translate("MainWindow", "关于此软件"))
        self.comboBox.setItemText(0, self._translate("MainWindow", "覆盖"))
        self.comboBox.setItemText(1, self._translate("MainWindow", "添加数字后缀"))
        self.comboBox.setItemText(2, self._translate("MainWindow", "添加时间后缀"))
        self.comboBox.setCurrentIndex(self.save_mode)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_flag = True
            self.mouse_Position = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.mouse_flag:
            self.move(QMouseEvent.globalPos() - self.mouse_Position)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.mouse_flag = False

    def welcome_dialog(self):
        if self.first_open == 1:
            title = '欢迎使用 Teaching Material Download Manager'
            content = """请认真阅读以下内容, 如果您不同意以下任意内容, 请立即退出本软件:\n\n 1.本软件使用GPLv3许可证, 请根据GPLv3许可证正确行使您拥有的关于\n    本软件的权力以及您应履行的义务, 您可以点击“关于此软件”并在弹出
    的窗口中阅读 GPLv3 的原文。\n\n 2.请尊重教材编者和作者的劳动果实, 在中华人民共和国的法律范围内\n    使用本软件及电子教材。"""
            w = Dialog(title, content, self)
            w.yesButton.setText('同意')
            w.cancelButton.setText('不同意')
            if w.exec():
                self.first_open = 0
                self.config['first_open'] = self.first_open
                self.save_config()
            else:
                QCoreApplication.quit()
                sys.exit()

    def Close_Window(self):
        title = '是否退出软件'
        content = """请确认所有下载任务已完成, 否则可能会导致下载失败!!!"""
        w = Dialog(title, content, self)
        if w.exec():
            QCoreApplication.quit()
            sys.exit()
        else:
            pass

    def url_enter_pressed(self):
        if self.list_enable_value == 0:
            self.start()
        else:
            self.add_to_list()

    def set_enable(self, state):
        if state:
            if self.list_enable_value == 1:
                self.pushButton_3.setEnabled(True)
            self.lineEdit.setEnabled(True)
            self.pushButton.setEnabled(True)
            self.confirm_folder()
            self.pushButton_4.setEnabled(True)
            self.comboBox.setEnabled(True)
            self.lineEdit_2.setEnabled(True)
            self.checkBox_3.setEnabled(True)
            if self.list_enable_value == 0:
                self.checkBox_2.setEnabled(False)
            else:
                self.checkBox_2.setEnabled(True)
            if self.auto_download_enable_value == 0:
                self.checkBox.setEnabled(True)
                self.pushButton_4.setEnabled(True)
                self.delete_menu_enable = True
            else:
                self.checkBox.setEnabled(False)
                self.pushButton_4.setEnabled(False)
                self.delete_menu_enable = False
        else:
            self.pushButton.setEnabled(False)
            self.confirm_folder()
            self.pushButton_4.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            self.comboBox.setEnabled(False)
            self.checkBox_2.setEnabled(False)
            self.lineEdit_2.setEnabled(False)
            self.checkBox_3.setEnabled(False)
            self.checkBox.setEnabled(False)
            self.lineEdit.setEnabled(False)

    def path_enter_pressed(self):
        self.confirm_folder()

    def warning_slot(self):
        self.warning = 1

    def error_slot(self):
        self.error = 1

    def ID_A_warning_slot(self):
        self.ID_A_warning = 1

    def folder_changed(self):
        self.pushButton_2.setEnabled(True)

    def save_config(self):
        with open('config.json', 'w') as f:
            json.dump(self.config, f)

    def choose_folder(self):
        chosen_fold = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹",
                                                                 os.path.expanduser('~') + '\\document')
        if chosen_fold:
            if os.path.isdir(chosen_fold):
                if not chosen_fold.endswith('\\'):
                    self.folder = chosen_fold + '\\'
                self.config['folder'] = self.folder
                self.save_config()
                self.lineEdit.setText(self.folder)
                self.pushButton_2.setEnabled(False)

    def confirm_folder(self):
        if os.path.isdir(self.lineEdit.text()):
            if not self.folder.endswith('\\'):
                self.folder = self.lineEdit.text() + '\\'
            self.config['folder'] = self.folder
            self.save_config()
            self.pushButton_2.setEnabled(False)
        else:
            self.pushButton_2.setEnabled(True)
            self.path_wrong_warning_dialog()

    def list_enable(self, state):
        if self.checkBox_3.isChecked():
            self.listWidget_2.clear()
            self.listWidget_2.setEnabled(True)
            self.pushButton_4.setText(self._translate("MainWindow", "开始队列"))
            self.pushButton_3.setEnabled(True)
            self.list_enable_value = 1
            self.config['list_enable_value'] = self.list_enable_value
            self.download_manage_thread.list_enable_value = self.list_enable_value
            self.save_config()
            self.checkBox_2.setEnabled(True)
            if self.checkBox_2.isChecked():
                self.auto_download_enable_value = 1
                self.config['auto_download_enable_value'] = self.auto_download_enable_value
                self.download_manage_thread.auto_download_enable_value = self.auto_download_enable_value
                self.download_manage_thread.keep = True
                while not os.path.exists(self.folder):
                    self.path_wrong_warning_dialog()
                self.download_manage_thread.start()
                self.save_config()
                self.pushButton_4.setEnabled(False)
            else:
                self.auto_download_enable_value = 0
                self.config['auto_download_enable_value'] = self.auto_download_enable_value
                self.download_manage_thread.auto_download_enable_value = self.auto_download_enable_value
                self.download_manage_thread.keep = False
                self.save_config()
                self.pushButton_4.setEnabled(True)
        else:
            self.list_delete_dialog()

    def path_wrong_warning_dialog(self):
        title = '当前路径不可用'
        content = """点击下方OK按钮后在弹出的窗口中浏览并选择文件夹"""
        w = Dialog(title, content, self)
        if w.exec():
            self.choose_folder()
        else:
            pass

    def url_empty_warning_dialog(self):
        title = '网址不能为空'
        content = """请在输入框中正确输入网址"""
        w = Dialog(title, content, self)
        w.cancelButton.setVisible(False)
        if w.exec():
            pass

    def list_delete_dialog(self):
        title = '确定要停用队列吗？'
        content = """队列中未完成的下载任务都将被删除"""
        w = Dialog(title, content, self)
        if w.exec():
            self.list_enable_value = 0
            self.config['list_enable_value'] = self.list_enable_value
            self.download_manage_thread.list_enable_value = self.list_enable_value
            self.save_config()
            self.pushButton_3.setEnabled(False)
            self.listWidget_2.clear()
            self.list = []
            self.listWidget_2.addItem('队列已被停用')
            self.listWidget_2.setEnabled(False)
            self.checkBox_2.setChecked(False)
            self.checkBox_2.setEnabled(False)
            self.checkBox.setEnabled(True)
            self.auto_download_enable_value = 0
            self.config['auto_download_enable_value'] = self.auto_download_enable_value
            self.download_manage_thread.auto_download_enable_value = self.auto_download_enable_value
            self.download_manage_thread.keep = False
            self.save_config()
            self.pushButton_4.setEnabled(True)
            self.pushButton_4.setText(self._translate("MainWindow", "开始下载"))
        else:
            self.checkBox_3.setChecked(True)

    def auto_download_enable(self, state):
        if self.checkBox_2.isChecked():
            self.pushButton_4.setText(self._translate("MainWindow", "开始队列"))
            self.pushButton_4.setEnabled(False)
            self.auto_download_enable_value = 1
            self.config['auto_download_enable_value'] = self.auto_download_enable_value
            self.download_manage_thread.auto_download_enable_value = self.auto_download_enable_value
            self.download_manage_thread.keep = True
            while not os.path.exists(self.folder):
                self.path_wrong_warning_dialog()
            self.download_manage_thread.start()
            self.save_config()
            self.checkBox.setChecked(False)
            self.checkBox.setEnabled(False)
            self.open_folder_value = 0
            self.config['open_folder_value'] = self.open_folder_value
            self.save_config()
        else:
            self.pushButton_4.setEnabled(True)
            self.auto_download_enable_value = 0
            self.config['auto_download_enable_value'] = self.auto_download_enable_value
            self.download_manage_thread.auto_download_enable_value = self.auto_download_enable_value
            self.download_manage_thread.keep = False
            self.save_config()
            self.checkBox.setEnabled(True)
            self.open_folder_value = 0
            self.config['open_folder_value'] = self.open_folder_value
            self.save_config()

    def open_folder(self, state):
        if self.checkBox.isChecked():
            self.open_folder_value = 1
            self.config['open_folder_value'] = self.open_folder_value
            self.save_config()
        else:
            self.open_folder_value = 0
            self.config['open_folder_value'] = self.open_folder_value
            self.save_config()

    def about_dialog(self):
        self.about_window = AboutWindow()
        self.about_window.setupUi(QWidget)
        self.about_window.show()

    def add_to_list(self):
        if self.lineEdit_2.text() != '':
            self.list.append(self.lineEdit_2.text())
            self.listWidget_2.addItem(self.lineEdit_2.text())
            self.lineEdit_2.clear()
            if self.auto_download_enable_value == 1:
                self.download_manage_thread.start_download = True
        else:
            self.url_empty_warning_dialog()

    def start(self):
        if self.list_enable_value == 0:
            if self.lineEdit_2.text() == '':
                self.url_empty_warning_dialog()
                return None
        else:
            if len(self.list) == 0:
                return None
        self.download_manage_thread.manual = True
        while not os.path.exists(self.folder):
            self.path_wrong_warning_dialog()
        self.download_manage_thread.start()
        self.set_enable(False)

    def auto_download_slot(self):
        global textbook_file
        self.download_manage_thread.url_list = self.list
        self.download_manage_thread.save_mode = self.save_mode
        self.download_manage_thread.save_path = self.folder
        self.lineEdit_2.clear()
        self.download_manage_thread.setting_finished = True
        self.set_enable(True)

    def single_download_slot(self):
        global textbook_file
        self.download_manage_thread.save_mode = self.save_mode
        self.download_manage_thread.save_path = self.folder
        self.download_manage_thread.url = self.lineEdit_2.text()
        self.lineEdit_2.clear()
        self.download_manage_thread.setting_finished = True

    def list_download_slot(self):
        global textbook_file
        self.download_manage_thread.url_list = self.list
        self.download_manage_thread.save_mode = self.save_mode
        self.download_manage_thread.save_path = self.folder
        self.lineEdit_2.clear()
        self.download_manage_thread.setting_finished = True

    def all_download_finish_slot(self):
        self.set_enable(True)
        if self.open_folder_value != 0:
            os.startfile(self.folder)
        if self.list_enable_value == 1:
            if self.auto_download_enable_value == 0:
                title = '已完成当前所有下载任务'
                content = """已完成列表中的所有下载任务"""
                w = Dialog(title, content, self)
                w.cancelButton.setVisible(False)
                if w.exec():
                    pass
        else:
            title = '已完成当前下载任务'
            content = """已完成本次下载任务"""
            w = Dialog(title, content, self)
            w.cancelButton.setVisible(False)
            if w.exec():
                pass

    def single_download_finish_slot(self, url):
        global textbook_file
        if self.list_enable_value == 1:
            if len(self.list) != 0:
                self.list.pop(0)
                item = self.listWidget_2.takeItem(0)
                del item
        if self.auto_download_enable_value == 1:
            if len(self.list) == 0:
                self.download_manage_thread.start_download = False
        if self.ID_A_warning == 1:
            self.ID_A_WARNING_info(url)
            self.ID_A_warning = 0
        elif self.warning == 1:
            self.warning_info(url)
            self.warning = 0
        elif self.error == 1:
            self.error_info(url)
            self.error = 0
        else:
            self.successful_info(url)

    def successful_info(self, url):
        InfoBar.success(
            title='下载成功',
            content="已成功下载:" + url,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_LEFT,
            duration=18000,
            parent=self
        )

    def ID_A_WARNING_info(self, url):
        InfoBar.error(
            title='网址错误',
            content="无法下载:" + url + "请输入正确的网址后再试一次",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_LEFT,
            duration=20000,
            parent=self
        )

    def error_info(self, url):
        InfoBar.error(
            title='下载失败',
            content="无法下载:" + url + "建议检查网络连接, 并在试一次, 若你想支持本软件的开发, 请导出下载日志并将其发送到 ricardojackmc@gmail.com",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_LEFT,
            duration=20000,
            parent=self
        )

    def warning_info(self, url):
        InfoBar.warning(
            title='出现了一些问题',
            content="下载" + url + "时出现了一些问题, 但是如你所见, 文件应该已经成功保存到此电脑, 若你想支持本软件的开发, 请导出下载日志并将其发送到 ricardojackmc@gmail.com",
            orient=Qt.Horizontal,
            isClosable=False,
            position=InfoBarPosition.TOP_LEFT,
            duration=20000,
            parent=self
        )

    def update_listwidget_slot(self, dictionary):
        global kill, data_dictionary
        self.download_data.update(dictionary)
        self.listWidget.clear()
        for value in self.download_data.values():
            item = QListWidgetItem(value)
            self.listWidget.addItem(item)
            self.listWidget.setCurrentItem(item)
            self.listWidget.scrollToItem(item, QtWidgets.QAbstractItemView.PositionAtBottom)
        for value in dictionary.values():
            if value == 'finish':
                kill = 1
                self.download_manage_thread.infor_finish = True
                break

    def export_data(self):
        try:
            exported_data = QtWidgets.QFileDialog.getSaveFileName(self,
                                                                  "导出下载日志",
                                                                  os.path.expanduser('~') + '\\document\\',
                                                                  "JSON文件 (*.json)")
            with open(exported_data[0], 'w') as f:
                json.dump(self.download_data, f)
        except:
            pass

    def clear_data(self):
        self.download_data = {}
        self.listWidget.clear()

    def combobox_changed(self, index):
        self.save_mode = index
        self.config['save_mode'] = self.save_mode
        self.save_config()

    def delete_item(self):
        selected_items = self.listWidget_2.selectedItems()
        if selected_items:
            title = '是否删除选中项'
            content = '此操作不可逆'
            w = Dialog(title, content, self)
            if w.exec():
                for item in selected_items:
                    row = self.listWidget_2.row(item)
                    self.listWidget_2.takeItem(row)
                    self.list.pop(row)
            else:
                pass
            self.listWidget_2.clearSelection()

    def eventFilter(self, source, event):
        if source == self.listWidget_2 and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Delete:
                self.delete_item()
                return True
        return super().eventFilter(source, event)

    def show_delete_menu(self, pos):
        global_pos = self.listWidget_2.mapToGlobal(pos)
        menu = RoundMenu(parent=self.centralwidget)
        menu.setEnabled(self.delete_menu_enable)
        delete = Action(FluentIcon.DELETE, '删除所选项')
        delete.triggered.connect(self.delete_item)
        menu.addAction(delete)
        menu.exec(global_pos, aniType=MenuAnimationType.DROP_DOWN)

    def get_windows_theme_color(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\DWM")
            value, type = winreg.QueryValueEx(key, "AccentColor")
            winreg.CloseKey(key)
            if type == winreg.REG_DWORD:
                r = value % 256
                g = (value >> 8) % 256
                b = (value >> 16) % 256
                theme_color = [r, g, b]
            else:
                theme_color = None
        except:
            theme_color = None
        return theme_color

    def set_DISPLAY_MODE(self):
        global DISPLAY_MODE
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                value_name = "AppsUseLightTheme"
                value, _ = winreg.QueryValueEx(key, value_name)
                DISPLAY_MODE = value
        except:
            DISPLAY_MODE = 1
