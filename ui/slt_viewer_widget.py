from OpenGL.GLU import gluLookAt, gluPerspective
from OpenGL.GL import (
    glBegin,
    glEnd,
    glEnable,
    glClearColor,
    glMatrixMode,
    GL_PROJECTION,
    GL_DEPTH_TEST,
    glLoadIdentity,
    GL_MODELVIEW,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    glClear,
    GL_TRIANGLES,
    glVertex3fv,
    glColor3fv,
    glViewport,
    # GL_QUADS,
    glOrtho,
    glRotatef,
    glTranslatef,
)
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from chomp import StlReader
import numpy as np


class Chomp_Viewer_Widget(QOpenGLWidget):
    def __init__(self):
        super().__init__()

        self.selected_stl_file = ""

    def set_stl_file(self, stl_file):
        self.selected_stl_file = stl_file
        self.paintGL()

    def initializeGL(self):
        try:
            # black bg
            glClearColor(0.0, 0.0, 0.0, 1.0)
            print("OpenGL initialized successfully")
        except Exception as e:
            print(f"Error initializing OpenGL: {e}")

    def paintGL(self):
        if len(self.selected_stl_file) == 0:
            print("no file")
            return

        print("file found")

        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # gluPerspective(
        #     45, 800 / 600, 0.1, 50.0
        # )  # Field of view, aspect ratio, near, far
        gluPerspective(45.0, self.width() / self.height(), 0.1, 10000.0)
        glMatrixMode(GL_MODELVIEW)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        gluLookAt(
            0,
            0,
            -200,
            0,
            0,
            0,
            0,
            1,
            0,
        )

        glRotatef(45, 0, 1, 0)

        stl_reader = StlReader()
        vertices, indices = stl_reader.read_stl_triangles(self.selected_stl_file)
        # print("First 5 vertices:", vertices[:5])
        # print("First 5 indices:", indices[:5])
        # min_vertex = np.min(vertices, axis=0)
        # max_vertex = np.max(vertices, axis=0)
        # print("Vertex min:", min_vertex)
        # print("Vertex max:", max_vertex)

        center = np.mean(vertices, axis=0)
        glTranslatef(-center[0], -center[1], -center[2])

        glBegin(GL_TRIANGLES)
        for face in indices:
            glColor3fv((1, 0, 0))
            for index in face:
                vertex = vertices[index]
                glVertex3fv(vertex)
        glEnd()

        # glBegin(GL_QUADS)
        # glColor3fv(colors[-1])
        # for vertex in faces[-1]:
        #     glVertex3fv(vertices[vertex])
        # glEnd()

    def resizeGL(self, w, h):
        print(f"resizeGL called with width={w}, height={h}")
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)

    def keyPressEvent(self, event):
        pass
        # vertices = [
        #     (0.0, 1.0, 0.0),  # Top point
        #     (-1.0, -1.0, -1.0),  # Front-left
        #     (1.0, -1.0, -1.0),  # Front-right
        #     (1.0, -1.0, 1.0),  # Back-right
        #     (-1.0, -1.0, 1.0),  # Back-left
        # ]

        # # Define the faces of the pyramid (each face is a triangle)
        # faces = [
        #     (0, 1, 2),  # Front face
        #     (0, 2, 3),  # Right face
        #     (0, 3, 4),  # Back face
        #     (0, 4, 1),  # Left face
        #     (1, 2, 3, 4),  # Base (quad)
        # ]
        # # Define the vertices of the pyramid

        # # Define colors for each face
        # colors = [
        #     (1.0, 0.0, 0.0),  # Red
        #     (0.0, 1.0, 0.0),  # Green
        #     (0.0, 0.0, 1.0),  # Blue
        #     (1.0, 1.0, 0.0),  # Yellow
        #     (0.5, 0.5, 0.5),  # Gray for the base
        # ]
