from OpenGL.GL import *
import numpy as np

class Mesh:
    def __init__(self, vertices, indices):
        self.vertices = np.array(vertices, dtype=np.float32)
        self.indices = np.array(indices, dtype=np.uint32)

    def draw(self):
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vertices)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, self.indices)
        glDisableClientState(GL_VERTEX_ARRAY)

def load_obj(filepath):
    vertices = []
    indices = []

    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith('v '):
                parts = line.strip().split()
                vertices.extend([float(parts[1]), float(parts[2]), float(parts[3])])
            elif line.startswith('f '):
                parts = line.strip().split()
                face = [int(p.split('/')[0]) - 1 for p in parts[1:]]
                if len(face) == 3:
                    indices.extend(face)
                elif len(face) == 4:
                    indices.extend([face[0], face[1], face[2], face[0], face[2], face[3]])

    return Mesh(vertices, indices)
