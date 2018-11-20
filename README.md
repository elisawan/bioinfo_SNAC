## Synopsis

This project is focused on the digital pathology field.
Pathologists perform diagnosis based on the visualization of histological samples.
Usually the examination is visual: doctors look for abnormalities and decides for a diagnosis

We developed a system that can take in input a WSI (whole histological image) and create a attention map for cancer detection.

The WSI is passed to a trained neural network that performs the prediction and delivers the final result

## Motivation

The project was developed and delivered for the Bioinformatic (01OVFOV) course at **Politecnico di Torino**, held by professor Elisa Ficarra, by Group 6 (Elisa Wan, Andrea Grippi, Silvia Fornara, Greta Berardengo)

## Installation

Before using the prediction script make sure to have all the requirements available on your system.
You can run:

```python
$ pip install -r requirements.txt
```

## Structure of the SNAC package
1. colorCrop_v2.py
2. CombineSlides_v2.py
3. CropSlides_v2.py
4. predictionScript_v2.py
5. models/
	1. 2classes/
		1. vgg16
		2. inceptionResNetV2
		3. basic-NN
	2. 3classes/
		1. vgg16
		2. inceptionResNetV2
		3. basic-NN
6. results/
7. tools/
	1. DatasetAnalysis.py
	2. WhiteImagesDetection.py

## API Reference

Information on classes, methods and files are attached to this html documentation.

## Tests

To use this prediction software, just type on your command line:

```python
$ python predictionScript.py {class_of_interest} {model_path} {number_classes} {image_folder}
```

* class_of_interest indicates the type of tissue you want highlighted in the attention map. It can take one of the following values: H, non-H, AC, AD.
* model_name is the name of the model to be used for prediction. It should be chosen from one of the available pretrained models: inceptionResNetV2, vgg-16 or basic_NN.
* number_classes number of classes on which the model has been trained on. It can be 2 (H, non-H) or 3 (H, AC, AD).
* image_folder is the path of the folder containing images you want to get a prediction of.

Note: Models trained on 2 classes only support class_of_interest = H or non-H.
      Models trained on 3 classes support class_of_interest = H, AC or AD.

## License

Delivered with licence GNU GPL v3
