# coding: utf8
'''
Script containing the method to combine images
'''
from PIL import Image

def combineImage(img_1, img_2, offset_x, offset_y):
    '''
    Method called by prediction script to recombine the original image from its fragments

    :param Image img_1: image to attach the new fragment to
    :param Image img_2: new image fragment
    :param int offser_x: offset in the original image on the x axis of the current fragment (img_2)
    :param int offser_x: offset in the original image on the y axis of the current fragment (img_1)
    '''
    img_1.paste(img_2, (offset_x, offset_y))
    return img_1
