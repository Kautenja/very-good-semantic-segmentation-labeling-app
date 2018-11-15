"""A data labeler for generating LED alert and audio alert systems."""
import os
import shutil
import numpy as np
from PIL import Image
from pyglet.window import key
from tqdm import tqdm
from .graphics.image_view import ImageView


class DataLabeler(object):

    def __init__(self, image: np.ndarray, metadata, segmentation: np.ndarray=None) -> None:
        """
        Initialize a new data labeling application.

        Args:
            image: the image to segment
            metadata: the labeling metadata for the segmentation
            segmentation: an existing segmentation if there is one

        Returns:
            None

        """
        self._image = image
        self._segmentation = segmentation
        # set the default color to black
        self._color = (0, 0, 0)
        # setup the window for the simulator and register event handlers
        self._view = ImageView('Data Labeler', image.shape[:2])
        self._view.add_on_mouse_press_handler(self._on_mouse_press)
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
        pass
        # # if key is return, move to the next frame
        # if symbol == key.RETURN:
        #     self._can_advance = True
        # # set the color and intensity based on the values in the mappings.
        # # Because the dictionaries have mutually exclusive keys, use the get
        # # method for both and default to the current value when the key isn't
        # # found.
        # self._color = COLORS.get(symbol, self._color)
        # self._intensity = self._intensity_map.get(symbol, self._intensity)

    def _on_mouse_press(self, mouse_x: int, mouse_y: int) -> None:
        """
        Handle a callback when a mouse click occurs.

        Args:
            mouse_x: the x pixel of the mouse
            mouse_y: the y pixel of the mouse

        Returns:
            None

        """
        pass
        # # set the LED on the window
        # led = self._view.set_led(mouse_x, mouse_y, self.led_color)
        # # if the index of the LED is None, i.e., no LED clicked, return
        # if led is None:
        #     return
        # # update the target vector
        # self._output_vector[led, 0] = CODES[self.color]
        # # set the intensity for the color
        # self._output_vector[led, 1] = self.intensity

    def run(self) -> None:
        """Run the simulation."""
        # start the application and run until the flag is cleared
        self._is_running = True
        while self._is_running:
            # process events from the window
            self._view.event_step()


# explicitly define the outward facing API of this module
__all__ = [DataLabeler.__name__]
