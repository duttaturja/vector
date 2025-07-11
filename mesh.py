from OpenGL.GL import *
import numpy as np
from PIL import Image

class Mesh:
    def __init__(self, vertices, indices, normals=None, texcoords=None):
        self.vertices = np.array(vertices, dtype=np.float32)
        self.indices = np.array(indices, dtype=np.uint32)
        self.normals = np.array(normals, dtype=np.float32) if normals else None
        self.texcoords = np.array(texcoords, dtype=np.float32) if texcoords else None
        self.texture_id = None

    def load_texture(self, path):
        image = Image.open(path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = image.convert("RGBA").tobytes()

        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glBindTexture(GL_TEXTURE_2D, 0)

    def draw(self):
        if self.texcoords is not None and self.texture_id is not None:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vertices)

        if self.normals is not None:
            glEnableClientState(GL_NORMAL_ARRAY)
            glNormalPointer(GL_FLOAT, 0, self.normals)

        if self.texcoords is not None:
            glEnableClientState(GL_TEXTURE_COORD_ARRAY)
            glTexCoordPointer(2, GL_FLOAT, 0, self.texcoords)

        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, self.indices)

        glDisableClientState(GL_VERTEX_ARRAY)
        if self.normals is not None:
            glDisableClientState(GL_NORMAL_ARRAY)
        if self.texcoords is not None:
            glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        if self.texcoords is not None and self.texture_id is not None:
            glBindTexture(GL_TEXTURE_2D, 0)
            glDisable(GL_TEXTURE_2D)

def load_obj(filepath):
    temp_vertices = []
    temp_normals = []
    temp_texcoords = []
    vertex_indices = []
    normal_indices = []
    texcoord_indices = []

    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith('v '):
                parts = line.strip().split()
                temp_vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif line.startswith('vn '):
                parts = line.strip().split()
                temp_normals.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif line.startswith('vt '):
                parts = line.strip().split()
                temp_texcoords.append([float(parts[1]), float(parts[2])])
            elif line.startswith('f '):
                parts = line.strip().split()[1:]
                for part in parts:
                    vals = part.split('/')
                    v_idx = int(vals[0]) - 1
                    t_idx = int(vals[1]) - 1 if len(vals) > 1 and vals[1] != '' else None
                    n_idx = int(vals[2]) - 1 if len(vals) > 2 and vals[2] != '' else None

                    vertex_indices.append(v_idx)
                    if t_idx is not None:
                        texcoord_indices.append(t_idx)
                    if n_idx is not None:
                        normal_indices.append(n_idx)

    vertices = [coord for idx in vertex_indices for coord in temp_vertices[idx]]
    normals = [coord for idx in normal_indices for coord in temp_normals[idx]] if normal_indices else None
    texcoords = [coord for idx in texcoord_indices for coord in temp_texcoords[idx]] if texcoord_indices else None
    indices = list(range(len(vertex_indices)))

    return Mesh(vertices, indices, normals, texcoords)
