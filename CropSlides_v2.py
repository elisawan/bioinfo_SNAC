# coding: utf8
'''
Script for cropping images

:dim_tile = dimension of each square tile
:overlap_tile = overlap of one tile with the next one
:level_tile = {0,1} level of detail (see DatasetAnalysis)

Output file name format: {original file name}_{start_x}_{start_y}.jpg
'''

from os import listdir
from os.path import isfile, split, join
import cv2
import numpy as np
import sys

'''
OpenSlide

:read_region - Return an RGBA Image containing the contents of the specified region. Unlike in the C interface, the image data is not premultiplied.
# Parameters:
:location tuple – (x, y) tuple giving the top left pixel in the level 0 reference frame
:level int – the level number
:size tuple – (width, height) tuple giving the region size
'''
# ##### I valori fanno riferimento all'immagine in level 0.... Facendo delle prove, il fattore di zoom dal livello 0 al livello 1 è 4

dim_tile = 224
overlap_tile = 50
level_tile = 1

def conv_l1tol0(n):
    return n*4

def conv_l0tol1(n):
    return int(n/4)

def cropImage(slide, offset_x, offset_y):
    '''
    Method called by prediction script to crop a .svs slide

    :param openslide object slide: an openslide object to crop from
    :param int offset_x:
    :param int offset_y:
    '''

    dim_x = slide.dimensions[0]
    dim_y = slide.dimensions[1]
    if(conv_l1tol0(offset_x+dim_tile) <= dim_x and conv_l1tol0(offset_y+dim_tile) <= dim_y):
        tile = slide.read_region((conv_l1tol0(offset_x),conv_l1tol0(offset_y)),level_tile,(dim_tile,dim_tile))
        tile = np.array(tile)
        return tile[...,:3]
    sys.exit("CropSlides - cropImage: failed")

def get_jpg(slide, file_name):
    dim_x = slide.dimensions[0]
    dim_y = slide.dimensions[1]
    img = slide.read_region((0,0),level_tile,(conv_l0tol1(dim_x),conv_l0tol1(dim_y))).convert('RGB').save(file_name)
