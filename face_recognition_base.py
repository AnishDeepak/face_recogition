import json
import numpy as np
import cv2
# import pafy
from time import time
from imutils import paths
import face_recognition
import pickle
import os
from datetime  import datetime

class Face_Recognition:
    #get the video and return it
    def get_video(self):
        #return cv2.VideoCapture('rtsp://10.10.5.200:554/user=admin&password=&channel=1&stream=0.sdp?')
        return cv2.VideoCapture(0)
    #count the existing employee image folders
    def emp_count(self):
        imagePaths = list(paths.list_images('new_emp_images'))
        return len(imagePaths)
    #encode the existing employee face images and return the encodings and names
    def face_encodings(self):
        known_face_encodings=[]
        known_face_names=[]
        imagePaths = list(paths.list_images('old_emp_images'))
        for (i, imagePath) in enumerate(imagePaths):
            name = imagePath.split(os.path.sep)[-2]
            image = face_recognition.load_image_file(imagePath)
            face_encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(face_encoding)
            known_face_names.append(name)
        return known_face_encodings,known_face_names
    #create new amployee face encodngs
    def new_face_encodings(self,names):
        new_encoding=[]
        new_names=[]
        imagePaths = list(paths.list_images('new_emp_images'))
        for (i, imagePath) in enumerate(imagePaths):
            name = imagePath.split(os.path.sep)[-2]
            if name not in names:
                image = face_recognition.load_image_file(imagePath)
                face_encoding = face_recognition.face_encodings(image)[0]
                new_encoding.append(face_encoding)
                new_names.append(name)
        return new_encoding, new_names
    #store the results in json file
    def Attendance(self,name):
        with open('attendance.json', 'r+') as f:
            DataList = f.readlines()
            name_list = []
            for data in DataList:
                ent = data.split(',')
                name_list.append(ent[0])
            if name not in name_list:
                curr = datetime.now()
                dt = curr.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dt}')
    #compare the faces from video feed and existing employees
    def face_recognition(self,frame,known_face_encodings,known_face_names):
        small_frame = cv2.resize(frame, (0, 0), fx=0.45, fy=0.45)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        while True:
            #if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame,model='hog')
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding,tolerance=.5)
                name = "Unknown"
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                face_names.append(name)
            return face_names
    def __call__(self):
        video_source = self.get_video()
        assert video_source.isOpened()
        x_shape = int(video_source.get(cv2.CAP_PROP_FRAME_WIDTH))
        y_shape = int(video_source.get(cv2.CAP_PROP_FRAME_HEIGHT))
        known_face_encodings, known_face_names = self.face_encodings()
        new_emp_count = self.emp_count()
        while True:
            ret, frame = video_source.read()
            frame2=cv2.resize(frame,(680,480),fx=0,fy=0,interpolation=cv2.INTER_CUBIC)
            assert ret
            if self.emp_count()>new_emp_count:
                new_emp_count=0
                new_encodings,new_names = self.new_face_encodings(known_face_names)
                #known_face_encodings, known_face_names = self.new_face_encodings(known_face_names)
                known_face_encodings.extend(new_encodings)
                known_face_names.extend(new_names)
            faces=self.face_recognition(frame2,known_face_encodings,known_face_names)
            for name in set(faces):
                s1 = slice(9, -4)
                self.Attendance(name)
            print(faces)
a = Face_Recognition()
a()

