import numpy as np

class Camera:
    def __init__(self):
        self.position = np.array([0.0, 0.0, 3.0], dtype=np.float32)
        self.front = np.array([0.0, 0.0, -1.0], dtype=np.float32)
        self.up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        self.right = np.cross(self.front, self.up)

        self.yaw = -90.0
        self.pitch = 0.0
        self.zoom = 45.0

        self.first_mouse = True
        self.last_x = 400
        self.last_y = 300

        self.speed = 2.5
        self.sensitivity = 0.1

    def get_view_matrix(self):
        center = self.position + self.front
        return self.look_at(self.position, center, self.up)

    def look_at(self, eye, center, up):
        f = center - eye
        f = f / np.linalg.norm(f)

        s = np.cross(f, up)
        s = s / np.linalg.norm(s)

        u = np.cross(s, f)

        result = np.identity(4, dtype=np.float32)
        result[0, 0:3] = s
        result[1, 0:3] = u
        result[2, 0:3] = -f
        result[0, 3] = -np.dot(s, eye)
        result[1, 3] = -np.dot(u, eye)
        result[2, 3] = np.dot(f, eye)

        return result

    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        xoffset *= self.sensitivity
        yoffset *= self.sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        if constrain_pitch:
            self.pitch = max(-89.0, min(89.0, self.pitch))

        self.update_camera_vectors()

    def process_scroll(self, yoffset):
        self.zoom -= yoffset
        self.zoom = max(1.0, min(45.0, self.zoom))

    def process_keyboard(self, direction, delta_time):
        velocity = self.speed * delta_time
        if direction == "FORWARD":
            self.position += self.front * velocity
        if direction == "BACKWARD":
            self.position -= self.front * velocity
        if direction == "LEFT":
            self.position -= self.right * velocity
        if direction == "RIGHT":
            self.position += self.right * velocity

    def update_camera_vectors(self):
        yaw_r = np.radians(self.yaw)
        pitch_r = np.radians(self.pitch)

        front = np.array([
            np.cos(yaw_r) * np.cos(pitch_r),
            np.sin(pitch_r),
            np.sin(yaw_r) * np.cos(pitch_r)
        ], dtype=np.float32)

        self.front = front / np.linalg.norm(front)
        self.right = np.cross(self.front, self.up)
        self.right = self.right / np.linalg.norm(self.right)
