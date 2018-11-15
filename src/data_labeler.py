"""A semantic segmentation labeling application."""
import multiprocessing
import numpy as np
import pandas as pd
from PIL import Image
from pyglet.window import key
from .graphics.image_view import ImageView
from .graphics.palette import Palette
from .segment import segment


class DataLabeler(object):
    """A semantic segmentation labeling application."""

    def __init__(self,
        image: np.ndarray,
        metadata: pd.DataFrame,
        output_file: str,
        segmentation: np.ndarray=None
    ) -> None:
        """
        Initialize a new data labeling application.

        Args:
            image: the image to segment
            metadata: the labeling metadata for the segmentation
            output_file: the output file to save segmentations to
            segmentation: an existing segmentation if there is one

        Returns:
            None

        """
        self._image = image
        self._metadata = metadata
        self._output_file = output_file
        self._segmentation = segmentation
        self._opacity = 5
        self._brush_size = multiprocessing.Value('i', 5)
        self._is_brush = multiprocessing.Value('b', True)
        # create a raw array for sharing image data between processes
        raw_array = multiprocessing.RawArray('b', int(np.prod(image.shape)))
        numpy_array = np.frombuffer(raw_array, dtype='uint8')
        self._super_pixel = numpy_array.reshape(image.shape)
        #
        raw_array = multiprocessing.RawArray('i', int(np.prod(image.shape[:-1])))
        numpy_array = np.frombuffer(raw_array, dtype='int32')
        self._super_pixel_segments = numpy_array.reshape(image.shape[:-1])
        # if there is no segmentation, initialize as the first label
        if self._segmentation is None:
            self._segmentation = np.zeros_like(image, dtype='uint8')
            self._segmentation[:, :, range(3)] = metadata['rgb'][0]
        # set the default color to the first label
        self._color = metadata['rgb'][0]
        # setup the window for the simulator and register event handlers
        self._view = ImageView('Data Labeler', image.shape[:2])
        self._view.add_on_mouse_press_handler(self._on_mouse_press)
        self._view.add_on_mouse_drag_handler(self._on_mouse_drag)
        self._view.add_on_key_press_handler(self._on_key_press)
        # setup a flag to determine if the application is running
        self._is_running = False

    @property
    def image(self) -> np.ndarray:
        """Return the image to display under the labeling overlay."""
        # get the lock for the brush value
        with self._is_brush.get_lock():
            # if brush mode, return the normal image
            if self._is_brush.value:
                return self._image
            # otherwise in super pixel mode, return the super pixel
            return self._super_pixel

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
            Image.fromarray(self._segmentation).save(self._output_file)
        # if key is escape, save the segmentation to disk and quit
        elif symbol == key.ESCAPE:
            print('saving and quitting')
            Image.fromarray(self._segmentation).save(self._output_file)
            self._is_running = False
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
        # get the lock for the brush value
        with self._is_brush.get_lock():
            # if brush mode, return the normal image
            if self._is_brush.value:
                print('brush')
            else:
                print('super pixel')
                super_pixel = self._super_pixel_segments[mouse_y, mouse_x]
                mask = self._super_pixel_segments == super_pixel
                self._segmentation[mask] = self._color

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
        alpha = 255 * np.ones_like(self.image[..., 0:1])
        img = np.concatenate([self.image, alpha], axis=-1)
        # setup the segmentation image with an alpha channel scaled by the
        # opacity parameter of the application
        intensity = 255 * (self._opacity / 9)
        alpha = intensity * np.ones_like(self._segmentation[..., 0:1])
        seg = np.concatenate([self._segmentation, alpha], axis=-1).astype('uint8')
        # send the images to the window
        self._view.show([img, seg])

    def _on_palette_change(self, palette_data: dict) -> None:
        """
        Respond to changes in the palette data.

        Args:
            palette_data: a dictionary of data from the palette process

        Returns:
            None

        """
        self._color = self._metadata.set_index('label').loc[palette_data['label']]['rgb']
        with self._is_brush.get_lock():
            self._is_brush.value = palette_data['paint'] == 'brush'
        with self._brush_size.get_lock():
            self._brush_size.value = palette_data['brush_size']
        if palette_data['paint'] == 'super_pixel':
            algorithm = palette_data['super_pixel']
            arguments = palette_data[algorithm]
            segs = segment(self._image, algorithm, **arguments)
            self._super_pixel_segments[:], self._super_pixel[:] = segs

    def run(self) -> None:
        """Run the simulation."""
        # start the application and run until the flag is cleared
        self._is_running = True
        Palette.thread(self._metadata, self._on_palette_change)
        while self._is_running:
            # process events from the window
            self._view.event_step()
            # blit changes to the screen
            self._blit()
        # close the image view
        self._view.close()


# explicitly define the outward facing API of this module
__all__ = [DataLabeler.__name__]
