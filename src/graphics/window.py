"""A simple class for viewing images using a pyglet window."""
from pyglet.window import Window as _Window
from pyglet.image import ImageData as _ImageData
from pyglet import gl


# the factor to zoom in by
ZOOM_IN = 1.2
# the factor to zoom out by
ZOOM_OUT = 1 / ZOOM_IN
# the max factor to zoom in by (matches the min brush size)
MAX_ZOOM = 5
# the min factor to zoom in by
MIN_ZOOM = 0.2


class Window(object):
    """A simple class for viewing images using a pyglet window."""

    def __init__(self, caption: str, height: int, width: int,
        encoding: str='RGBA'
    ) -> None:
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
        self._left = 0
        # TODO: is this necessary?
        self._right = width
        self._bottom = 0
        # TODO: is this necessary?
        self._top = height
        self._zoom_level = 1
        self._zoomed_width = width
        self._zoomed_height = height

    def __repr__(self) -> str:
        """Return an executable string representing this object."""
        return '{}(caption={}, height={}, width={}, encoding={})'.format(
            self.__class__.__name__,
            self.caption,
            self.height,
            self.width,
            self.encoding,
        )

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
        """
        Respond to mouse scrolling events.

        Args:
            x: the x position of the mouse
            y: the y position of the mouse
            dx: the rate of change in the x position
            dy: the rate of change in the y position

        Returns:
            None

        """
        # Get the scaling factor
        scale = ZOOM_IN if dy > 0 else ZOOM_OUT if dy < 0 else 1
        # check If zoom_level is in the legal range
        if not MIN_ZOOM < self._zoom_level * scale < MAX_ZOOM:
            return
        # scale the zoom level
        self._zoom_level *= scale
        # calculate the position of the mouse
        mouse_x = x / self.width
        mouse_y = y / self.height
        # determine the position of the mouse within the image
        mouse_x_in_img = self._left + mouse_x * self._zoomed_width
        mouse_y_in_img = self._bottom + mouse_y * self._zoomed_height
        # update the zoomed width and height variables
        self._zoomed_width *= scale
        self._zoomed_height *= scale
        # update the points of the image view frame
        self._left = mouse_x_in_img - mouse_x * self._zoomed_width
        self._right = mouse_x_in_img + (1 - mouse_x) * self._zoomed_width
        self._bottom = mouse_y_in_img - mouse_y * self._zoomed_height
        self._top = mouse_y_in_img + (1 - mouse_y) * self._zoomed_height

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
        self._left = 0
        self._right = self.width
        self._bottom = 0
        self._top = self.width
        self._zoom_level = 1
        self._zoomed_width = self.width
        self._zoomed_height = self.height

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
        speed = max(1.0, self._zoom_level)
        # update the positions of the frame corners
        self._left += dx * speed
        self._right += dx * speed
        self._bottom += dy * speed
        self._top += dy * speed

    def transform(self, x: int, y: int) -> any:
        """
        Transform x and y values on the screen to values on the base image.

        Args:
            x: the x position on the screen
            y: the y position on the screen

        Returns:
            the transformed x and y values

        """
        # determine the position of the mouse inside the original frame
        x = x - self._left
        y = y - self._bottom
        # transform the mouse positions to the new frame size
        x /= self._zoom_level
        y /= self._zoom_level
        # pass the values to the callback
        return x, y

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
        gl.glEnable(gl.GL_BLEND)
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
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            # blit the image to the window
            image.blit(self._left, self._bottom,
                width=self._zoomed_width,
                height=self._zoomed_height
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
