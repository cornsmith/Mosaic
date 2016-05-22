# Mosaic Maker
Create a mosaic from any image using your own images as tiles.  

## Functionality
Turn a picture into a mosaic where the tiles are:  
- a set of pictures  
- a colour palette from another picture (future release)  
- a given colour palette (future release)  
- a preset shape (future release)  

## Examples
Emojify
![girl input](examples/girl.jpg?raw=true)
![girl output](examples/girl-emoji.jpg?raw=true)

Fruits
![fruits input](examples/fruits.jpg?raw=true)
![fruits output](examples/fruits-fruits.jpg?raw=true)

## Usage
1. Build tile set
2. Process image

### 1. Build tile set
`python tiles.py dir_name tile_file max_pixel`  

The tile file is a numpy zip file consisting of the data of each image (RGBA as numpy array), main colour of each image, and the maximum height / width of the tile set.

### 2. Process image
`python in_file out_file tile_file`  

Takes the input file and creates a mosaic using the tile file and saves as the output file.

## Requirements
- Python 3.x  
- numpy  
- scipy  
- PIL  
