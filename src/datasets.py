import cv2
import numpy as np

#labels for each kind of tag
label_maps = {"T":0 , "F": 1, "N": 2}
inv_label_maps = {v : k  for (k, v) in label_maps.items()}

class Photo:
    """
    This class is a photo which contains a list of faces.
    image_ID : the ID of this photo 
    image : the path of the image
    """
    class Face:   
        """
        This class represents a face start in (x , y).
        w : width
        h : height
        tag : T/F/N
        label : numbers corresponding to the tag
        feature : the vector of features of this face
        """
        def __init__(self, x, y, w, h, tag = None):
            """
            This is the Constructor of Face
            """
            self.x = int(float(x))
            self.y = int(float(y))
            self.w = int(float(w))
            self.h = int(float(h))
            self.tag = tag
            if tag is not None:
                self.label = label_maps[tag]
            else:
                self.label = None
            self.feature = None

    def __init__(self, image_ID = None):
        """
        This is the constructor of Photo.
        """
        self.image_ID = image_ID
        self.faces = []
        self.image = None

    def read_image(self, image_path):
        """
        Read image from the image_path and store it in memory
        """
        self.image = cv2.imread(image_path)
        assert self.image is not None

    def add_face(self, x, y, w, h, tag = None):
        """
        Add a face to the list of faces.
        """
        self.faces.append( self.Face(x, y, w, h, tag) )
    
    def extract_features(self):
        """
        For each face in the list of faces, extract its features.
        """
        for f in self.faces:
            if self.image is not None:
                f.feature = np.array([f.x, f.y, f.w, f.h, np.mean(self.image[f.y : f.y+f.h, f.x : f.x+f.w])])
            else:
                f.feature = np.array([f.x, f.y, f.w, f.h])
