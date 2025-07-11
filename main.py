import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective
import numpy as np
from camera import Camera
from mesh import load_obj
import time

WIDTH, HEIGHT = 800, 600

def init_window():
    if not glfw.init():
        raise Exception("GLFW can't be initialized")

    window = glfw.create_window(WIDTH, HEIGHT, "Vector - 3D Modeller", None, None)
    if not window:
        glfw.terminate()
        raise Exception("GLFW window can't be created")

    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION,  (0.5, 1.0, 0.3, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT,   (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE,   (0.8, 0.8, 0.8, 1.0))
    glClearColor(0.2, 0.3, 0.3, 1.0)
    return window

def get_ray_from_mouse(x, y, view_matrix, projection_matrix):
    x = (2.0 * x) / WIDTH - 1.0
    y = 1.0 - (2.0 * y) / HEIGHT
    ray_nds = np.array([x, y, -1.0, 1.0])

    inv_proj = np.linalg.inv(projection_matrix)
    eye_coords = inv_proj @ ray_nds
    eye_coords = np.array([eye_coords[0], eye_coords[1], -1.0, 0.0])

    inv_view = np.linalg.inv(view_matrix)
    world_coords = inv_view @ eye_coords
    ray_dir = world_coords[:3]
    ray_dir = ray_dir / np.linalg.norm(ray_dir)
    return ray_dir

def main():
    window = init_window()
    camera = Camera()
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    mesh = load_obj("models/cube.obj")
    mesh.load_texture("textures/Bricks019_2K-JPG_Color.jpg")

    def mouse_callback(window, xpos, ypos):
        if camera.first_mouse:
            camera.last_x = xpos
            camera.last_y = ypos
            camera.first_mouse = False

        xoffset = xpos - camera.last_x
        yoffset = camera.last_y - ypos
        camera.last_x = xpos
        camera.last_y = ypos

        camera.process_mouse_movement(xoffset, yoffset)

    def scroll_callback(window, xoffset, yoffset):
        camera.process_scroll(yoffset)

    def mouse_button_callback(window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            xpos, ypos = glfw.get_cursor_pos(window)

            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            gluPerspective(camera.zoom, WIDTH / HEIGHT, 0.1, 100.0)
            projection = glGetDoublev(GL_PROJECTION_MATRIX).T
            glPopMatrix()

            view = camera.get_view_matrix()
            ray_dir = get_ray_from_mouse(xpos, ypos, view, projection)
            ray_origin = camera.position

            if mesh.intersect_ray(ray_origin, ray_dir):
                mesh.selected = not mesh.selected
                print("Mesh selected:", mesh.selected)

    glfw.set_cursor_pos_callback(window, mouse_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)

    last_frame = time.time()

    while not glfw.window_should_close(window):
        current_frame = time.time()
        delta_time = current_frame - last_frame
        last_frame = current_frame

        glfw.poll_events()

        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            camera.process_keyboard("FORWARD", delta_time)
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            camera.process_keyboard("BACKWARD", delta_time)
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            camera.process_keyboard("LEFT", delta_time)
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            camera.process_keyboard("RIGHT", delta_time)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(camera.zoom, WIDTH / HEIGHT, 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        view = camera.get_view_matrix()
        glLoadMatrixf(view.T)

        mesh.draw()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
