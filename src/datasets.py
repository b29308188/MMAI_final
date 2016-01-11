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

    def histogram(self, img):
        
        Orishape = img.shape
        hist = []
        img = img.reshape((img.shape[0]*img.shape[1]*img.shape[2]),order='F')
        hist += list(np.histogram(img[0:Orishape[0]*Orishape[1]], bins=np.arange(0,257,64))[0])
        hist += list(np.histogram(img[Orishape[0]*Orishape[1]:2*Orishape[0]*Orishape[1]], bins=np.arange(0,257,64))[0])
        hist += list(np.histogram(img[2*Orishape[0]*Orishape[1]:3*Orishape[0]*Orishape[1]], bins=np.arange(0,257,32))[0])

        return hist

    def colorgram(self, img):
        cgram = []
        for i in xrange(3): # RGB
            #cgram += [np.mean(img[0:,0:,i]), np.var(img[0:,0:,i])]
            cgram += [np.mean(img[0:,0:,i]), np.std(img[0:,0:,i])]
        return cgram

    def get_global_features(self):
        gfs = []
        gfs += [len(self.faces)] # number of faces in this image
        average_distance = 0.
        self.disMatrix = np.zeros((len(self.faces), len(self.faces)))
        for i, f1 in enumerate(self.faces):
            for j, f2 in enumerate(self.faces):
                dis = np.sqrt(((f1.x+f1.w/2) - (f2.x+f2.w/2))**2 + ((f1.y+f1.h/2) - (f2.y+f2.h/2))**2) #l2 dis
                #dis = np.absolute((f1.x+f1.w/2) - (f2.x+f2.w/2)) + np.absolute((f1.y+f1.h/2) - (f2.y+f2.h/2)) #l1 dis
                #dis = ((f1.x * f2.x) + (f1.y * f2.y))/np.sqrt((f1.x**2+f1.y**2) * (f2.x**2+f2.y**2)) # cos dis
                # dis = np.sqrt((float((f1.x+f1.w/2) - (f2.x+f2.w/2))/self.image.shape[0])**2 + \
                #     (float((f1.y+f1.h/2) - (f2.y+f2.h/2))/self.image.shape[1])**2) # weighted l2 dis
                self.disMatrix[i, j] = dis
                average_distance += dis
        #gfs += [average_distance/(len(self.faces)*(len(self.faces)-1)/2)]
        self.global_feature = gfs

    def local_features(self, f, no):
        lfs = [f.x, f.y, f.w, f.h] 
        lfs += self.colorgram(self.image[f.y : f.y+f.h, f.x : f.x+f.w])
        lfs += [np.var(self.disMatrix[no, :]), np.mean(self.disMatrix[no, :])] # average distance to other faces
        #lfs += [f.w * f.h] # size
        lfs += [f.x+f.w/2, f.y+f.h/2] # center

        NinR = 0.0
        R = 0.4 * self.image.shape[0]# percentage of image's width
        for i in xrange(len(self.faces)):
            if self.disMatrix[no, i] < R :
                NinR += 1
            #print self.disMatrix[no, i]

        lfs += [NinR/len(self.faces)]
        #lfs += self.histogram(self.image[f.y : f.y+f.h, f.x : f.x+f.w])
        return lfs

    
    def extract_features(self):
        """
        For each face in the list of faces, extract its features.
        """
        self.get_global_features()
        for i, f in enumerate(self.faces):
            if self.image is not None:
                f.feature = np.array(self.local_features(f, i) + self.global_feature )
            else:
                f.feature = np.array([f.x, f.y, f.w, f.h])

    




         