"""A simple class for viewing images using a pyglet window."""
from pyglet.window import Window as _Window
from pyglet.image import ImageData as _ImageData
from pyglet.gl import *


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

    def set_cursor(self, cursor) -> None:
        """
        Set the windows cursor to a new value.

        Args:
            cursor: the abstract pyglet cursor to set the mouse to

        Returns:
            None

        """
        self._window.set_mouse_cursor(cursor)

    def show(self, frame, _flip: bool=True) -> None:
        """
        Show an array of pixels on the window.

        Args:
            frame: the frame to show on the window

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
        frames = frame if isinstance(frame, (list, tuple)) else [frame]
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
            image.blit(0, 0, width=self._window.width, height=self._window.height)
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
