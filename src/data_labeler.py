"""A data labeler for generating LED alert and audio alert systems."""
import numpy as np
import pandas as pd
from PIL import Image
from pyglet.window import key
from .graphics.image_view import ImageView


class DataLabeler(object):

    def __init__(self, image: np.ndarray, metadata: pd.DataFrame,
        segmentation: np.ndarray=None
    ) -> None:
        """
        Initialize a new data labeling application.

        Args:
            image: the image to segment
            metadata: the labeling metadata for the segmentation
            segmentation: an existing segmentation if there is one

        Returns:
            None

        """
        self._opacity = 9
        self._image = image
        self._metadata = metadata
        self._segmentation = segmentation
        # if there is no segmentation, initialize as the first label
        if self._segmentation is None:
            self._segmentation = np.zeros_like(image, dtype='uint8')
            self._segmentation[:, :, range(3)] = metadata['rgb'][1]
        # set the default color to black
        self._color = (0, 0, 0)
        # setup the window for the simulator and register event handlers
        self._view = ImageView('Data Labeler', image.shape[:2])
        self._view.add_on_mouse_press_handler(self._on_mouse_press)
        self._view.add_on_mouse_drag_handler(self._on_mouse_drag)
        self._view.add_on_key_press_handler(self._on_key_press)
        # setup a flag to determine if the application is running
        self._is_running = False

    def _on_key_press(self, symbol: int) -> None:
        """
        Handle a callback when a keyboard event occurs.

        Args:
            symbol: the symbol on the keyboard

        Returns:
            None

        """
        # if key is save, save the segmentation to disk
        if symbol == key.S:
            print('saving')
        # if key is escape, save the segmentation to disk and quit
        elif symbol == key.ESCAPE:
            print('saving and quitting')
        # if the key is in [48, 59] it's numeric, adjust the opacity overlay
        elif 48 <= symbol <= 59:
            print('setting opacity to {}'.format(symbol - 48))
            self._opacity = symbol - 48

    def _on_mouse_press(self, mouse_x: int, mouse_y: int) -> None:
        """
        Handle a callback when a mouse click occurs.

        Args:
            mouse_x: the x pixel of the mouse
            mouse_y: the y pixel of the mouse

        Returns:
            None

        """
        print(mouse_x, mouse_y)

    def _on_mouse_drag(self, mouse_x: int, mouse_y: int) -> None:
        """
        Handle a callback when a mouse drag occurs.

        Args:
            mouse_x: the x pixel of the mouse
            mouse_y: the y pixel of the mouse

        Returns:
            None

        """
        print(mouse_x, mouse_y)

    def _blit(self) -> None:
        """Blit local data structures to the GUI."""
        # setup the source image with an alpha channel
        alpha = 255 * np.ones_like(self._image[..., 0:1])
        img = np.concatenate([self._image, alpha], axis=-1)
        # setup the segmentation image with an alpha channel scaled by the
        # opacity parameter of the application
        intensity = 255 * (self._opacity / 9)
        alpha = intensity * np.ones_like(self._segmentation[..., 0:1])
        seg = np.concatenate([self._segmentation, alpha], axis=-1).astype('uint8')
        # send the images to the window
        self._view.show([img, seg])

    def run(self) -> None:
        """Run the simulation."""
        # start the application and run until the flag is cleared
        self._is_running = True
        while self._is_running:
            # process events from the window
            self._view.event_step()
            # blit changes to the screen
            self._blit()


# explicitly define the outward facing API of this module
__all__ = [DataLabeler.__name__]
