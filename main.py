import glfw
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective
import numpy as np
from camera import Camera
from mesh import Mesh, load_obj

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
    glClearColor(0.2, 0.3, 0.3, 1.0)
    return window

def main():
    window = init_window()
    camera = Camera()
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    # Load mesh from .obj file
    mesh = load_obj("models/cube.obj")

    # Callbacks
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

    glfw.set_cursor_pos_callback(window, mouse_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
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
