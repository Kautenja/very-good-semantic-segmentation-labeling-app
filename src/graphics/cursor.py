"""A method for setting up a brush cursor."""
import numpy as np
import pyglet
from skimage.draw import circle as draw_circle


def make_circle(radius: int, dtype: str='uint8') -> np.ndarray:
    """
    Make a circle with a given radius.

    Args:
        radius: the radius of the circle to draw

    Returns:
        a NumPy matrix of size 2 * radius + 1 with a circle in it.

    """
    # if the radius is even, make it odd
    length = 2 * radius + 1
    # create an RGBA box to house the circle in
    box = np.zeros((length, length), dtype=dtype)
    # get the coordinates for the circle
    x_pixels, y_pixels = draw_circle(radius, radius, radius)
    # set the coordinates of the circle in the box
    box[x_pixels, y_pixels] = 1

    return box


def make_ring(inner_radius: int, outer_radius: int,
    dtype: str='uint8'
) -> np.ndarray:
    """
    Make a circle with a given radius.

    Args:
        inner_radius: the inner radius of the circle to draw
        outer_radius: the outer radius of the circle to draw

    Returns:
        a NumPy matrix of size 2 * radius + 1 with a circle in it.

    """
    # if the radius is even, make it odd
    length = 2 * outer_radius + 1
    # create an RGBA box to house the circle in
    box = np.zeros((length, length), dtype=dtype)
    # get the coordinates for the outer circle
    x_pixels, y_pixels = draw_circle(outer_radius, outer_radius, outer_radius)
    # set the coordinates of the circle in the box
    box[x_pixels, y_pixels] = 1
    # get the coordinates for the inner circle
    x_pixels, y_pixels = draw_circle(outer_radius, outer_radius, inner_radius)
    # set the coordinates of the circle in the box
    box[x_pixels, y_pixels] = 0

    return box


def make_cursor(circle: np.ndarray,
    color: tuple=(255, 255, 255)
) -> np.ndarray:
    """
    Make an RGBA cursor with a given radius and color.

    Args:
        circle: the matrix with the circle to make a cursor image from
        color: the color of the circle to make

    Returns:
        a NumPy tensor with shape (2 * radius + 1, 2 * radius + 1, 4)

    """
    # create a matrix with a circle in it
    circle = circle[..., None]
    # create a circle in a matrix and assign the color
    image = np.concatenate(3 * [circle], axis=-1) * color
    # add an alpha channel
    image = np.concatenate([image, 255 * circle], axis=-1).astype('uint8')

    return image


def pyglet_cursor(img: np.ndarray,
    img_format: str='RGBA'
) -> pyglet.window.ImageMouseCursor:
    """
    Return a pyglet mouse cursor from the given input image.

    Args:
        img: the image as an RGBA NumPy tensor
        format: the format of the image data

    Returns:
        an image mouse cursor for pyglet

    """
    # create an image data object from the NumPy tensor
    img_data = pyglet.image.ImageData(
        *img.shape[:-1],
        img_format,
        img.tobytes(),
        pitch=img.shape[1] * -len(img_format)
    )
    # create the "hot shape" of the pyglet cursor. i.e., the center of the
    # circle representing the cursor, which is centered in the square image
    hot_shape = int(img.shape[0] / 2), int(img.shape[1] / 2)
    # create the pyglet cursor object from the image data
    cursor = pyglet.window.ImageMouseCursor(img_data, *hot_shape)

    return cursor


# explicitly define the outward facing API of this module
__all__ = [
    make_circle.__name__,
    make_cursor.__name__,
    make_ring.__name__,
    pyglet_cursor.__name__,
]
