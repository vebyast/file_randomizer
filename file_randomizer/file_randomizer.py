import pathlib
import random
import appdirs
import shelve
import sys

from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QFileDialog

user_data_dir = pathlib.Path(appdirs.user_data_dir('FileRandomizer', 'Vebyast'))
user_data_dir.mkdir(parents=True, exist_ok=True)

class FileRandomizerWidget(QtWidgets.QWidget):
    def __init__(self, user_data_shelve):
        super().__init__()

        self.user_data_shelve = user_data_shelve

        if 'target_directory' not in self.user_data_shelve:
            self.user_data_shelve['target_directory'] = None
        if 'picked_file' not in self.user_data_shelve:
            self.user_data_shelve['picked_file'] = None

        self.select_dir_button = QtWidgets.QPushButton("Select Directory")
        self.dir_label = QtWidgets.QLabel(self.user_data_shelve['target_directory'],
                                          alignment=QtCore.Qt.AlignRight)

        self.randomize_button = QtWidgets.QPushButton("Randomize File")
        self.file_label = QtWidgets.QLabel(self.user_data_shelve['picked_file'], alignment=QtCore.Qt.AlignRight)

        self.root_layout = QtWidgets.QVBoxLayout(self)

        self.dir_layout = QtWidgets.QHBoxLayout()
        self.root_layout.addLayout(self.dir_layout)
        self.dir_layout.addWidget(self.select_dir_button)
        self.dir_layout.addWidget(self.dir_label)
        
        self.file_layout = QtWidgets.QHBoxLayout()
        self.root_layout.addLayout(self.file_layout)
        self.file_layout.addWidget(self.randomize_button)
        self.file_layout.addWidget(self.file_label)

        self.select_dir_button.clicked.connect(self.choose_directory)
        self.randomize_button.clicked.connect(self.randomize_file)

    @QtCore.Slot()
    def choose_directory(self):
        self.user_data_shelve['target_directory'] = QFileDialog.getExistingDirectory()
        self.dir_label.setText(self.user_data_shelve['target_directory'])

    @QtCore.Slot()
    def randomize_file(self):
        d = pathlib.Path(self.user_data_shelve['target_directory'])
        files = [p for p in d.iterdir() if p.is_file()]
        self.user_data_shelve['picked_file'] = random.choice(files).name
        self.file_label.setText(self.user_data_shelve['picked_file'])

def main():
    with shelve.open(user_data_dir / 'settings') as user_data_shelve:
        app = QApplication(sys.argv)
        widget = FileRandomizerWidget(user_data_shelve)
        widget.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    main()
