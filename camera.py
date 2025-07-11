import numpy as np

class Camera:
    def __init__(self, position=None, target=None, up=None):
        self.position = np.array(position if position else [0, 0, 3], dtype=np.float32)
        self.target = np.array(target if target else [0, 0, 0], dtype=np.float32)
        self.up = np.array(up if up else [0, 1, 0], dtype=np.float32)

        self.yaw = -90.0
        self.pitch = 0.0
        self.last_x = 400
        self.last_y = 300
        self.first_mouse = True
        self.zoom = 45.0

        self.front = np.array([0, 0, -1], dtype=np.float32)

    def get_view_matrix(self):
        direction = self.position + self.front
        return self.look_at(self.position, direction, self.up)

    def look_at(self, eye, center, up):
        f = (center - eye)
        f = f / np.linalg.norm(f)

        s = np.cross(f, up)
        s = s / np.linalg.norm(s)

        u = np.cross(s, f)

        result = np.identity(4, dtype=np.float32)
        result[0, :3] = s
        result[1, :3] = u
        result[2, :3] = -f
        result[0, 3] = -np.dot(s, eye)
        result[1, 3] = -np.dot(u, eye)
        result[2, 3] = np.dot(f, eye)
        return result

    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        sensitivity = 0.1
        xoffset *= sensitivity
        yoffset *= sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        if constrain_pitch:
            self.pitch = max(-89.0, min(89.0, self.pitch))

        front = np.array([
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)),
            np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        ], dtype=np.float32)
        self.front = front / np.linalg.norm(front)

    def process_scroll(self, yoffset):
        self.zoom -= yoffset
        self.zoom = max(1.0, min(45.0, self.zoom))
