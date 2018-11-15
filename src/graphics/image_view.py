"""An image view using NumPy and Pyglet."""
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
        self._window = Window(caption, *image_shape)

    def show(self, image: 'np.ndarray') -> None:
        """
        Show the window with the given data.

        Args:
            image: the image to display on the image view

        Returns:
            None

        """
        self._window.show(image)

    def add_event_handler(self, handler) -> None:
        """
        Add an event handler to the view.

        Args:
            handler: a callable handler to register with the view

        Returns:
            None

        """
        self._window.window.event(handler)

    def add_on_mouse_press_handler(self, handler) -> None:
        """
        Add an on mouse press event handler to the view.

        Args:
            handler: a callable mouse press handler to register with the view

        Returns:
            None

        """
        def on_mouse_press(mouse_x: int, mouse_y: int, *args) -> None:
            """Respond to a pyglet mouse click event."""
            return handler(mouse_x, mouse_y)
        self.add_event_handler(on_mouse_press)

    def add_on_mouse_drag_handler(self, handler) -> None:
        """
        Add an on mouse drag event handler to the view.

        Args:
            handler: a callable mouse drag handler to register with the view

        Returns:
            None

        """
        def on_mouse_drag(mouse_x: int, mouse_y: int, *args) -> None:
            """Respond to a pyglet mouse drag event."""
            return handler(mouse_x, mouse_y)
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
        self.add_event_handler(on_key_press)

    def event_step(self) -> None:
        """Perform an event step to handle events in a loop."""
        self._window.window.switch_to()
        self._window.window.dispatch_events()
        self._window.window.dispatch_event('on_draw')
        self._window.window.flip()


# explicitly define the outward facing API of this module
__all__ = [ImageView.__name__]
