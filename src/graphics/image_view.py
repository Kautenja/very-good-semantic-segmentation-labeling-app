"""An image view using NumPy and Pyglet."""
import pyglet
from .window import Window


class ImageView(object):
    """An image view using NumPy and Pyglet."""

    def __init__(self, caption: str, image_shape: tuple) -> None:
        """
        Initialize a new driving simulator.

        Args:
            caption:
            image_shape:

        Returns:
            None

        """
        # setup the window for this view
        self.image_shape = image_shape
        self._window = Window(caption, *image_shape)

    def set_cursor(self, cursor) -> None:
        """
        Set the windows cursor to a new value.

        Args:
            cursor: the abstract pyglet cursor to set the mouse to

        Returns:
            None

        """
        self._window.set_cursor(cursor)

    def add_event_handler(self, handler) -> None:
        """
        Add an event handler to the view.

        Args:
            handler: a callable handler to register with the view

        Returns:
            None

        """
        self._window.window.event(handler)

    def left_mouse_handler(self, x: int, y: int, handler: 'Callable') -> any:
        """
        Handle mouse events when the left button is pressed, held, released.

        Args:
            x: the x position on the screen
            y: the y position on the screen
            handler: the callable handler

        Returns:
            the output of the handler method

        """
        # determine the position of the mouse inside the original frame
        x = x + -self._window.left
        y = self.image_shape[0] - y + self._window.bottom
        # transform the mouse positions to the new frame size
        x /= self._window.zoom_level
        y = self.image_shape[0] - (self.image_shape[0] - y) / self._window.zoom_level
        # pass the values to the callback
        return handler(x, y)

    def add_on_mouse_press_handler(self, handler) -> None:
        """
        Add an on mouse press event handler to the view.

        Args:
            handler: a callable mouse press handler to register with the view

        Returns:
            None

        """
        def on_mouse_press(x, y, buttons, _) -> None:
            """Respond to a pyglet mouse click event."""
            # if the button is the left button, pass values to the handler
            if buttons == pyglet.window.mouse.LEFT:
                return self.left_mouse_handler(x, y, handler)
        # add the method as an event handler to the window
        self.add_event_handler(on_mouse_press)

    def add_on_mouse_drag_handler(self, handler) -> None:
        """
        Add an on mouse drag event handler to the view.

        Args:
            handler: a callable mouse drag handler to register with the view

        Returns:
            None

        """
        def on_mouse_drag(x, y, dx, dy, buttons, _) -> None:
            """Respond to a pyglet mouse drag event."""
            # if the button is the right button, move the camera
            if buttons == pyglet.window.mouse.RIGHT:
                self._window.move_camera(dx, dy)
            # if the button is the left button, pass values to the handler
            elif buttons == pyglet.window.mouse.LEFT:
                return self.left_mouse_handler(x, y, handler)
        # add the method as an event handler to the window
        self.add_event_handler(on_mouse_drag)

    def add_on_key_press_handler(self, handler) -> None:
        """
        Add an on key press event handler to the view.

        Args:
            handler: a callable key press handler to register with the view

        Returns:
            None

        """
        def on_key_press(symbol: int, *args) -> None:
            """Respond to a pyglet keyboard key press event."""
            return handler(symbol)
        # add the method as an event handler to the window
        self.add_event_handler(on_key_press)

    def show(self, image: 'np.ndarray') -> None:
        """
        Show the window with the given data.

        Args:
            image: the image to display on the image view

        Returns:
            None

        """
        self._window.show(image)

    def close(self):
        """Close the view."""
        self._window.close()


# explicitly define the outward facing API of this module
__all__ = [ImageView.__name__]
