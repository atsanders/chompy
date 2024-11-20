from ui.slt_viewer_widget import Chomp_Viewer_Widget
from ui.chomp_test_widget import Chomp_Widget
from ui.stl_select_widget import Slt_Select_Widget
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget
import os


def main():
    os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"
    os.environ["QT_QPA_PLATFORM"] = "xcb"

    app = QApplication([])

    window = QWidget()
    layout = QVBoxLayout()

    chomp_widget = Chomp_Widget()
    stl_select_widget = Slt_Select_Widget()
    stl_viewer_widget = Chomp_Viewer_Widget()

    stl_select_widget.fileSelected.connect(chomp_widget.set_stl_file)
    stl_select_widget.fileSelected.connect(stl_viewer_widget.set_stl_file)

    stl_viewer_widget.setMinimumSize(400, 300)
    layout.addWidget(stl_select_widget)
    layout.addSpacing(25)
    layout.addWidget(stl_viewer_widget)
    layout.addWidget(chomp_widget)

    app.processEvents()

    layout.addStretch()

    window.setLayout(layout)
    window.setWindowTitle("Chompy Slicer")
    window.resize(800, 600)

    # stl_viewer_widget.update()

    window.show()

    app.exec()


if __name__ == "__main__":
    main()
