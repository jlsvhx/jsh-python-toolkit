import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QProgressBar
from PyQt5.QtCore import QTimer

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.startProgress)
        layout.addWidget(self.start_button)

        self.setLayout(layout)
        self.setWindowTitle('PyQt Progress Bar Example')

    def startProgress(self):
        self.progress = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateProgress)
        self.timer.start(100)  # 更新进度条的时间间隔（毫秒）

    def updateProgress(self):
        self.progress += 0.5
        self.progress_bar.setValue(self.progress)
        if self.progress >= 100:
            self.timer.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
