'''
1. crop svs images in tiles
2. predict
3. recombine tiles
'''
import tensorflow as tf
from keras.models import load_model
import sys
from os.path import isfile, split, join
from colorCrop_v2 import applyOverlay
import numpy as np
from PIL import Image
import CropSlides_v2 as cs
from CombineSlides_v2 import combineImage
from os import listdir
from os.path import isfile
import openslide
import cv2
import progressbar
import time
import h5py

dim_tile = 224
overlap_tile = 50
level_tile = 1
models_dir = "models"
result_folder = "./results/"

def get_prediction_index(target_class):
    '''
    convertion from class name to the corresponding index in the prediction array
    :param str target_class: class of interest

    # Supported classes
    H - Healthy
    Non-H - Not healthy
    AC - Adenocarcinoma
    AD - Adenoma
    '''
    if target_class == "H":
        return 0
    if target_class == "non-H":
        return 1
    if target_class == "AC":
        return 1
    if target_class == "AD":
        return 2
    else:
        return -1

def get_model(model_name, num_classes):

    '''
    retreave requested model from the available repository and loads it
    :param string model_name
    :param int number of classes the model was trained on
    return a trained keras model
    '''

    num_classes = int(num_classes)
    if(num_classes == 2):
        if(model_name == "vgg-16"):
            return load_model(join(models_dir,"vgg_2.h5"))
        if(model_name == "inceptionResNetV2"):
            model = tf.keras.applications.InceptionResNetV2(input_shape=(224,224,3), weights=None, include_top=True, classes=2)
            model.load_weights(join(models_dir,"inception_2.h5"))
            return model
        if(model_name == "basic-NN"):
            return load_model(join(models_dir,"basic-NN_2.h5"))
    if(num_classes == 3):
        if(model_name == "vgg-16"):
            return load_model(join(models_dir,"vgg_3.h5"))
        if(model_name == "inceptionResNetV2"):
            model = tf.keras.applications.InceptionResNetV2(input_shape=(224,224,3), weights=None, include_top=True, classes=3)
            model.load_weights(join(models_dir,"inception_3.h5"))
            return model
        if(model_name == "basic-NN"):
            return load_model(join(models_dir,"basic-NN_3.h5"))
    sys.exit("failed to load model")


def set_results_folder(model_name, num_classes):
    '''
    return the correct folder to store the prediction results
    '''
    return join(join("./results",str(num_classes)+"classes"),model_name)


def create_attention_map(target_class, model_name, num_classes, slide_folder_path):
    '''
    main function

    :param str target_class: class of intrest. Choose from: "H","non-H","AC","AD"
    :param str model_h5: path to the .h5 file of the trained model to be used for prediction
    :param str test_image_path: path to the folder where test images (.svs format) are stored
    :param str tile_dest_folder: path to the existing folder where the cropped files will be stored
    '''
    start_time = time.time()
    print("Loading model: " + model_name)
    model = get_model(model_name, num_classes)

    prediction_index = get_prediction_index(target_class)
    if(prediction_index == -1):
        exit("Unsupported label")

    print("class of interest "+str(prediction_index)+"-"+target_class)

    result_folder = set_results_folder(model_name, num_classes)

    for slide_name in listdir(slide_folder_path):
        output_file = open(join(result_folder,slide_name.split(".")[0]+"_"+target_class+".txt"), "w")
        output_file.write("slide: "+slide_name)
        output_file.write("target_class:"+target_class)

        slide = openslide.OpenSlide(join(slide_folder_path,slide_name))
        cs.get_jpg(slide,join(result_folder,slide_name.split(".")[0]+"_original.jpg"))
        dim_x = slide.dimensions[0]
        dim_y = slide.dimensions[1]

        img_out = Image.new('RGB', (cs.conv_l0tol1(dim_x), cs.conv_l0tol1(dim_y)))
        i = 0
        j = 0

        bar = progressbar.ProgressBar(widgets=[progressbar.Percentage(),progressbar.Bar(),], max_value=int(dim_x/224)*int(dim_y/224)).start()
        k = 0
        while(cs.conv_l1tol0(i+dim_tile) <= dim_x):
            while(cs.conv_l1tol0(j+dim_tile) <= dim_y):

                crop = cs.cropImage(slide,i,j)

                crop_pred = (crop-128)/128
                crop_pred = np.expand_dims(crop, axis=0)
                prediction = model.predict(crop_pred)
                output_file.write("("+str(i)+","+str(j)+") "+str(prediction))
                #print(prediction[0][prediction_index])
                crop_colored = Image.fromarray(crop.astype('uint8'), 'RGB')
                crop_colored = applyOverlay(crop_colored, prediction[0][prediction_index])

                #crop_colored.save(str(k)+".jpg")
                #k = k+1
                img_out = combineImage(img_out,crop_colored, i, j)

                j = j+dim_tile-overlap_tile

                time.sleep(0.1)
                bar.update(i + 1)
            i = i+dim_tile-overlap_tile
            j = 0

        output_name = slide_name.split(".")[0]+"_"+target_class+".jpg"
        img_out.save(join(result_folder,output_name))

        bar.finish()

        print("output file "+ output_name+" has been saved in: "+result_folder)

        end_time = time.time()
        print("duration: "+str(end_time-start_time))

if(__name__== "__main__"):
    if(len(sys.argv) != 5):
        sys.exit("Usage: python predictionScript.py <target class> <CNN model name> <number of classes> <test image location>")
    create_attention_map(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
