from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)
from chomp import Chomp


class Chomp_Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_stl_file = ""
        chomp_layout = QVBoxLayout(self)

        self.stl_chomp_btn = QPushButton("Chomp!", self)
        self.stl_chomp_btn.setDisabled(True)
        chomp_layout.addWidget(self.stl_chomp_btn)

        self.triangle_min_z_label = QLabel("", self)
        chomp_layout.addWidget(self.triangle_min_z_label)
        self.triangle_max_z_label = QLabel("", self)
        chomp_layout.addWidget(self.triangle_max_z_label)
        self.calculated_layer_count = QLabel("", self)
        chomp_layout.addWidget(self.calculated_layer_count)

    def set_stl_file(self, stl_file):
        self.selected_stl_file = stl_file
        self.enable()

    def enable(self):
        self.stl_chomp_btn.setEnabled(True)
        self.stl_chomp_btn.clicked.connect(self.chomp)

    def diable(self):
        self.stl_chomp_btn.setDisabled(True)

    def chomp(self):
        if self.selected_stl_file is None:
            return
        if self.selected_stl_file == "":
            return

        chomp = Chomp()
        # chomp.read_stl_triangles(self.selected_stl_file)

        chomp.chomp(self.selected_stl_file)
        self.triangle_min_z_label.setText(
            f"Min Z: {chomp.orig_min_z} | Adj Z: {chomp.adjusted_min_z}"
        )
        self.triangle_max_z_label.setText(
            f"Max Z: {chomp.orig_max_z} | Adj Z: {chomp.adjusted_max_z}"
        )
        self.calculated_layer_count.setText(
            f"Calculated layer count: {chomp.calculated_layer_count}"
        )
