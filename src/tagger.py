import cv2
import sys
import glob
import os
import pandas as pd

def detect_faces(detector, image):
    """
    Input: a face detector and an image
    Output: the faces locations (x, y, width, height)
    """
    #convert to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the image
    faces = detector.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=5,
        minSize=(10, 10),
        flags = cv2.CASCADE_SCALE_IMAGE
    )
    
    return faces


if __name__  == "__main__":
    
    try:
        #folder that contains untagged images
        input_folder = sys.argv[1]

        #folder that contains tagged images
        output_folder = sys.argv[2]
        
        #folder that contains images without faces
        removed_folder = sys.argv[3]
    except:
        sys.exit("Usage: python [input_foler] [output_folder] [removed_folder]" ) 
    
    if not os.path.exists(input_folder):
        sys.exit("Input folder not exists!!!!" )
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    if not os.path.exists(removed_folder):
        os.makedirs(removed_folder)
    
    if not os.path.exists(output_folder + "/"+ "tag_file.csv"):
        #no tag before : create a new one
        df = pd.DataFrame(columns = ("image_ID", "x", "y", "width", "height","tag"))
    else:
        # read the tag file as a pandas DataFrame
        df = pd.read_csv(output_folder + "/"+ "tag_file.csv")


    # Create the haar cascade
    detector = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

    # for each image in the folder
    for image_path in glob.glob(input_folder+"/*.jpg"):
        #remove the folder prefix and get the image ID
        image_ID = image_path.replace(input_folder, "")
        
        #if already tagged
        if image_ID in df['image_ID'].values:
            continue

        # Read the image
        image = cv2.imread(image_path)
        
        #detect faces
        faces = detect_faces(detector, image)
        print "find %d faces in image %s "% (len(faces), image_path)
        
        #no faces, then move this image to remove folder and go to the next image
        if len(faces) == 0:
                os.rename(image_path, removed_folder + "/" +image_ID)
                continue
        
        tuples = [] # list of (image_ID, face, tag)
        for (x, y, w, h)  in faces:
            # Draw a rectangle around the faces
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            #show image
            cv2.imshow("img", image)
            
            """
            wait for keys:
            t : true for tag
            f : false for tag
            n : not a face
            """
            key = ""
            while key != ord("t") and key != ord("f") and key != ord("n") :
                key = cv2.waitKey()
            if key == ord("t"):
                cv2.putText(image, "T", (x, y), cv2.FONT_HERSHEY_SIMPLEX,2, 255, thickness = 3)
                tag = "T" 
            if key == ord("f"):
                cv2.putText(image, "F", (x, y), cv2.FONT_HERSHEY_SIMPLEX,2, 255, thickness = 3)
                tag = "F" 
            if key == ord("n"):
                cv2.putText(image, "N", (x, y), cv2.FONT_HERSHEY_SIMPLEX,2, 255, thickness = 3)
                tag = "N" 
            tuples.append((image_ID, x, y, w, h, tag))
        
        #show the final tagged image
        cv2.imshow("img", image)
        """
        wait for keys:
        27: esc
        32: space
        """
        while key != 27 and key != 32:
            key = cv2.waitKey()
        if key == 27:# write the DataFrame into the csv file WITHOUT the current tags in this image
            df.to_csv(output_folder + "/" + "tag_file.csv", index = False)
            cv2.destroyAllWindows()
            sys.exit("Exit!")
        else: # space : add the tags into the DataFrame
            for t in tuples:
                df.loc[len(df)] =  t
            #finish tag this image : move it to taggedoutput folder
            os.rename(image_path, output_folder + "/" +image_ID)

        cv2.destroyAllWindows()
        
    # write the DataFrame into the csv file 
    df.to_csv(output_folder + "/" +"tag_file.csv", index = False)
