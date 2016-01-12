import sys
sys.path.append(".")
import csv
import numpy as np
from datasets import Photo
import cv2

def f1_score(precision, recall):
    return 2*precision*recall/(precision+recall)

def detect_faces(detector, image):
    """
    Input: a face detector and an image, you may prorivde a detector as this:
    *** detector = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml") ***
    Output: the faces locations (x, y, width, height)
    """
    #convert to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the image
    faces = detector.detectMultiScale(
        gray,
        scaleFactor=1.05,
        #scaleFactor=1.2,
        minNeighbors=8,
        minSize=(10, 10),
        flags = cv2.CASCADE_SCALE_IMAGE
    )
    return faces

def build_photos_from_csv(file_path):
    """
    Read the CSV and return a list of photos with labeled faces.
    """
    P = []
    image_IDs = set()
    for(image_ID, x, y, w, h, tag) in csv.reader(open(file_path), delimiter = ","):
        #each line is a face
        if image_ID == "image_ID": # header
            continue
        if image_ID not in image_IDs: 
            P.append(Photo(image_ID)) # new a photo
            image_IDs.add(image_ID)
        P[-1].add_face(x, y, w, h, tag) # add this face
    return P

def weighted_precision_recall(trueY, predY, sample_weight = None):
    """
    Calculate the weighted precisions and recalls for each lind of labels.
    """
    if sample_weight is None:
        sample_weight = np.array([1.0 for i in range(len(trueY))])
    scores = []
    for label in [0, 1, 2]:
        hit = 0.0
        deno_r = 0.0
        deno_p = 0.0
        index = 0
        for (ty, py) in zip(trueY, predY):
            if ty == label:
                deno_r += sample_weight[index]
            if py == label:
                deno_p += sample_weight[index]
                if py == ty:
                    hit += sample_weight[index]
            index += 1
        p = 0
        r = 0
        try:
            p = hit / deno_p
        except:
            pass
        try:    
            r = hit / deno_r 
        except:
            pass
        scores.extend([p, r])
    return scores

def read_training_data(csv_path, image_prefix = None, category = False, sample_weight = False):
    """
    Read training data from csv file and extract features.
    image_prefix : the folder that contains the images
    category : whether to return the category(image_ID) for each face - used for labelKFold
    sample_weight : whether to return the sample weights of each face
    """
    
    P = build_photos_from_csv(csv_path)
    if image_prefix is not None:
        for p in P:
            p.read_image(image_prefix+"/"+p.image_ID)
    
    categories = [] 
    sample_weights = [] 
    X = []
    Y = []
    
    #build training data
    for p in P:
        p.extract_features()
        for f in p.faces:
            X.append(f.feature)
            Y.append(f.label)
            categories.append(p.image_ID) #make sure the faces in the same image would not be separated when using labelKFold
            sample_weights.append(1.0/len(p.faces)) #more faces in a image -> less important?
    sample_weights = np.array(sample_weights)
    X = np.array(X)
    Y = np.array(Y)

    if category is False and  sample_weight is False:
        return (X, Y)
    elif category is False:
        return (X, Y, sample_weights)
    elif sample_weight is False:
        return (X, Y, categories)
    else:
        return (X, Y, categories, sample_weights)
