import os.path
import sys

from PyQt5.QtCore import QModelIndex, QTimer, Qt, QUrl, QDir
from PyQt5.QtGui import QFont, QDesktopServices
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QHeaderView, QMessageBox, QFileDialog, \
    QStatusBar, QMenu, QAction

import aio

from jshtoolkit.sub2main import main as sub2main
from jshtoolkit.checkFile import check_broken_images_in_folder_mu, calculate_crc32_in_folder_mu
from jshtoolkit.png2webpV1 import png2webpV1
from jshtoolkit.delblankdir import delBlankDir

class MyWindow(aio.Ui_MainWindow):

    def write_console(self, text):
        font = QFont("微软雅黑", 12)  # 设置字体为Arial，大小为12
        self.textEdit.setFont(font)
        self.textEdit.moveCursor(self.textEdit.textCursor().End)  # 将光标移到末尾
        self.textEdit.insertPlainText(text)  # 插入文本

    def __init__(self):
        self.current_path = None
        self.model = None

    def onTreeViewClicked(self, index):
        self.expandAndCollapse(index)
        self.resizeTreeViewColumns()
        selected_path = self.model.filePath(index)
        print(f"selected path: {selected_path}")
        if self.model.isDir(index):
            self.current_path = selected_path
            self.updateTableView()

        selected_index = self.treeView.selectionModel().currentIndex()
        selected_file_path = self.model.filePath(selected_index)
        self.lineEdit.setText(f"当前路径：{selected_file_path}")

    def expandAndCollapse(self, index):
        # 切换项的展开状态
        if self.treeView.isExpanded(index):
            self.treeView.collapse(index)
        else:
            self.treeView.expand(index)
            # 收起其他展开的项
            self.collapseOtherItems(index)

    def collapseOtherItems(self, index):
        # 获取当前项的父项
        parent = index.parent()

        # 遍历树视图的所有项
        for row in range(self.model.rowCount(parent)):
            # 获取当前项的子项索引
            child_index = self.model.index(row, 0, parent)

            # 如果不是当前项，且当前项处于展开状态，则收起它
            if child_index != index and self.treeView.isExpanded(child_index):
                self.treeView.collapse(child_index)

    def updateTableView(self):
        if self.current_path:
            self.model.setRootPath(self.current_path)
            self.tableView.setModel(self.model)
            self.tableView.setRootIndex(self.model.index(self.current_path))
            # 自适应列宽度
            QTimer.singleShot(0, self.resizeColumns)

    def resizeColumns(self):
        header = self.tableView.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

    def resizeTreeViewColumns(self):
        header = self.treeView.header()
        for i in range(self.model.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        MainWindow.resize(1920, 1080)
        # 创建文件系统模型
        self.model = QFileSystemModel()
        self.model.setRootPath("")  # 设置根路径为空，显示整个文件系统树
        # 允许显示隐藏文件夹
        self.model.setFilter(QDir.AllEntries | QDir.Hidden)


        # 创建树视图
        # 隐藏文件类型和日期等信息
        self.treeView.setRootIsDecorated(False)
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(""))  # 设置根索引为根路径的索引
        # 连接信号
        self.treeView.clicked.connect(self.onTreeViewClicked)
        # 禁用双击展开
        self.treeView.setExpandsOnDoubleClick(False)

        # 创建表视图
        # self.table_view = QTableView()
        self.tableView.setModel(self.model)
        # self.layout.addWidget(self.table_view)

        # 设置状态栏
        self.statusBar = QStatusBar()
        MainWindow.setStatusBar(self.statusBar)

        # # 创建选择路径按钮和标签
        # self.select_button = QPushButton("选择路径")
        # self.select_button.clicked.connect(self.select_path)
        # self.path_label = QLabel("当前路径：")

        self.pushButton_4.clicked.connect(lambda: self.callfunction(sub2main))
        self.pushButton_6.clicked.connect(lambda: self.callfunction(calculate_crc32_in_folder_mu))
        self.pushButton.clicked.connect(lambda: self.callfunction(check_broken_images_in_folder_mu))
        self.pushButton_3.clicked.connect(lambda: self.callfunctionWithoutSelect(png2webpV1))
        self.pushButton_5.clicked.connect(lambda: self.callfunction(delBlankDir))

        self.treeView.customContextMenuRequested.connect(self.showContextMenu)
        self.createContextMenu()

        # 设置双击事件连接
        self.tableView.doubleClicked.connect(self.on_double_click)

    def on_double_click(self, index):
        # 双击打开的处理方法
        file_path = self.model.filePath(index)
        if not self.model.isDir(index):  # 确保双击的是文件而不是文件夹
            print(f"Opening file: {file_path}")
            # 使用系统默认的程序打开文件
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))

    def createContextMenu(self):
        self.contextMenu = QMenu(MainWindow)
        self.action1 = QAction("选项1", MainWindow)
        self.action2 = QAction("选项2", MainWindow)

        self.contextMenu.addAction(self.action1)
        self.contextMenu.addAction(self.action2)

    def showContextMenu(self, position):
        # print("showContextMenu position", position)
        self.contextMenu.exec_(self.treeView.mapToGlobal(position))

    def setStatusBarMessage(self, message):
        # 更新状态栏消息
        self.statusBar.showMessage(message)

    def callfunctionWithoutSelect(self, function):
        self.setStatusBarMessage("Calling function start")

        sourcedir = QFileDialog.getExistingDirectory(MainWindow, "选择源文件夹")
        outputdir = QFileDialog.getExistingDirectory(MainWindow, '选择输出文件夹')

        if len(sourcedir) == 0 or len(outputdir) == 0:
            print(f"文件夹地址为空")
        else:
            function(sourcedir, outputdir)

        self.setStatusBarMessage("Calling function end")


    def callfunction(self, function):

        selected_index = self.treeView.selectionModel().currentIndex()
        selected_file_path = self.model.filePath(selected_index)
        if os.path.isdir(selected_file_path):
            msg = f"selected directory: {selected_file_path}"
            print(msg)
            reply = QMessageBox.question(MainWindow, 'Confirmation', 'Are you sure to proceed ' + msg,
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                print('Proceeding...')
                function(selected_file_path)
            else:
                print('Cancelled')
        else:
            print(f"{selected_file_path} is not a directory")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()

    ui = MyWindow()
    ui.setupUi(MainWindow)
    sys.stdout.write = ui.write_console
    MainWindow.show()
    # 示例输出
    print("Hello, this is a console output.")
    print("You can use this console to output messages.")
    sys.exit(app.exec_())
