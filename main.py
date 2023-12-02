import sys
import os
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QAction, QMenu, QSystemTrayIcon
from PyQt5.QtGui import QPixmap, QCursor, QIcon
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QApplication, QDesktopWidget


class ExitConfirmDialog(QDialog):
    def __init__(self, parent=None):
        super(ExitConfirmDialog, self).__init__(parent)
        self.setWindowTitle('sure?')
        self.setGeometry(200, 200, 400, 400)  # 设置对话框大小
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()  # 设置垂直布局

        # 隐藏宠物按钮
        self.hideButton = QPushButton('隐藏宠物', self)
        self.hideButton.clicked.connect(self.onHideClicked)
        layout.addWidget(self.hideButton)

        # 退出程序按钮
        self.quitButton = QPushButton('退出程序', self)
        self.quitButton.clicked.connect(self.onQuitClicked)
        layout.addWidget(self.quitButton)

        self.setLayout(layout)

    def onHideClicked(self):
        self.parent().hidePet()  # 调用主窗体的隐藏方法
        self.accept()  # 关闭对话框

    def onQuitClicked(self):
        self.parent().quitApp()  # 调用主窗体的退出方法
        self.accept()  # 关闭对话框


class DesktopPet(QWidget):
    def __init__(self, parent=None):
        super(DesktopPet, self).__init__(parent)
        self.initPall()  # 启动托盘
        self.setRandomPosition()
        # 设置窗口无边框并保持在顶部
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)

        # 设置窗口透明度属性
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # 设置窗口大小
        self.resize(128, 128)

        # 创建并设置图片标签
        self.image_label = QLabel(self)
        self.image_label.resize(128, 128)
        self.setPetImage('pikachu/shime1.png')  # 假设你有一个128x128的宠物图片在这个路径

        # 设置窗口标题
        self.setWindowTitle('DeskTopPet')

        self.show()  # 显示窗口

    def setPetImage(self, image_path):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片文件'{image_path}'未找到。")

        # 加载图片并设置到标签
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)  # 图片按比例缩放以填满标签

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
        elif event.button() == Qt.RightButton:
            self.showContextMenu(event.pos())
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.dragPosition is not None:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    def setRandomPosition(self):
        # 获取屏幕尺寸
        screen = QDesktopWidget().screenGeometry()
        # 宠物尺寸
        size = self.geometry()
        # 可移动位置
        x_max = screen.width() - size.width()
        y_max = screen.height() - size.height()
        # 随机选择x和y坐标
        x = random.randint(0, x_max)
        y = random.randint(0, y_max)
        # 设置宠物的位置
        self.move(x, y)

    def initPall(self):
        # 初始化托盘设置退出和显示按钮

        showing = QAction('显示', self)
        showing.triggered.connect(self.showin)

        icons = os.path.join('icon.png')
        quit_action = QAction('退出', self)
        quit_action.triggered.connect(self.quitApp)
        quit_action.setIcon(QIcon(icons))
        # 右键菜单
        self.tray_icon_meun = QMenu(self)
        self.tray_icon_meun.addAction(quit_action)
        self.tray_icon_meun.addAction(showing)

        # 无关紧要的设计
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(icons))
        self.tray_icon.setContextMenu(self.tray_icon_meun)
        self.tray_icon.show()

    def showContextMenu(self, position):
        # 创建菜单
        contextMenu = QMenu(self)

        # 添加游戏子菜单
        gameMenu = contextMenu.addMenu('游戏')
        gameAction1 = QAction('游戏1', self)
        gameAction2 = QAction('游戏2', self)
        gameMenu.addAction(gameAction1)
        gameMenu.addAction(gameAction2)

        # 添加散步选项
        walkAction = QAction('散步', self)
        contextMenu.addAction(walkAction)

        # 添加其他子菜单
        otherMenu = contextMenu.addMenu('其他')
        otherAction1 = QAction('其他1', self)
        otherAction2 = QAction('其他2', self)
        otherMenu.addAction(otherAction1)
        otherMenu.addAction(otherAction2)

        # 添加隐藏选项
        hideAction = QAction('隐藏', self)
        hideAction.triggered.connect(self.hidePet)
        contextMenu.addAction(hideAction)

        # 添加退出选项
        exitAction = QAction('退出', self)
        exitAction.triggered.connect(self.quit)
        contextMenu.addAction(exitAction)

        # 显示菜单
        contextMenu.exec_(self.mapToGlobal(position))

    def quit(self):
        dialog = ExitConfirmDialog(self)
        res = dialog.exec_()  # 显示对话框并等待用户操作
        if res:  # 如果用户选择退出
            self.quitApp()  # 调用退出应用程序

    def quitApp(self):
        self.close()
        sys.exit()

    def showin(self):
        self.setWindowOpacity(1)

    def hidePet(self):
        self.setWindowOpacity(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    desktop_pet = DesktopPet()  # 创建桌面宠物
    sys.exit(app.exec_())  # 启动事件循环
