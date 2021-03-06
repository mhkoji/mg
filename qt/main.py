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
        def sort_by_name_root(names):
            try:
                name2order = {}
                for name in names:
                    name_root = os.path.splitext(name)[0]
                    name2order[name] = int(name_root, 10)
                return sorted(names, key=lambda x: name2order[x])
            except ValueError:
                # Failed to convert name_root into into
                return None

        names = os.listdir(self.path__)
        names_ordered = sort_by_name_root(names) or names
        return [self.make_file(name) for name in names_ordered]

    def make_file(self, name):
        path = os.path.join(self.path(), name)
        if os.path.isdir(path):
            return Folder(path)
        else:
            return File(path)


class Slideshow(PyQt5.QtWidgets.QWidget):
    class Image():
        def __init__(self, pixmap, file):
            self.pixmap = pixmap
            self.file = file

    def __init__(self, files, parent=None):
        super().__init__(parent)
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

        self.image_list = []
        for file in files:
            pixmap = PyQt5.QtGui.QPixmap(file.path())
            if not pixmap.isNull():
                self.image_list.append(Slideshow.Image(pixmap, file))

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

    def show_image(self, image):
        self.label.setPixmap(image.pixmap)
        self.setWindowTitle(image.file.path())

    def next_image(self, is_forward):
        length = len(self.image_list)
        if length == 0:
            self.next_btn.setEnabled(False)
            self.prev_btn.setEnabled(False)
            return

        if self.index is None:
            self.index = 0
        else:
            diff = 1 if is_forward else -1
            self.index = (self.index + diff) % length

        self.show_image(self.image_list[self.index])


class MainWindow(PyQt5.QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(300, 50, 400, 350)
        self.setWindowTitle('mg')

        self.box = PyQt5.QtWidgets.QVBoxLayout(self)

        self.btn = PyQt5.QtWidgets.QPushButton('Dialog', self)
        self.btn.clicked.connect(self.show_dialog)
        self.box.addWidget(self.btn)

        self.slideshow_button = PyQt5.QtWidgets.QPushButton('Slideshow', self)
        self.box.addWidget(self.slideshow_button)

        self.folder_list_widget = PyQt5.QtWidgets.QListWidget(self)
        self.box.addWidget(self.folder_list_widget)

        self.image_list_widget = PyQt5.QtWidgets.QListWidget(self)
        self.box.addWidget(self.image_list_widget)

        self.home_directory = os.path.expanduser('~')

    def keyPressEvent(self, event):
        key = event.key()
        if key == PyQt5.Qt.Qt.Key_Escape:
            self.close()

    def show_dialog(self):
        path = PyQt5.QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Open directory', self.home_directory)
        if path:
            self.show_folder(Folder(path))

    def show_folder(self, folder):
        child_folder_list = []
        child_file_list = []
        for child in folder.files():
            if isinstance(child, Folder):
                child_folder_list.append(child)
            else:
                child_file_list.append(child)

        for folder in child_folder_list:
            for file in folder.files():
                pixmap = PyQt5.QtGui.QPixmap(file.path())
                if not pixmap.isNull():
                    icon = PyQt5.QtGui.QIcon(pixmap)
                    text = os.path.basename(folder.path())
                    item = PyQt5.QtWidgets.QListWidgetItem(icon, text)
                    item.folder = folder
                    self.folder_list_widget.addItem(item)
                    break

        self.folder_list_widget.itemClicked.connect(
            lambda item: self.show_folder(item.folder))

        for file in child_file_list:
            pixmap = PyQt5.QtGui.QPixmap(file.path())
            if not pixmap.isNull():
                icon = PyQt5.QtGui.QIcon(pixmap)
                text = os.path.basename(file.path())
                item = PyQt5.QtWidgets.QListWidgetItem(icon, text)
                self.image_list_widget.addItem(item)

        if 0 < len(folder.files()):
            self.slideshow_button.clicked.connect(
                lambda: Slideshow(
                    files=folder.files(), parent=self).show())

def main():
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    wnd = MainWindow()
    wnd.show()

    sys.exit(app.exec_())
    PyQt5.QtWidgets.QApplication.closeAllWindows()


if __name__ == '__main__':
    main()
