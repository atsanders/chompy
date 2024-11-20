
from PyQt6.QtWidgets import (QHBoxLayout, QVBoxLayout, QLabel, QFileDialog, QPushButton, QWidget, QSizePolicy)
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.opengl import GLViewWidget, GLGridItem
from PyQt6.QtCore import pyqtSignal
from pathlib import Path
from chomp import Chomp
import numpy as np

class Slt_Select_Widget(QWidget):
    fileSelected = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        stl_select_layout = QHBoxLayout(self)

        self.stl_select_btn = QPushButton('Select STL', self)
        self.stl_select_btn.clicked.connect(self.select_file_dialog)
        stl_select_layout.addWidget(self.stl_select_btn)

        self.stl_file_path_label = QLabel("Please select a file...", self)
        stl_select_layout.addWidget(self.stl_file_path_label)

        self.setLayout(stl_select_layout)

    def select_file_dialog(self):
        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir)
        selected_file_path = fname[0]

        if selected_file_path == None: 
            return
        if not selected_file_path.lower().endswith(".stl"):
            return

        self.fileSelected.emit(selected_file_path)
        self.stl_file_path_label.setText(selected_file_path)

class Chomp_Viewer_Wiget(QWidget):
    def __init__(self):
        super().__init__()

        # Create the GLViewWidget for 3D rendering
        self.gl_widget = GLViewWidget()
        self.gl_widget.setCameraPosition(distance=10)
        self.gl_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Create a grid and add it to the GLViewWidget
        grid = GLGridItem()
        self.gl_widget.addItem(grid)

        # Generate random 3D data (100 points in space)
        data = np.random.rand(100, 3) * 50  # Scale the points up to be larger

        # Create a scatter plot item with the generated data
        colors = np.ones([1000,4])*255
        colors[:,:-1] = np.random.rand(1000,3)
        scatter_plot = gl.GLScatterPlotItem(pos = data, color = colors, size = 30)  # Default color and size
        self.gl_widget.addItem(scatter_plot)

        # Adjust the camera to ensure the points are visible
        self.gl_widget.opts['distance'] = 100  # Set the camera distance to zoom out
        self.gl_widget.opts['elevation'] = 30  # Set the camera elevation angle
        self.gl_widget.opts['azimuth'] = 45    # Set the camera azimuth angle

        # Set the layout for the widget and add the GLViewWidget
        layout = QVBoxLayout(self)
        layout.addWidget(self.gl_widget)

        # Set the layout for the window
        self.setLayout(layout)

        self.resize(400, 600)


class Chomp_Widget(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_stl_file = ""
        chomp_layout = QVBoxLayout(self)

        self.stl_chomp_btn = QPushButton('Chomp!', self)
        self.stl_chomp_btn.setDisabled(True)
        chomp_layout.addWidget(self.stl_chomp_btn)

        self.triangle_min_z_label = QLabel("", self)
        chomp_layout.addWidget(self.triangle_min_z_label)
        self.triangle_max_z_label = QLabel("", self)
        chomp_layout.addWidget(self.triangle_max_z_label)
        self.calculated_layer_count = QLabel("", self)
        chomp_layout.addWidget(self.calculated_layer_count)


    def set_chomp_file(self, stl_file):
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
        chomp.read_stl_triangles(self.selected_stl_file)
        self.triangle_min_z_label.setText(f"Min Z: {chomp.orig_min_z} | Adj Z: {chomp.adjusted_min_z}")
        self.triangle_max_z_label.setText(f"Max Z: {chomp.orig_max_z} | Adj Z: {chomp.adjusted_max_z}")
        self.calculated_layer_count.setText(f"Calculated layer count: {chomp.calculated_layer_count}")
        