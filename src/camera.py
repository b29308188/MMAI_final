import cv2
import datetime
import time
import sys
import cPickle
sys.path.append(".")
import glob
from utils import detect_faces
from datasets import Photo, inv_label_maps
import numpy as np
import pandas as pd

class Camera():
	def __init__(self, model_path=None):
		print "USAGE : python camera.py model_path"
		self.model_path = model_path
		with open(model_path, "rb") as f:
			self.model = cPickle.load(f)
			self.detector = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

		self.images = None

	def start(self):
		cv2.namedWindow("opening...")
		vc = cv2.VideoCapture(0)

		detect_flag = False

		videoflag = 0
		rval, frame = vc.read()
		s = time.time()
		a = time.time()
		tuples = [] # list of (image_ID, face, tag)
		self.faces = []
		while True:
			if frame is not None:
				pframe = cv2.flip(cv2.resize(frame, (960, 720)), 1)
				dframe = cv2.resize(pframe, (480, 360)) # size ratio = 4
				ratio = 2

			
				p = Photo()
				faces = detect_faces(self.detector, dframe)
				faces = sorted(faces, key=lambda tup: tup[0])
				for (r_x, r_y, r_w, r_h) in faces:
					x, y, w, h = ratio*r_x, ratio*r_y, ratio*r_w, ratio*r_h
					p.add_face(x, y, w, h)
					# Draw a rectangle around the faces
					cv2.rectangle(pframe, (x, y), (x+w, y+h), (255, 0, 0), 2)
				p.image = pframe
				p.extract_features()
				self.faces = []
				if len(p.faces) != 0:
					X = np.array([f.feature for f in p.faces])
					predY = self.model.predict(X)

					for (i, f) in enumerate(p.faces):
						if inv_label_maps[predY[i]] == 'T':
							cv2.rectangle(pframe, (f.x, f.y), (f.x+f.w, f.y+f.h), (0, 255, 0), 2)
						self.faces += [(f.x, f.y, f.w, f.h, inv_label_maps[predY[i]], None)]


				cv2.imshow("camera", pframe)

			
			rval, frame = vc.read()

			oper = cv2.waitKey(1) & 0xFF
			if oper == ord('p'):
				t = time.time()
				iname = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H.%M.%S')
				print iname
				#iname = "/Users/GDog/Desktop/" + iname + ".png"
				self.images = pframe
				vc.release()
				cv2.destroyAllWindows()
				break



if __name__ == "__main__":

	

	cv2.namedWindow("preview")
	vc = cv2.VideoCapture(0)

	videoflag = 0
	rval, frame = vc.read()
	s = time.time()
	a = time.time()

	while True:

		if frame is not None:
			#print frame.shape
			print "image extract:", time.time()-a
			a = time.time()
			pframe = cv2.flip(cv2.resize(frame, (960, 720)), 1)
			print "flip+resize: ", time.time()-a
			a = time.time()
			#detector part
			p = Photo()
			faces = detect_faces(detector, pframe)
			faces = sorted(faces, key=lambda tup: tup[0])
			for (x, y, w, h) in faces:
				p.add_face(x, y, w, h)
				# Draw a rectangle around the faces
				cv2.rectangle(pframe, (x, y), (x+w, y+h), (255, 0, 0), 2)
			print "detect: ", time.time()-a
			a = time.time()
			#filter part
			p.image = pframe
			p.extract_features()
			if len(p.faces) != 0:
				X = np.array([f.feature for f in p.faces])
				predY = model.predict(X)

				for (i, f) in enumerate(p.faces):
					if inv_label_maps[predY[i]] == 'T':
						cv2.rectangle(pframe, (f.x, f.y), (f.x+f.w, f.y+f.h), (0, 255, 0), 2)

			print "predict: ", time.time()-a
			a = time.time()
			cv2.imshow("camera", pframe)
			#cv2.imshow("preview", pframe)

		rval, frame = vc.read()
		ss = s
		s = time.time()

		if videoflag == 1:
			V.append(frame)
			# videoC.write(frame)

		oper = cv2.waitKey(1) & 0xFF
		if oper == ord('p'):
			t = time.time()
			iname = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H.%M.%S')
			print iname
			cv2.imwrite(iname, cv2.flip(frame, 1))
			vc.release()
			break



