from pathlib import Path
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QFileDialog,
    QPushButton,
    QWidget,
)
from PyQt6.QtCore import pyqtSignal


class Slt_Select_Widget(QWidget):
    fileSelected = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        stl_select_layout = QHBoxLayout(self)

        self.stl_select_btn = QPushButton("Select STL", self)
        self.stl_select_btn.clicked.connect(self.select_file_dialog)
        stl_select_layout.addWidget(self.stl_select_btn)

        self.stl_file_path_label = QLabel("Please select a file...", self)
        stl_select_layout.addWidget(self.stl_file_path_label)

        self.setLayout(stl_select_layout)

    def select_file_dialog(self):
        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(self, "Open file", home_dir)
        selected_file_path = fname[0]

        if selected_file_path is None:
            return
        if not selected_file_path.lower().endswith(".stl"):
            return

        self.fileSelected.emit(selected_file_path)
        self.stl_file_path_label.setText(selected_file_path)
