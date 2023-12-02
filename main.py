import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QAction, QMenu, QSystemTrayIcon
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt


class DesktopPet(QWidget):
    def __init__(self, parent=None):
        super(DesktopPet, self).__init__(parent)

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

        # 设置窗口位置
        self.move(300, 200)

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

        # 添加其他子菜单`
        otherMenu = contextMenu.addMenu('其他')
        otherAction1 = QAction('其他1', self)
        otherAction2 = QAction('其他2', self)
        otherMenu.addAction(otherAction1)
        otherMenu.addAction(otherAction2)

        # 添加退出选项
        exitAction = QAction('退出', self)
        exitAction.triggered.connect(self.close)
        contextMenu.addAction(exitAction)

        # 添加最小化窗口
        minimizeAction = QAction('最小化', self)
        minimizeAction.triggered.connect(self.minimizeWindow)
        contextMenu.addAction(minimizeAction)

        # 显示菜单
        contextMenu.exec_(self.mapToGlobal(position))

    def minimizeWindow(self):
        self.showMinimized()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    desktop_pet = DesktopPet()  # 创建桌面宠物
    sys.exit(app.exec_())  # 启动事件循环
