# -*- coding: utf-8 -*-
"""
Description: Pre-processing to create tile data from a directory of images
Usage: python tiles.py dir_name tile_file max_pixel
Input:
    dir_name - the directory of images to use as tiles without trailing slash,
        e.g. "./Images"
    tile_file - the location and name of the saved output tile file,
        e.g. "tiles.npz"
    max_pixel - the maximum height or width tile size in pixels
Output:
    numpy zip of 3 arrays:
        colours - the main colour of each image
        thumbs - the thumbnail of each image
        size - the maximum height / width of thumbnails
"""

import os
import sys
import numpy as np
from scipy.cluster.vq import kmeans
from PIL import Image
from collections import Counter


def get_main_colour(data, method='kmeans', remove_bw=True):
    """
    kmeans - (k=1) on image, taking out all whites and blacks
    quantcount - quantized count using hex transformation
    """
    def rgb_to_hex(rgb, quantize=True):
        rgb = tuple(rgb.astype(int))
        if quantize:
            rgb = (
                int(rgb[0] / 255 * 51) * 5,
                int(rgb[1] / 255 * 51) * 5,
                int(rgb[2] / 255 * 51) * 5
            )
        return '%02x%02x%02x' % rgb

    def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def get_hex_counts(data):
        hex_data = np.apply_along_axis(rgb_to_hex, 1, data)
        hex_count = Counter(hex_data)
        del hex_count['ffffff']
        del hex_count['000000']
        return hex_count

    data = data.reshape((data.shape[0] * data.shape[1], data.shape[2])).astype(float)

    # take out black and white
    if remove_bw:
        ix = np.all(
            [
                (data != np.array([255, 255, 255, 0])).any(axis=1),
                (data != np.array([0, 0, 0, 0])).any(axis=1)
            ],
            axis=0
        )
        data = data[ix, ]

    if method == 'kmeans':
        clust = kmeans(data, 1)
        main_colours = clust[0]

    if method == 'quantcount':
        colour_counts = get_hex_counts(data)
        total = sum(colour_counts.values())
        main_colours = []
        running_count = 0.0

        for c in sorted(colour_counts, key=colour_counts.get, reverse=True):
            if running_count < 0.6: # TODO: parameterise threshold?
                running_count += colour_counts[c] / total
                main_colours.append(hex_to_rgb(c))

    return main_colours

def read_tiles(dir_name):
    main_colours = []
    thumbs = []

    files = os.listdir(dir_name)
    n_files = len(files)
    print(n_files, 'images found')

    n_file = 0
    for filename in files:
        n_file += 1
        print('Processing', filename, n_file)
        img = Image.open(dir_name + '/' + filename).convert('RGBA')
        img_data = np.array(img)
        img.thumbnail((max_pixel, max_pixel))
        thumbs.append(np.array(img))
        main_colours.append(get_main_colour(img_data))

    main_colours = np.vstack(main_colours)
    return main_colours, thumbs

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Usage: python tiles.py dir_name tile_file max_pixel')
        exit()
    dir_name = sys.argv[1]
    tile_file = sys.argv[2]
    if len(sys.argv) == 4:
        max_pixel = sys.argv[3]
    else:
        max_pixel = 60

    main_colours, thumbs = read_tiles(dir_name)
    np.savez(tile_file, colours=main_colours, thumbs=thumbs, size=max_pixel)
