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
        self.image = cv2.resize(cv2.imread(image_path), (960, 720))
        assert self.image is not None

    def add_face(self, x, y, w, h, tag = None):
        """
        Add a face to the list of faces.
        """
        self.faces.append( self.Face(x, y, w, h, tag) )
    def histogram(self, img):
        
        Orishape = img.shape
        hist = []
        img = img.reshape((img.shape[0]*img.shape[1]*img.shape[2]),order='F')
        a = np.histogram(img[0:Orishape[0]*Orishape[1]], bins=np.arange(0,257,64))[0]
        hist += list(a.astype(float)/np.sum(a))
        b = np.histogram(img[Orishape[0]*Orishape[1]:2*Orishape[0]*Orishape[1]], bins=np.arange(0,257,64))[0]
        hist += list(b.astype(float)/np.sum(b))
        c = np.histogram(img[2*Orishape[0]*Orishape[1]:3*Orishape[0]*Orishape[1]], bins=np.arange(0,257,32))[0]
        hist += list(c.astype(float)/np.sum(c))
        return hist
    
    def colorgram(self, img):
        cgram = []
        for i in xrange(3): # RGB
            cgram += [np.mean(img[0:,0:,i]), np.std(img[0:,0:,i])]
        return cgram

    def get_global_features(self):
        gfs = []
        gfs += [len(self.faces), self.image.shape[0]*self.image.shape[1]] # number of faces in this image
        gfs += [np.mean([f.x for f in self.faces]), np.var([f.x for f in self.faces])]
        gfs += [np.mean([f.y for f in self.faces]), np.var([f.y for f in self.faces])]
        gfs += [np.mean([f.w for f in self.faces]), np.var([f.w for f in self.faces])]
        gfs += [np.mean([f.h for f in self.faces]), np.var([f.h for f in self.faces])]
        average_distance = 0.
        self.disMatrix = np.zeros((len(self.faces), len(self.faces)))
        for i, f1 in enumerate(self.faces):
            for j, f2 in enumerate(self.faces):
                dis = np.sqrt(((f1.x+f1.w/2) - (f2.x+f2.w/2))**2 + ((f1.y+f1.h/2) - (f2.y+f2.h/2))**2) #l2 dis
                self.disMatrix[i, j] = dis
                average_distance += dis
        self.global_feature = gfs

    def local_features(self, f, no):
        lfs = [f.x, f.y, f.w, f.h]
        lfs += self.colorgram(self.image[f.y : f.y+f.h, f.x : f.x+f.w])

        lfs += [np.var(self.disMatrix[no, :]), np.mean(self.disMatrix[no, :])] # average distance to other faces
        lfs += [f.x+f.w/2, f.y+f.h/2] # center
        
        NinR = 0.0
        R = 0.4 * self.image.shape[0]# percentage of image's width
        for i in xrange(len(self.faces)):
            if self.disMatrix[no, i] < R :
                NinR += 1

        lfs += [NinR/len(self.faces)]
        return lfs

    
    def extract_features(self):
        """
        For each face in the list of faces, extract its features.
        """
        if self.image is not None:
            self.get_global_features()
        for i, f in enumerate(self.faces):
            if self.image is not None:
                f.feature = np.array(self.local_features(f, i) + self.global_feature )
            else:
                f.feature = np.array([float(f.w*f.h)])

    




         
