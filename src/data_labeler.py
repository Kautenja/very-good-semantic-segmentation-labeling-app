"""A data labeler for generating LED alert and audio alert systems."""
import os
import shutil
import numpy as np
from PIL import Image
from pyglet.window import key
from tqdm import tqdm
from .graphics import ImageView


class DataLabeler(object):

    def __init__(self, image_shape: tuple) -> None:
        """Initialize a new data labeling application."""
        # set the default color to black
        self._color = (0, 0, 0)
        # set a flag for when to advance to the next image
        self._can_advance = False
        # set the output vector to none (initialized by calls to run)
        self._output_vector = None
        # setup the window for the simulator
        self._view = ImageView('Data Labeler', image_shape)
        self._view.add_on_mouse_press_handler(self._on_mouse_press)
        self._view.add_on_key_press_handler(self._on_key_press)
        # # setup a callback on the window to handle keyboard events
        # def on_key_press(symbol: int, *args) -> None:
        #     """Respond to a pyglet keyboard key press event."""
        #     return self._on_key_press(symbol)
        # self._view.add_event_handler(on_key_press)
        # # setup a callback on the window to handle mouse events
        # def on_mouse_press(mouse_x: int, mouse_y: int, *args) -> None:
        #     """Respond to a pyglet mouse click event."""
        #     return self._on_mouse_press(mouse_x, mouse_y)
        # self._view.add_event_handler(on_mouse_press)

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

    # def run(self) -> None:
    #     """Run the simulation."""
    #     # iterate over the frames in the input video
    #     for filename in tqdm(sorted(os.listdir(self.data_path))):
    #         # reset the output vector
    #         self._output_vector = np.zeros((sum(self._view.num_leds), 2))
    #         # reset the LEDs
    #         self._view.reset_leds()
    #         # ignore files that aren't images
    #         if filename[-4:] not in {'.jpg', '.png'}:
    #             continue
    #         # open the image from disk
    #         image = Image.open(os.path.join(self.data_path, filename))
    #         frame = np.array(image)
    #         # update the window with the frame and predicted values
    #         self._view.update(frame, None, None, None)
    #         # wait for the advance key event to occur
    #         while not self._can_advance:
    #             self._view.event_step()
    #         self._can_advance = False
    #         # save the output vector to disk
    #         outfile = filename.replace('.jpg', '.npz').replace('.png', '.npz')
    #         outfile = os.path.join(self.output_dir, outfile)
    #         np.savez_compressed(outfile, y=self._output_vector)
    #         # print to the console if in verbose mode
    #         if self.verbose:
    #             print(outfile)
    #             print(self._output_vector)
    #             print()


# explicitly define the outward facing API of this module
__all__ = [DataLabeler.__name__]
