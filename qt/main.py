import sys
import os

import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtWidgets


class Folder():
    def __init__(self, path):
        self.path__ = path

    def path(self):
        return self.path__

    def entry_names(self):
        return os.listdir(self.path__)


class FolderWindow(PyQt5.QtWidgets.QWidget):
    def __init__(self, folder, parent=None):
        super().__init__(parent)
        self.folder = folder

        self.setWindowTitle(folder.path())
        self.setGeometry(300, 50, 400, 350)
        # Without setting the flags, the window is not shown...
        self.setWindowFlags(PyQt5.QtCore.Qt.Window)

        self.box = PyQt5.QtWidgets.QVBoxLayout(self)
        for name in self.folder.entry_names():
            label = PyQt5.QtWidgets.QLabel(self)
            label.setText(name)
            label.adjustSize()
            self.box.addWidget(label)


class MainWindow(PyQt5.QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(300, 50, 400, 350)
        self.setWindowTitle('mg')

        self.btn = PyQt5.QtWidgets.QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.show_dialog)

        self.home_directory = os.path.expanduser('~')

    def show_dialog(self):
        path = PyQt5.QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Open directory', self.home_directory)

        if path:
            self.folder_window = FolderWindow(
                folder=Folder(path),
                parent=self)
            self.folder_window.show()


def main():
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    wnd = MainWindow()
    wnd.show()

    sys.exit(app.exec_())
    PyQt5.QtWidgets.QApplication.closeAllWindows()


if __name__ == '__main__':
    main()
