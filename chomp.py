import stl_reader
import numpy as np

# import numpy.typing as npt


class StlReader(object):
    # def __init__(self):
    # self.vertices = npt.NDArray[np.float32]
    # self.faces = npt.NDArray[np.uint32]

    def read_stl_triangles(self, file_path):
        return stl_reader.read(file_path)
        # self._read_z_bounds(self.vertices)
        # self._adjust_z_bounds()


class Chomp(object):
    def __init__(self):
        self.LAYER_HEIGHT = 0.2
        self.adjusted_min_z = 0.0
        self.adjusted_max_z = 0.0
        self.orig_min_z = 0.0
        self.orig_max_z = 0.0
        self.calculated_layer_count = 0
        # storing these may be dumb, just sending it
        self.slices = []
        # self.vertices = npt.NDArray[np.float32]
        # self.faces = npt.NDArray[np.uint32]

    # def read_stl_triangles(self, file_path):
    #     self.vertices, self.indices = stl_reader.read(file_path)
    #     self._read_z_bounds(self.vertices)
    #     self._adjust_z_bounds()

    def chomp(self, file_path):
        stl_reader = StlReader()
        vertices, _ = stl_reader.read_stl_triangles(file_path)

        self._read_z_bounds(vertices)
        self._adjust_z_bounds()

        progress_max = self.adjusted_max_z - self.adjusted_min_z
        progress_threshold = 10
        progress = 0
        last_progress = 0.0

        print("Progress: 0%")

        z = self.adjusted_min_z
        while z <= self.adjusted_max_z:
            layer = self._compute_layer_contours(vertices, z)
            self.slices.append(layer)

            progress = (z - self.adjusted_min_z) / progress_max * 100
            p = int(progress)
            if p // progress_threshold * progress_threshold == p and p > last_progress:
                print(f"Progress: {int(progress)}%")
                last_progress = progress

            z += self.LAYER_HEIGHT

        print("Progress: 100%")

    def _compute_layer_contours(self, triangles, z):
        contours = []

        for triangle in triangles:
            intersection_points = []
            v0, v1, v2 = triangle
            z0, z1, z2 = v0, v1, v2

            for p1, p2, z_p1, z_p2 in [
                (v0, v1, z0, z1),
                (v1, v2, z1, z2),
                (v2, v0, z2, z0),
            ]:
                if (z_p1 <= z <= z_p2) or (z_p2 <= z <= z_p1):
                    # linear interpol to find intersect point on edge
                    # come back to this later
                    t = (z - z_p1) / (z_p2 - z_p1)
                    intersection = p1 + t * (p2 - p1)
                    intersection_points.append(intersection)

            if len(intersection_points) == 2:
                contours.append(np.array(intersection_points))
        return contours

    # TODO Z CAN BE +30, adjust the other way too
    # example max Z is 30, subtract that as offset
    def _adjust_z_bounds(self):
        offset = abs(self.orig_min_z)
        self.adjusted_min_z += self.LAYER_HEIGHT
        self.adjusted_max_z += self.LAYER_HEIGHT

        if self.orig_min_z < 0:
            self.calculated_layer_count = int(
                (offset + self.orig_max_z) / self.LAYER_HEIGHT
            )
        else:
            self.calculated_layer_count = int(
                (self.orig_max_z - offset) / self.LAYER_HEIGHT
            )
        self.adjusted_max_z = self.calculated_layer_count * self.LAYER_HEIGHT

    def _read_z_bounds(self, vertices_array):
        z_values = vertices_array[:, 2]
        self.orig_min_z = np.min(z_values)
        self.orig_max_z = np.max(z_values)
