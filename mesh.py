from OpenGL.GL import *
import numpy as np

class Mesh:
    def __init__(self, vertices, indices, normals=None):
        self.vertices = np.array(vertices, dtype=np.float32)
        self.indices = np.array(indices, dtype=np.uint32)
        self.normals = np.array(normals, dtype=np.float32) if normals else None

    def draw(self):
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vertices)

        if self.normals is not None:
            glEnableClientState(GL_NORMAL_ARRAY)
            glNormalPointer(GL_FLOAT, 0, self.normals)

        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, self.indices)

        glDisableClientState(GL_VERTEX_ARRAY)
        if self.normals is not None:
            glDisableClientState(GL_NORMAL_ARRAY)

def load_obj(filepath):
    temp_vertices = []
    temp_normals = []
    vertex_indices = []
    normal_indices = []

    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith('v '):
                parts = line.strip().split()
                temp_vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif line.startswith('vn '):
                parts = line.strip().split()
                temp_normals.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif line.startswith('f '):
                parts = line.strip().split()[1:]
                for part in parts:
                    vals = part.split('//') if '//' in part else part.split('/')
                    v_idx = int(vals[0]) - 1
                    n_idx = int(vals[-1]) - 1 if len(vals) > 1 and len(temp_normals) > 0 else None
                    vertex_indices.append(v_idx)
                    if n_idx is not None:
                        normal_indices.append(n_idx)

    vertices = [coord for idx in vertex_indices for coord in temp_vertices[idx]]
    normals = [coord for idx in normal_indices for coord in temp_normals[idx]] if normal_indices else None
    indices = list(range(len(vertex_indices)))

    if normals:
        return Mesh(vertices, indices, normals)
    else:
        return Mesh(vertices, indices)
