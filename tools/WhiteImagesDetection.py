
# coding: utf-8
'''
Determine whether a crop contains meaningful informations or it's almost all white, using OpenCV
 

pixel_th = 127. Valore sopra il quale il colore del pixel è considerato bianco  
image_th = 0.8. Se più dell'80% dell'immagine è bianca, la consideriamo non significativa
'''
# In[102]:


import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image 
import os
from os import listdir
from os.path import isfile


# In[148]:


pixel_th = 215
image_th = 0.5


# In[111]:


allcrop_dir = 'crop/'
trash_dir = 'trash/'


# In[149]:


count_white_img = 0
for file_name in listdir(allcrop_dir):
    if isfile(allcrop_dir+file_name):
        img = Image.open(allcrop_dir+file_name)
        img = img.convert('L')
        img = np.array(img)
        ret,thresh1 = cv2.threshold(img,pixel_th,255,cv2.THRESH_BINARY)
        count = 0
        tot = 0
        for p in np.nditer(thresh1):
            if p == 255:
                count = count+1
            tot = tot+1
        if count/tot > image_th:
            print("meaningless image: all white, moving it...")
            os.rename(allcrop_dir+file_name,trash_dir+file_name)
            count_white_img = count_white_img + 1
print("totale immagini spostate: " + str(count_white_img))


# In[141]:


type(thresh1)


# In[140]:


thresh1[0].shape

