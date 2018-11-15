"""A method to segment image."""
from skimage.color import rgb2gray
from skimage.filters import sobel
from skimage.segmentation import felzenszwalb
from skimage.segmentation import slic
from skimage.segmentation import quickshift
from skimage.segmentation import watershed
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float


# a list of segmentation algorithms supported by this module
SEGMENTATION_LIST = [felzenszwalb, slic, quickshift, watershed]
# a mapping of string method names to their references in memory
SEGMENTATION = {alg.__name__: alg for alg in SEGMENTATION_LIST}



def segment(image, algorithm: str, mark: bool=True, **kwargs):
    """
    Segment an input image using given segmentation algorithm and params.

    Args:
        image: the image to segment
        algorithm: the string name of the skimage segmentation algorithm to use
        mark: whether to return the marked image (True) or segments (False)
        kwargs: the key word arguments to pass to the segmentation algorithm

    Returns:
        a segmented image if mark is true, otherwise a segmentation map

    """
    # try to unwrap the method using string name
    try:
        segment_image = SEGMENTATION[algorithm]
    except KeyError:
        raise ValueError('{} is not a valid segmentation algorithm')
    # if the image is in [0, 255], convert the image to [0, 1]
    if str(image.dtype) == 'uint8':
        image = img_as_float(image)
    # if the algorithm is watershed, apply sobel and grayscale first
    if algorithm == 'watershed':
        image = sobel(rgb2gray(image))
    # apply the segmentation algorithm with given key word arguments
    segmentation = segment_image(image, **kwargs)
    # if mark, return the original image with marked boundaries
    if mark:
        return (255 * mark_boundaries(image, segmentation)).astype('uint8')
    # otherwise return the segmentation as is
    return segmentation


# define the outward facing API of this module
__all__ = [segment.__name__]
