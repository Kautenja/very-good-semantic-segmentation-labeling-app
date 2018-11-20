"""A simple class for viewing images using a pyglet window."""
from pyglet.window import Window as _Window
from pyglet.image import ImageData as _ImageData
from pyglet.gl import *


# the factor to zoom in by
ZOOM_IN_FACTOR = 1.2
# the factor to zoom out by
ZOOM_OUT_FACTOR = 1 / ZOOM_IN_FACTOR


class Window(object):
    """A simple class for viewing images using a pyglet window."""

    def __init__(self, caption: str, height: int, width: int, encoding: str='RGBA') -> None:
        """
        Initialize a new image viewer.

        Args:
            caption: the caption/title for the window
            height: the height of the window
            width: the width of the window
            encoding: the encoding of the images to display

        Returns:
            None

        """
        self.caption = caption
        self.height = height
        self.width = width
        self.encoding = encoding
        self._window = None
        self.left = 0
        self.right = width
        self.bottom = 0
        self.top = height
        self.zoom_level = 1
        self.zoomed_width = width
        self.zoomed_height = height

    def __repr__(self) -> str:
        """Return an executable string representing this object."""
        template = '{}(caption={}, height={}, width={})'
        return template.format(self.caption, self.height, self.width)

    def __del__(self) -> None:
        """Close any open windows and delete this object."""
        self.close()

    @property
    def is_open(self) -> bool:
        """Return a boolean determining if this window is open."""
        return self._window is not None

    @property
    def window(self) -> _Window:
        """Return the pyglet window inside this image viewer."""
        # open the window if it isn't open already
        if not self.is_open:
            self.open()
        return self._window

    def open(self) -> None:
        """Open the window."""
        self._window = _Window(
            caption=self.caption,
            height=self.height,
            width=self.width,
            vsync=False,
            resizable=False,
        )
        self._window.event(self.on_mouse_scroll)

    def on_mouse_scroll(self, x: int, y: int, dx: float, dy: float) -> None:
        """Respond to mouse scrolling events."""
        # Get the scaling factor
        f = ZOOM_IN_FACTOR if dy > 0 else ZOOM_OUT_FACTOR if dy < 0 else 1
        # check If zoom_level is in the legal range
        if .2 < self.zoom_level * f < 5:
            self.zoom_level *= f
            # calculate the position of the mouse
            mouse_x = x / self.width
            mouse_y = y / self.height
            # determine the position of the mouse within the image
            mouse_x_in_img = self.left + mouse_x * self.zoomed_width
            mouse_y_in_img = self.bottom + mouse_y * self.zoomed_height
            # update the zoomed width and height variables
            self.zoomed_width *= f
            self.zoomed_height *= f
            # update the points of the image view frame
            self.left = mouse_x_in_img - mouse_x * self.zoomed_width
            self.right = mouse_x_in_img + (1 - mouse_x) * self.zoomed_width
            self.bottom = mouse_y_in_img - mouse_y * self.zoomed_height
            self.top = mouse_y_in_img + (1 - mouse_y) * self.zoomed_height

    def set_cursor(self, cursor) -> None:
        """
        Set the windows cursor to a new value.

        Args:
            cursor: the abstract pyglet cursor to set the mouse to

        Returns:
            None

        """
        self._window.set_mouse_cursor(cursor)

    def reset_camera(self) -> None:
        """Reset the camera to it's default position."""
        self.left = 0
        self.right = self.width
        self.bottom = 0
        self.top = self.width
        self.zoom_level = 1
        self.zoomed_width = self.width
        self.zoomed_height = self.height

    def move_camera(self, dx: float, dy: float) -> None:
        """
        Move the camera of the window with given velocity.

        Args:
            dx: the rate of change in x value
            dy: the rate of change in y value

        Returns:
            None

        """
        # determine the speed to move the camera at
        speed = max(1.0, self.zoom_level)
        # update the positions of the frame corners
        self.left += dx * speed
        self.right += dx * speed
        self.bottom += dy * speed
        self.top += dy * speed

    def show(self, data: list) -> None:
        """
        Show an array of pixels on the window.

        Args:
            data: the data to show on the window

        Returns:
            None
        """
        # open the window if it isn't open already
        if not self.is_open:
            self.open()
        # prepare the window for the next frame
        self._window.clear()
        self._window.switch_to()
        self._window.dispatch_events()
        # create the list of frames from the inputs
        frames = data if isinstance(data, (list, tuple)) else [data]
        # setup alpha channel blending
        glEnable(GL_BLEND)
        # iterate over the frames in the input
        for frame in frames:
            # create an image data object
            image = _ImageData(
                frame.shape[1],
                frame.shape[0],
                self.encoding,
                frame.tobytes(),
                pitch=frame.shape[1] * -len(self.encoding)
            )
            # set the alpha channel blend mode for the image
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            # blit the image to the window
            image.blit(self.left, self.bottom,
                width=self.zoomed_width,
                height=self.zoomed_height
            )

        # flip the changes to the window
        self._window.flip()

    def close(self) -> None:
        """Close the window."""
        # if the window is open, close and delete the window
        if self.is_open:
            self._window.close()
            self._window = None


# explicitly define the outward facing API of this module
__all__ = [Window.__name__]
