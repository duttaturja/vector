import numpy as np
from OpenGL.GL import *
from PIL import Image

def ray_triangle_intersect(orig, dir, v0, v1, v2):
    eps = 1e-6
    edge1 = v1 - v0
    edge2 = v2 - v0
    h = np.cross(dir, edge2)
    a = np.dot(edge1, h)
    if -eps < a < eps:
        return False
    f = 1.0 / a
    s = orig - v0
    u = f * np.dot(s, h)
    if u < 0.0 or u > 1.0:
        return False
    q = np.cross(s, edge1)
    v = f * np.dot(dir, q)
    if v < 0.0 or u + v > 1.0:
        return False
    t = f * np.dot(edge2, q)
    return t > eps

class Mesh:
    def __init__(self, vertices, indices, normals):
        self.vertices = np.array(vertices)
        self.indices = indices
        self.normals = normals if normals else None
        self.selected = False
        self.texture_id = None

    def load_texture(self, path):
        img = Image.open(path)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.array(img, dtype=np.uint8)

        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)

    def draw(self):
        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glBegin(GL_TRIANGLES)
        for i in self.indices:
            if self.normals and i < len(self.normals):
                glNormal3fv(self.normals[i])
            if self.selected:
                glColor3f(1.0, 0.0, 0.0)  # red if selected
            else:
                glColor3f(1.0, 1.0, 1.0)  # white if not
            glVertex3fv(self.vertices[i])
        glEnd()

        if self.texture_id:
            glDisable(GL_TEXTURE_2D)

    def intersect_ray(self, origin, direction):
        print("Checking intersection...")
        for i in range(0, len(self.indices), 3):
            v0 = self.vertices[self.indices[i]]
            v1 = self.vertices[self.indices[i + 1]]
            v2 = self.vertices[self.indices[i + 2]]
            if ray_triangle_intersect(origin, direction, v0, v1, v2):
                return True
        return False

def load_obj(path):
    vertices = []
    normals = []
    indices = []

    with open(path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                vertices.append(list(map(float, line.strip().split()[1:])))
            elif line.startswith('vn '):
                normals.append(list(map(float, line.strip().split()[1:])))
            elif line.startswith('f '):
                face = line.strip().split()[1:]
                for vertex in face:
                    if '//' in vertex:
                        parts = vertex.split('//')
                        idx = int(parts[0]) - 1
                    elif '/' in vertex:
                        parts = vertex.split('/')
                        idx = int(parts[0]) - 1
                    else:
                        idx = int(vertex) - 1
                    indices.append(idx)

    return Mesh(vertices, indices, normals)
