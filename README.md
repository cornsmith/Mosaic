# Mosaic Maker
Create a mosaic from any image using your own images as tiles.  

1. Build tile set
2. Process image

## 1. Build tile set
__python tiles.py dir_name tile_file max_pixel__  
The tile file is a numpy zip file consisting of the data of each image (RGBA as numpy array), main colour of each image, and the maximum height / width of the tile set.

## 2. Process image
__python in_file out_file tile_file__
Takes the input file and creates a mosaic using the tile file and saves as the output file.

### Requirements
Python 3.x
numpy
scipy
PIL


