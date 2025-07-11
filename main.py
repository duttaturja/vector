import glfw
from OpenGL.GL import *
import numpy as np

def init_window(width, height, title):
    if not glfw.init():
        raise Exception("GLFW can't be initialized")

    window = glfw.create_window(width, height, title, None, None)
    if not window:
        glfw.terminate()
        raise Exception("GLFW window can't be created")

    glfw.make_context_current(window)
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
    window = init_window(800, 600, "3D Modeller - Step 1")

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        draw_triangle()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
