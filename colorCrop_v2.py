'''
This file contains the methods needed to colour an image according to the prediction of the neural network
'''
from PIL import Image

def evaluatePrediction(prediction):
    '''
    Method called to compute the alpha value of the red mask to apply to the image slice, based on the value of the prediction

    :param float prediction: Prediction value
    '''
    if prediction < 0.5:
        return 255
    return int((1-prediction)*255+100)

def applyOverlay(img, prediction):
    '''
    Method called to apply overlay to an image according to its prediction value

    :param np.array img: numpy array
    :param float prediction: Prediction value
    '''
    #Setting level of transparency of overlay
    alpha = evaluatePrediction(prediction)
    #create the coloured overlays
    red = Image.new('RGB',img.size,(255,0,0))
    #create a mask using RGBA to define an alpha channel to make the overlay transparent
    mask = Image.new('RGBA',img.size,(0,0,0,alpha))
    return Image.composite(img,red,mask).convert('RGB')
