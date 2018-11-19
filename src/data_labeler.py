"""A semantic segmentation labeling application."""
import multiprocessing
import numpy as np
import pandas as pd
from PIL import Image
from pyglet.window import key
from skimage.segmentation import mark_boundaries
from skimage.draw import circle
from .cursor import make_cursor, make_ring, make_circle, pyglet_cursor
from .graphics.image_view import ImageView
from .graphics.palette import Palette
from .segment import segment


class DataLabeler(object):
    """A semantic segmentation labeling application."""

    def __init__(self,
        image: np.ndarray,
        metadata: pd.DataFrame,
        output_file: str,
        segmentation: np.ndarray=None,
        brush_border_color: tuple=(255, 255, 255),
    ) -> None:
        """
        Initialize a new data labeling application.

        Args:
            image: the image to segment
            metadata: the labeling metadata for the segmentation
            output_file: the output file to save segmentations to
            segmentation: an existing segmentation if there is one
            brush_border_color: the border color for the brush

        Returns:
            None

        """
        self._image = image
        self._metadata = metadata
        self._output_file = output_file
        self._segmentation = segmentation
        self._brush_border_color = brush_border_color
        self._opacity = 5
        self._brush_size = multiprocessing.Value('i', 5)
        self._is_brush = multiprocessing.Value('b', True)
        self._change_cursor = multiprocessing.Value('b', True)
        # create a raw array for sharing image data between processes
        raw_array = multiprocessing.RawArray('b', int(np.prod(image.shape)))
        numpy_array = np.frombuffer(raw_array, dtype='uint8')
        self._super_pixel = numpy_array.reshape(image.shape)
        # setup an array for the super pixel segmentation map
        raw_array = multiprocessing.RawArray('i', int(np.prod(image.shape[:-1])))
        numpy_array = np.frombuffer(raw_array, dtype='int32')
        self._super_pixel_segments = numpy_array.reshape(image.shape[:-1])
        # if there is no segmentation, initialize as the first label
        if self._segmentation is None:
            self._segmentation = np.zeros_like(image, dtype='uint8')
            self._segmentation[:, :, range(3)] = metadata['rgb'][0]
        # set the default color to the first label
        raw_array = multiprocessing.RawArray('b', 3)
        self._color = np.frombuffer(raw_array, dtype='uint8')
        self._color[:] = metadata['rgb'][0]
        # setup the window for the simulator and register event handlers
        self._view = ImageView('Data Labeler', image.shape[:2])
        self._view.add_on_mouse_press_handler(self._on_mouse_press)
        self._view.add_on_mouse_drag_handler(self._on_mouse_press)
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
            # if brush mode, draw on the image use the circles
            if self._is_brush.value:
                with self._brush_size.get_lock():
                    x, y = circle(mouse_x, mouse_y, self._brush_size.value)
                    self._segmentation[y, x] = self._color
            # if super pixel mode, draw on super pixels
            else:
                super_pixel = self._super_pixel_segments[mouse_y, mouse_x]
                mask = self._super_pixel_segments == super_pixel
                self._segmentation[mask] = self._color

    def _blit(self) -> None:
        """Blit local data structures to the GUI."""
        # setup the source image with an alpha channel
        alpha = 255 * np.ones_like(self.image[..., 0:1])
        img = np.concatenate([self._image, alpha], axis=-1)
        # setup the super pixel segmentations
        alpha = np.zeros_like(self.image)
        sup = mark_boundaries(alpha, self._super_pixel_segments,
            color=(127, 127, 127)
        )
        sup = np.concatenate([sup, sup[..., 0:1]], axis=-1).astype('uint8')
        # setup the segmentation image with an alpha channel scaled by the
        # opacity parameter of the application
        intensity = 255 * (self._opacity / 9)
        alpha = intensity * np.ones_like(self._segmentation[..., 0:1])
        seg = np.concatenate([self._segmentation, alpha], axis=-1).astype('uint8')
        # send the images to the window
        self._view.show([img, seg, sup])

    def _on_palette_change(self, palette_data: dict) -> None:
        """
        Respond to changes in the palette data.

        Args:
            palette_data: a dictionary of data from the palette process

        Returns:
            None

        """
        # set the color from the metadata
        color = self._metadata.set_index('label').loc[palette_data['label']]['rgb']
        # if the selected color is different, queue a cursor update
        if not np.array_equal(self._color, color):
            with self._change_cursor.get_lock():
                self._change_cursor.value = True
        # store the color with the new value
        self._color[:] = color
        # set the is brush flag
        with self._is_brush.get_lock():
            self._is_brush.value = palette_data['paint'] == 'brush'
        # set the brush size variable
        with self._brush_size.get_lock():
            # if the brush size is different, queue a cursor update
            if self._brush_size.value != palette_data['brush_size']:
                with self._change_cursor.get_lock():
                    self._change_cursor.value = True
            # store the brush size with the new value
            self._brush_size.value = palette_data['brush_size']
        # if the palette is in super pixel mode, get that data
        if palette_data['paint'] == 'super_pixel':
            # get the algorithm from the dictionary
            algorithm = palette_data['super_pixel']
            # get the arguments for the specific algorithm
            arguments = palette_data[algorithm]
            # get the segments using the given algorithm and arguments
            segs = segment(self._image, algorithm, **arguments)
            # apply the segmented image pixels and segments to local structures
            self._super_pixel_segments[:], self._super_pixel[:] = segs
        # otherwise set the super pixel data back to 0
        else:
            self._super_pixel_segments[:] = 0
            self._super_pixel[:] = 0

    def _update_cursor(self):
        """Update the mouse cursor for the application window."""
        # check if a cursor update is ready
        with self._change_cursor.get_lock():
            # if there is not update, return
            if not self._change_cursor.value:
                return
            # otherwise dequeue the update
            self._change_cursor.value = False
        # update the cursor with the brush size and color
        with self._brush_size.get_lock():
            # make a static border ring for the cursor
            ring = make_ring(self._brush_size.value - 1, self._brush_size.value)
            cursor = make_cursor(ring, self._brush_border_color)
            # make a circle with the current color
            circle = make_circle(self._brush_size.value) - ring
            cursor = cursor + make_cursor(circle, self._color)
            # create the pyglet cursor object and set it
            mouse = pyglet_cursor(cursor)
            self._view.set_cursor(mouse)

    def run(self) -> None:
        """Run the simulation."""
        # start the application and run until the flag is cleared
        self._is_running = True
        # start the palette thread
        Palette.thread(self._metadata, self._on_palette_change)
        while self._is_running:
            # update the cursor and blit changes to the screen
            self._update_cursor()
            self._blit()
        # close the image view
        self._view.close()


# explicitly define the outward facing API of this module
__all__ = [DataLabeler.__name__]
