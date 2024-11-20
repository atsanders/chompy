from PyQt6.QtWidgets import QApplication
from landing import Slt_Select_Widget, Chomp_Widget, Chomp_Viewer_Wiget
from PyQt6.QtWidgets import (QApplication, QVBoxLayout, QWidget)

def main():
    import os
    os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"

    app = QApplication([])

    window = QWidget()
    layout = QVBoxLayout()

    chomp_widget = Chomp_Widget()
    stl_select_widget = Slt_Select_Widget()
    stl_viewer_widget = Chomp_Viewer_Wiget()

    stl_select_widget.fileSelected.connect(chomp_widget.set_chomp_file)
    stl_viewer_widget.setStyleSheet("border: 1px solid red;")
    layout.addWidget(stl_select_widget)
    layout.addSpacing(25)
    layout.addWidget(stl_viewer_widget)
    layout.addWidget(chomp_widget)

    app.processEvents()

    layout.addStretch()

    window.setLayout(layout)
    window.setWindowTitle('Chompy Slicer')
    #window.resize(400, 200)

    window.show()

    app.exec()

if __name__ == '__main__':
    main()