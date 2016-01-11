from Tkinter import *
from PIL import ImageTk, Image
import cv2
import time
import pandas as pd
from camera import Camera
import os
import sys


count = 0
images_prefix = "images/"
imagenames = [images_prefix+"img7.jpg",images_prefix+"img81.jpg",images_prefix+"img203.jpg"]


Cam = Camera(model_path="../100_basic_SVC1.model")

dump_csv = "output.csv"
images_folder = "images/"



class GUIDemo(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.images = None
        
        
        if not os.path.exists(dump_csv):
            #no tag before : create a new one
            self.df = pd.DataFrame(columns = ("image_ID", "face_ID", "x", "y", "width", "height", "tag", "name"))
        else:
            # read the tag file as a pandas DataFrame
            self.df = pd.read_csv(dump_csv)

        self.num_images = len(set(self.df['image_ID'].tolist()))
        
        
 
    def createWidgets(self):
        self.numberText = Label(self)
        self.numberText["text"] = "Number:"
        self.numberText.grid(row=0, column=1)
        self.numberField = Entry(self)
        self.numberField["width"] = 50
        self.numberField.grid(row=0, column=2, columnspan=6)
 
        self.nameText = Label(self)
        self.nameText["text"] = "Name:"
        self.nameText.grid(row=1, column=1)
        self.nameField = Entry(self)
        self.nameField["width"] = 50
        self.nameField.grid(row=1, column=2, columnspan=6)
         
        # self.new = Button(self)
        # self.new["text"] = "New"
        # self.new.grid(row=2, column=0)
        # self.new["command"] =  self.newMethod
        # self.load = Button(self)
        # self.load["text"] = "Load"
        # self.load.grid(row=2, column=1)
        # self.load["command"] =  self.loadMethod
        self.tag = Button(self)
        self.tag["text"] = "Tag"
        self.tag.grid(row=2, column=1)
        self.tag["command"] =  self.tagMethod

        self.save = Button(self)
        self.save["text"] = "Save"
        self.save.grid(row=2, column=2)
        self.save["command"] =  self.saveMethod
        # self.encode = Button(self)
        # self.encode["text"] = "Encode"
        # self.encode.grid(row=2, column=3)
        # self.encode["command"] =  self.encodeMethod
        # self.decode = Button(self)
        # self.decode["text"] = "Decode"
        # self.decode.grid(row=2, column=4)
        # self.decode["command"] =  self.decodeMethod
        self.clear = Button(self)
        self.clear["text"] = "Clear"
        self.clear.grid(row=3, column=1)
        self.clear["command"] =  self.clearMethod
        self.delete = Button(self)
        self.delete["text"] = "Delete"
        self.delete.grid(row=3, column=2)
        self.delete["command"] =  self.deleteMethod
        # self.copy = Button(self)
        # self.copy["text"] = "Copy"
        # self.copy.grid(row=2, column=6)
        # self.copy["command"] =  self.copyMethod
 
        self.displayText = Label(self)
        self.displayText["text"] = "something happened"
        self.displayText.grid(row=5, column=1, columnspan=8)

        # camera
        self.camera = Button(self)
        self.camera["text"] = "Camera"
        self.camera.grid(row=4, column=1)
        self.camera["command"] =  self.cameraMethod

        self.dump = Button(self)
        self.dump["text"] = "Dump"
        self.dump.grid(row=4, column=2)
        self.dump["command"] =  self.dumpMethod

        # try image
        path = "images/img7.jpg"
        p = cv2.imread(path)
        # notice!! cv2.imread = BGR, not RGB
        p = cv2.cvtColor(p, cv2.COLOR_BGR2RGB)
        #img = ImageTk.PhotoImage(Image.open(path))
        img = ImageTk.PhotoImage(Image.fromarray(p, 'RGB'))
        self.picture = Label(self, image=img)
        self.picture.image = img
        #self.image = Canvas(self)
        # panel.grid(row=3, column=0, columnspan=2, rowspan=2,
        #         sticky=W+E+N+S, padx=5, pady=5)
        self.picture.grid(row=0, column=0, rowspan=6, sticky=NW)
        #self.image.create_image(0,0, image=img)
        #panel.pack(side="bottom", fill="both", expand="yes")

     
    def tagMethod(self):
        self.displayText["text"] = "This is Tag button."
        no = int(self.numberField.get())
        name = self.nameField.get()
        if no in self.faces:
            index = self.df.loc[self.df.face_ID == no].index
            self.df.set_value(index, "name", name)
            self.displayText["text"] = "Tag "+str(no)+": "+name
            self.redraw(self.images)
        else:
            self.displayText["text"] = "Number not found in this image."

    def saveMethod(self):

        animage = self.images.copy()
        for (i, face_id) in enumerate(self.faces):
            print face_id, len(self.df)
            (img_id, face_id, x, y, w, h, tag, name) = self.df.loc[face_id]
            print x,y
            info = str(int(face_id)) +": "+ name if name != None else str(int(face_id))
            cv2.putText(animage, info, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,255), thickness=3)
        path = images_folder+"img"+str(self.num_images-1)+".jpg"
        cv2.imwrite(path, animage)
        self.displayText["text"] = "Save image to: " + path

    def clearMethod(self):
        self.displayText["text"] = "This is Clear button."
        self.numberField.delete(0, 'end')
        self.nameField.delete(0, 'end')
 
    def deleteMethod(self):
        self.displayText["text"] = "This is Delete button."
        no = int(self.numberField.get())
        if no in self.faces:
            index = self.df.loc[self.df.face_ID == no].index
            self.df.set_value(index, "name", None)
            self.displayText["text"] = "Delete Name: "+str(no)
            self.redraw(self.images)
        else:
            self.displayText["text"] = "Number not found in this image."

    def cameraMethod(self):
        self.displayText["text"] = "This is Camera button."
        Cam.start()
        self.images = Cam.images
        print len(Cam.faces)
        print self.df.columns
        self.faces = []
        for (x, y, w, h, t, n) in Cam.faces:
            self.faces += [len(self.df)]
            self.df.loc[len(self.df)] =  ("img"+str(self.num_images), len(self.df), x, y, w, h, t, n)
        print len(self.df)
        self.num_images += 1

    def dumpMethod(self):
        self.displayText["text"] = "Dump faces to "+dump_csv+"."
        self.df.to_csv(dump_csv, index=False)
        


    def redraw(self, newimage):
        animage = newimage.copy()
        for (i, face_id) in enumerate(self.faces):
            print face_id, len(self.df)
            (img_id, face_id, x, y, w, h, tag, name) = self.df.loc[face_id]
            print x,y
            info = str(int(face_id)) +": "+ name if name != None else str(int(face_id))
            cv2.putText(animage, info, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,255), thickness=3)


        #cv2.putText(image, "N", (x, y), cv2.FONT_HERSHEY_SIMPLEX,2, 255, thickness = 3)
        try:
            p = cv2.cvtColor(animage, cv2.COLOR_BGR2RGB)
        except:
            p = animage
        img = ImageTk.PhotoImage(Image.fromarray(p, 'RGB'))
        self.picture = Label(self, image=img)
        self.picture.image = img
        self.picture.grid(row=0, column=0, rowspan=6, sticky=NW)
        


class Application(Frame):
    def say_hi(self):
        print "hi there, everyone!"

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "top"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


if __name__ == "__main__":


    count = 0
    
    root = Tk()
    app = GUIDemo(master=root)
    root.update_idletasks()
    root.update()

    # app.mainloop()

    while True:
        if app.images != None:

            app.redraw(app.images)
            root.update_idletasks()
            root.update() 
            
        root.update_idletasks()
        root.update()


    # import Tkinter

    # root = Tkinter.Tk()
    # canvas = Tkinter.Canvas(root)
    # canvas.grid(row = 0, column = 0)
    # photo = Tkinter.PhotoImage(master=root, file = 'Aaron.gif')
    # image1 = canvas.create_image(0,0, image=photo)
    # root.mainloop()




