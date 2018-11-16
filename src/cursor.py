"""A method for setting up a brush cursor."""
import numpy as np
from skimage.draw import circle as draw_circle


def make_circle(radius: int, dtype: str='uint8') -> np.ndarray:
    """
    Make a circle with a given radius.

    Args:
        radius: the radius of the circle to draw

    Returns:
        a Numpy matrix of size 2 * radius + 1 with a circle in it.

    """
    # if the radius is even, make it odd
    length = 2 * radius + 1
    # create an RGBA box to house the circle in
    box = np.zeros((length, length), dtype=dtype)
    # get the coordinates for the circle
    x_pixels, y_pixels = draw_circle(radius, radius, radius)
    # set the coordinates of the circle in the box to the given color
    box[x_pixels, y_pixels] = 1

    return box


def make_cursor(radius: int, color: tuple=(255, 255, 255)) -> np.ndarray:
    """
    Make an RGBA cursor with a given radius and color.

    Args:
        radius: the radius of the circle cursor to make
        color: the color of the circle to make

    Returns:
        a numpy tensor with shape (2 * radius + 1, 2 * radius + 1, 4)

    """
    # create a matrix with a circle in it
    circle = make_circle(radius)[..., None]
    # create a circle in a matrix and assign the color
    circle_image = np.concatenate(3 * [circle], axis=-1) * color
    # add an alpha channel
    return np.concatenate([circle_image, 255 * circle], axis=-1)


# explicitly define the outward facing API of this module
__all__ = [make_circle.__name__, make_cursor.__name__]
