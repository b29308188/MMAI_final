This is the 2015 Fall MMAI final project.
We enhance the performance of face recongition in the OpenCv by machine learning methods.
There are 3 kinds of tags in our data:
(1) T: Subject people face 
(2) F: Non-subject people face
(3) N: Not a face

Environment :
	python 2.7.9, 
	OpenCV(cv2) 3.0, 
	numpy 1.9.2, 
	sklearn 0.17
	pandas 0.17

Description and Usage:
	Please type in the following command with python interpreter under the ./src directory.

(1) tagger.py : This scipt helps people tag the images in the input folders and output a tagged csv file.
Also, it separates the faced and non-faced images by moving them into different folders.
Usage : python tagger.py input_folder face_folder nonface_folder

(2) make_consensus.py : This script takes 3 tagged csv files as inputs and ouputs their consensus of each face tag with the weight (1.1, 1, 1).
Usage : python make_consensus csv_file1 csv_file2 csv_file3 output_csv_file

(3) valid.py : This scipt does the n-fold cross validation for the input tagged csv and the images.
Usage : python valid.py csv_file image_folder

""" To TRAIN a model and DEMO with the visualized results, you may execute (4) and use the output model in (5). """

(4) train.py : This scipt trains on the tagged csv file and the images, and it then stores the model in the model_path.
Usage : python train.py csv_file image_folder model_path

(5) demo.py : This scipt uses learned model to predict the tags of the faces. 
It may shows the comparison of the original face-detected image and the refined one.

(6) datasets.py : Define Photo class and Face class in this file.
NOTE : If you would like to add new features, you should modify the "extract_feature()" function in this file.

(7) model.py : Wrap the machine learning models from sklearn.
NOTE : If you would like to try different models or different parameters, you should modify this file.

(8) utils.py : Implement some other frequent functions used for the above scripts.
