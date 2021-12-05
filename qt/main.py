import sys
import os

import PyQt5.Qt
import PyQt5.QtCore
import PyQt5.QtGui
import PyQt5.QtWidgets


class File():
    def __init__(self, path):
        self.path__ = path

    def path(self):
        return self.path__

    def name(self):
        return os.path.basename(self.path__)


class Folder(File):
    def __init__(self, path):
        super().__init__(path)

    def files(self):
        return [self.make_file(name) for name in os.listdir(self.path__)]

    def make_file(self, name):
        path = os.path.join(self.path(), name)
        if os.path.isdir(path):
            return Folder(path)
        return File(path)


class FolderWindow(PyQt5.QtWidgets.QWidget):
    def __init__(self, folder, parent=None):
        super().__init__(parent)
        self.folder = folder

        self.setGeometry(300, 50, 400, 350)
        # Without setting the flags, the window is not shown...
        self.setWindowFlags(PyQt5.QtCore.Qt.Window)

        self.box = PyQt5.QtWidgets.QVBoxLayout(self)

        hbox = PyQt5.QtWidgets.QHBoxLayout(self)
        self.box.addLayout(hbox)
        self.prev_btn = PyQt5.QtWidgets.QPushButton('prev', self)
        self.prev_btn.clicked.connect(lambda: self.next_image(False))
        hbox.addWidget(self.prev_btn)
        self.next_btn = PyQt5.QtWidgets.QPushButton('next', self)
        self.next_btn.clicked.connect(lambda: self.next_image(True))
        hbox.addWidget(self.next_btn)

        self.label = PyQt5.QtWidgets.QLabel(self)
        self.box.addWidget(self.label)
        self.index = None
        self.next_image(None)

    def keyPressEvent(self, event):
        key = event.key()
        if key == PyQt5.Qt.Qt.Key_H or key == PyQt5.Qt.Qt.Key_K:
            self.next_image(False)
        elif key == PyQt5.Qt.Qt.Key_L or key == PyQt5.Qt.Qt.Key_J:
            self.next_image(True)
        elif key == PyQt5.Qt.Qt.Key_Escape:
            self.close()

    def show_image(self, file):
        pixmap = PyQt5.QtGui.QPixmap(file.path())
        if pixmap.isNull():
            return False
        self.label.setPixmap(pixmap)
        self.setWindowTitle(file.path())
        return True

    def next_image(self, is_forward):
        files = self.folder.files()
        length = len(files)
        indices = None
        if self.index is None:
            indices = range(0, length)
        elif is_forward:
            if self.index == length - 1:
                return
            indices = range(self.index + 1, length)
        else:
            # backward
            if self.index == 0:
                return
            indices = reversed(range(0, self.index))
        for index in indices:
            if self.show_image(files[index]):
                self.index = index
                self.next_btn.setEnabled(self.index != length - 1)
                self.prev_btn.setEnabled(self.index != 0)
                return


class MainWindow(PyQt5.QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(300, 50, 400, 350)
        self.setWindowTitle('mg')

        self.btn = PyQt5.QtWidgets.QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.show_dialog)

        self.home_directory = os.path.expanduser('~')

    def keyPressEvent(self, event):
        key = event.key()
        if key == PyQt5.Qt.Qt.Key_Escape:
            self.close()

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
