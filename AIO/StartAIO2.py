import os.path
import sys
from concurrent.futures import ThreadPoolExecutor


from PyQt5.QtCore import QTimer, Qt, QUrl, QDir, QTime, QObject, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QDesktopServices
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QHeaderView, QMessageBox, QFileDialog, \
    QStatusBar, QMenu, QAction, QLCDNumber

import aio


from jfunction import checkUtils, compressUtils, folderUtils



class WorkerThread(QThread):
    finished = pyqtSignal()

    def __init__(self, function, *args, **kwargs):
        super().__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.function(*self.args, **self.kwargs)
        self.finished.emit()

class MyWindow(aio.Ui_MainWindow):

    def write_console(self, text):
        font = QFont("微软雅黑", 12)  # 设置字体为Arial，大小为12
        self.textEdit.setFont(font)
        self.textEdit.moveCursor(self.textEdit.textCursor().End)  # 将光标移到末尾
        self.textEdit.insertPlainText(text)  # 插入文本

    def __init__(self):
        self.current_path = None
        self.model = None
        self.executor = ThreadPoolExecutor(5)
        self.worker_thread = WorkerThread(function=None)  # 为了避免初始化时报错，先设置一个空的函数

    def onTreeViewClicked(self, index):
        self.expandAndCollapse(index)
        self.resizeTreeViewColumns()
        selected_path = self.model.filePath(index)
        print(f"selected path: {selected_path}")
        if self.model.isDir(index):
            self.current_path = selected_path
            self.updateTableView()

        if checkUtils.is_svf_exist(selected_path):
            self.pushButton_7.setEnabled(True)
        else:
            self.pushButton_7.setEnabled(False)

        selected_index = self.treeView.selectionModel().currentIndex()
        selected_file_path = self.model.filePath(selected_index)
        self.lineEdit.setText(f"当前路径：{selected_file_path}")

        self.setStatusBarMessage(os.path.basename(selected_path))


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

        MainWindow.resize(1200, 600)
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
        # self.tableView.verticalHeader().setDefaultAlignment(Qt.AlignHCenter)
        # self.tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        # self.tableView.verticalHeader().setDefaultSectionSize(20)  # height 为行高度
        # self.layout.addWidget(self.table_view)

        # 设置状态栏
        self.statusBar = QStatusBar()
        MainWindow.setStatusBar(self.statusBar)

        # # 创建选择路径按钮和标签
        # self.select_button = QPushButton("选择路径")
        # self.select_button.clicked.connect(self.select_path)
        # self.path_label = QLabel("当前路径：")

        self.pushButton_4.clicked.connect(lambda: self.call_function_confirm(folderUtils.sub2main_clear))
        self.pushButton_6.clicked.connect(lambda: self.call_function_confirm(checkUtils.calculate_crc32_in_folder_mu))
        self.pushButton.clicked.connect(lambda: self.call_function_confirm(checkUtils.check_broken_images_in_folder_mu))
        self.pushButton_3.clicked.connect(lambda: self.callfunctionWithoutSelect(compressUtils.png2webpV1))
        self.pushButton_5.clicked.connect(lambda: self.call_function_confirm(folderUtils.delBlankDir))
        self.pushButton_7.clicked.connect(lambda: self.call_function_no_confirm(checkUtils.open_current_sfv))

        self.lcdNumber.setDigitCount(8)  # 设置显示的位数为 8 位
        self.lcdNumber.setSegmentStyle(QLCDNumber.Filled)  # 设置填充样式
        self.lcdNumber.timer = QTimer(self.lcdNumber)  # 创建一个定时器
        self.lcdNumber.timer.timeout.connect(self.showTime)  # 定时器超时时连接到显示时间的槽函数
        self.lcdNumber.timer.start(1000)  # 设置定时器间隔为 1000 毫秒（1 秒）

        self.treeView.customContextMenuRequested.connect(self.showContextMenu)
        self.createContextMenu()

        # 设置双击事件连接
        self.tableView.doubleClicked.connect(self.on_double_click)

    def showTime(self):
        time = QTime.currentTime()  # 获取当前时间
        text = time.toString('hh:mm:ss')  # 格式化时间为字符串
        self.lcdNumber.display(text)  # 在 QLCDNumber 上显示时间

    def on_double_click(self, index):
        # 双击打开的处理方法
        file_path = self.model.filePath(index)
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
        sourcedir = QFileDialog.getExistingDirectory(MainWindow, "选择源文件夹")
        outputdir = QFileDialog.getExistingDirectory(MainWindow, '选择输出文件夹')
        print(f"sourcedir: {sourcedir}")
        print(f"outputdir: {outputdir}")

        if len(sourcedir) == 0 or len(outputdir) == 0:
            print(f"文件夹地址为空")
        else:
            function(sourcedir, outputdir)
            # self.executor.submit(function, sourcedir, outputdir)
            self.worker_thread = WorkerThread(function, sourcedir, outputdir)
            self.worker_thread.finished.connect(self.on_thread_finished)
            self.worker_thread.start()



    def call_function_no_confirm(self, function):

        selected_index = self.treeView.selectionModel().currentIndex()
        selected_file_path = self.model.filePath(selected_index)
        self.setStatusBarMessage("Calling function")
        if os.path.isdir(selected_file_path):
            msg = f"selected directory: {selected_file_path}"
            print(msg)
            print('Proceeding...')
            self.worker_thread = WorkerThread(function, selected_file_path)
            self.worker_thread.finished.connect(self.on_thread_finished)
            self.worker_thread.start()
            # self.executor.submit(function, selected_file_path)
        else:
            print(f"{selected_file_path} is not a directory")

    def call_function_confirm(self, function):
        # Modify to use worker thread...
        # Example:
        selected_index = self.treeView.selectionModel().currentIndex()
        selected_file_path = self.model.filePath(selected_index)
        if os.path.isdir(selected_file_path):
            msg = f"selected directory: {selected_file_path}"
            print(msg)
            reply = QMessageBox.question(MainWindow, 'Confirmation', 'Are you sure to proceed ' + msg,
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                print('Proceeding...')
                self.worker_thread = WorkerThread(function, selected_file_path)
                self.worker_thread.finished.connect(self.on_thread_finished)
                self.worker_thread.start()
            else:
                print('Cancelled')
        else:
            print(f"{selected_file_path} is not a directory")

    # Add method to handle thread finished signal
    def on_thread_finished(self):
        print("Thread finished")



if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()

    ui = MyWindow()
    ui.setupUi(MainWindow)
    sys.stdout.write = ui.write_console
    MainWindow.show()
    # 示例输出
    print("JSH Toolkit")
    sys.exit(app.exec_())
