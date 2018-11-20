import pyglet
from pyglet.gl import *

# Zooming constants
ZOOM_IN_FACTOR = 1.2
ZOOM_OUT_FACTOR = 1/ZOOM_IN_FACTOR

class App(pyglet.window.Window):

    def __init__(self, width, height, *args, **kwargs):
        super().__init__(width, height)
        #Initialize camera values
        self.left   = 0
        self.right  = width
        self.bottom = 0
        self.top    = height
        self.zoom_level = 1
        self.zoomed_width  = width
        self.zoomed_height = height

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
    # def on_mouse_scroll(self, x, y, dx, dy):
        # Move camera
        self.left   -= dx * self.zoom_level
        self.right  -= dx * self.zoom_level
        self.bottom -= dy * self.zoom_level
        self.top    -= dy * self.zoom_level

    def on_mouse_scroll(self, x, y, dx, dy):
    # def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # Get scale factor
        f = ZOOM_IN_FACTOR if dy > 0 else ZOOM_OUT_FACTOR if dy < 0 else 1
        # If zoom_level is in the proper range
        if .2 < self.zoom_level * f < 5:

            self.zoom_level *= f

            mouse_x = x / self.width
            mouse_y = y / self.height

            mouse_x_in_world = self.left + mouse_x * self.zoomed_width
            mouse_y_in_world = self.bottom + mouse_y * self.zoomed_height

            self.zoomed_width  *= f
            self.zoomed_height *= f

            self.left   = mouse_x_in_world - mouse_x * self.zoomed_width
            self.right  = mouse_x_in_world + (1 - mouse_x) * self.zoomed_width
            self.bottom = mouse_y_in_world - mouse_y * self.zoomed_height
            self.top    = mouse_y_in_world + (1 - mouse_y) * self.zoomed_height

    def on_draw(self):
        # Initialize Projection matrix
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()

        # Initialize Modelview matrix
        glMatrixMode( GL_MODELVIEW )
        glLoadIdentity()
        # Save the default modelview matrix
        glPushMatrix()

        # Clear window with ClearColor
        glClear( GL_COLOR_BUFFER_BIT )

        # Set orthographic projection matrix
        glOrtho( self.left, self.right, self.bottom, self.top, 1, -1 )

        # Draw quad
        glBegin( GL_QUADS )
        glColor3ub( 0xFF, 0, 0 )
        glVertex2i( 10, 10 )

        glColor3ub( 0xFF, 0xFF, 0 )
        glVertex2i( 110, 10 )

        glColor3ub( 0, 0xFF, 0 )
        glVertex2i( 110, 110 )

        glColor3ub( 0, 0, 0xFF )
        glVertex2i( 10, 110 )
        glEnd()

        # Remove default modelview matrix
        glPopMatrix()

    def run(self):
        pyglet.app.run()


App(500, 500).run()
