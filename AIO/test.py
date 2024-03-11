import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QFileSystemModel
from PyQt5.QtCore import QDir


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 600, 400)

        # 创建 QTreeView 和 QFileSystemModel
        self.treeView = QTreeView(self)
        self.model = QFileSystemModel(self)

        # 允许显示隐藏文件夹
        self.model.setFilter(QDir.AllEntries | QDir.Hidden)

        # 设置根路径为当前目录
        self.model.setRootPath(QDir.rootPath())

        # 获取目录列表
        rootIndex = self.model.index(QDir.rootPath())
        rowCount = self.model.rowCount(rootIndex)
        for i in range(rowCount):
            if self.model.fileName(rootIndex.child(i)) not in ['.', '..']:
                self.treeView.setModel(self.model)

        # 设置主窗口的中心部件
        self.setCentralWidget(self.treeView)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
