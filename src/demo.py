import sys
sys.path.append(".")
import cPickle
import numpy as np
import cv2
import glob
from utils import detect_faces
from datasets import Photo, inv_label_maps

if __name__ == "__main__":
    print "USAGE : python predict.py model_path (-d image_predfix)/(image_path) "
    model_path = sys.argv[1]
    if sys.argv[2] == "-d":
        image_prefix = sys.argv[3]
        image_list = [ image_path for image_path in sorted(glob.glob(image_prefix+"/*.[Jj][Pp][Gg]")) ]
    else:
        image_list = [sys.argv[2]]
    with open(model_path, "rb") as f:
        model = cPickle.load(f)

    
    for image_path in image_list:
        p = Photo()
        #before applying the filter
        image1 = cv2.imread(image_path)
        if image1 is None:
            print "no image", image_path
            continue
        detector = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
        faces = detect_faces(detector, image1)
        print "find %d faces in image %s "% (len(faces), image_path)
        faces = sorted(faces, key=lambda tup: tup[0])
        for (x, y, w, h) in faces:
            p.add_face(x, y, w, h)
            # Draw a rectangle around the faces
            cv2.rectangle(image1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        #after applying the filter
        #read image again to remove rectangles
        image2 = cv2.imread(image_path)
        p.read_image(image_path)
        p.extract_features()
        X = np.array([f.feature for f in p.faces])
        predY = model.predict(X)
        for (i, f) in enumerate(p.faces):
            if inv_label_maps[predY[i]] == 'T':
                cv2.rectangle(image2, (f.x, f.y), (f.x+f.w, f.y+f.h), (0, 255, 0), 2)
        
        image = np.concatenate((image1, image2), axis = 1)
        cv2.imshow("image", cv2.resize(image, (0, 0), fx = 0.5, fy = 0.5))
        key = cv2.waitKey()
        cv2.destroyAllWindows()
        if key == 27: # esc
            sys.exit("Exit!")


