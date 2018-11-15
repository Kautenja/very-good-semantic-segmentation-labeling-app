"""The main entry point for the data labeler."""
import argparse
import numpy as np
from PIL import Image
from src.data_labeler import DataLabeler


# create an argument parser to read arguments from the command line
PARSER = argparse.ArgumentParser(description=__doc__)
# add an argument for the image to segment
PARSER.add_argument('--image', '-i',
    type=str,
    help='TODO.',
    required=True,
)
# add an argument for the an existing segmentation to start with
PARSER.add_argument('--segmentation', '-s',
    type=str,
    help='TODO.',
    required=False,
    default=None,
)


# parse the options from the command line
ARGS = PARSER.parse_args()


with Image.open(ARGS.image) as image_file:
    ARGS.image = np.array(image_file)


if ARGS.segmentation is not None:
    with Image.open(ARGS.segmentation) as segmentation_file:
        ARGS.segmentation = np.array(segmentation_file)


LABELER = DataLabeler(ARGS.image, ARGS.segmentation)
