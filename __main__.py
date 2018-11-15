"""The main entry point for the data labeler."""
import argparse
import ast
import numpy as np
import pandas as pd
from PIL import Image
from src.data_labeler import DataLabeler


# create an argument parser to read arguments from the command line
PARSER = argparse.ArgumentParser(description=__doc__)
# add an argument for the image to segment
PARSER.add_argument('--image', '-i',
    type=str,
    help='the input image to segment.',
    required=True,
)
# add an argument for the labeling metadata
PARSER.add_argument('--metadata', '-m',
    type=str,
    help='the labeling metadata as a .csv file.',
    required=True,
)
# add an argument for the an existing segmentation to start with
PARSER.add_argument('--segmentation', '-s',
    type=str,
    help='the a priori segmentation if there is one.',
    required=False,
    default=None,
)


# parse the options from the command line
ARGS = PARSER.parse_args()


# load the input image to segment
with Image.open(ARGS.image) as image_file:
    ARGS.image = np.array(image_file)


# load the metadata
ARGS.metadata = pd.read_csv(ARGS.metadata)
ARGS.metadata['rgb'] = ARGS.metadata['rgb'].apply(ast.literal_eval)


# load the a priori segmentation if there is one
if ARGS.segmentation is not None:
    with Image.open(ARGS.segmentation) as segmentation_file:
        ARGS.segmentation = np.array(segmentation_file)


# create the data labeler application
LABELER = DataLabeler(ARGS.image, ARGS.metadata, ARGS.segmentation)
# run the data labeler application
LABELER.run()
