# -*- coding: utf-8 -*-
"""
Description: Processes image using tile file and saves to a new image
Usage: python in_file out_file tile_file
Input:
    in_file - the location and name of the image to process
    out_file - the location and name of the new image to save as
    tile_file - the location of the saved tile_file created using tiles.py
Output:
    a new mosaic-processed image, 125 max resolution
"""

import sys
import numpy as np
import random
from PIL import Image
from scipy.spatial import KDTree
from scipy.misc import imsave

MAX_RES = 125

def process_image(image_name, colours, thumbs, thumbsize):
    # KD Tree for Nearest-Neighbour
    kdt = KDTree(colours)

    # open image and make it smaller
    img = Image.open(image_name).convert('RGBA')
    img.thumbnail((MAX_RES, MAX_RES))
    img_data = np.array(img)

    # initialise new image
    new_shape = (
        img_data.shape[0] * thumbsize,
        img_data.shape[1] * thumbsize,
        img_data.shape[2]
    )
    new_image = np.zeros(new_shape, dtype=np.float)

    # populate new image
    for x in range(img_data.shape[0]):
        for y in range(img_data.shape[1]):
            _, nn_idx = kdt.query(img_data[x, y, :], k=3)
            thumb_img = thumbs[random.choice(nn_idx)] # TODO: change to distance-weighted probabilities
            x1 = (x * thumbsize)
            x2 = x1 + thumb_img.shape[0]
            y1 = (y * thumbsize)
            y2 = y1 + thumb_img.shape[1]
            new_image[x1:x2, y1:y2, :] = thumb_img
    return new_image


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print('Usage: python in_file out_file tile_file')
        exit()
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    tile_file = sys.argv[3]

    print('Loading data...')
    with np.load(tile_file) as tiles:
        colours=tiles['colours']
        thumbs=tiles['thumbs']
        thumbsize=int(tiles['size'])

    print('Processing image...')
    new_image = process_image(in_file, colours, thumbs, thumbsize)

    print('Saving new image...')
    imsave(out_file, new_image)