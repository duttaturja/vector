import glfw
from OpenGL.GL import *
import numpy as np
from camera import Camera
from OpenGL.GLU import gluPerspective

# Window dimensions
WIDTH, HEIGHT = 800, 600

def init_window():
    if not glfw.init():
        raise Exception("GLFW can't be initialized")

    window = glfw.create_window(WIDTH, HEIGHT, "3D Modeller - Camera Control", None, None)
    if not window:
        glfw.terminate()
        raise Exception("GLFW window can't be created")

    glfw.make_context_current(window)

    # Enable depth testing
    glEnable(GL_DEPTH_TEST)
    return window

def draw_triangle():
    glBegin(GL_TRIANGLES)
    glColor3f(1, 0, 0)  # Red
    glVertex3f(-0.5, -0.5, 0)
    glColor3f(0, 1, 0)  # Green
    glVertex3f(0.5, -0.5, 0)
    glColor3f(0, 0, 1)  # Blue
    glVertex3f(0, 0.5, 0)
    glEnd()

def main():
    window = init_window()

    camera = Camera()
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    # Mouse callback
    def mouse_callback(window, xpos, ypos):
        if camera.first_mouse:
            camera.last_x = xpos
            camera.last_y = ypos
            camera.first_mouse = False

        xoffset = xpos - camera.last_x
        yoffset = camera.last_y - ypos  # reversed since y-coords go from bottom to top
        camera.last_x = xpos
        camera.last_y = ypos

        camera.process_mouse_movement(xoffset, yoffset)

    glfw.set_cursor_pos_callback(window, mouse_callback)

    # Scroll callback
    def scroll_callback(window, xoffset, yoffset):
        camera.process_scroll(yoffset)

    glfw.set_scroll_callback(window, scroll_callback)

    # Set projection matrix once
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Perspective projection params: fov, aspect, near, far
    gluPerspective(camera.zoom, WIDTH / HEIGHT, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        # Clear screen and depth buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(camera.zoom, WIDTH / HEIGHT, 0.1, 100.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        view = camera.get_view_matrix()
        glLoadMatrixf(view.T)  # transpose here
        
        draw_triangle()

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
