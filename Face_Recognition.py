import json
import time
import numpy as np
import cv2
# import pafy
import pandas
from time import time
import pandas as pd
from imutils import paths
import face_recognition
import pickle
import os
from datetime  import datetime
import pickle
from face_enc import Face_Encodings
from connet_sql_ssh import Connect

class Face_Recognition:
    #get the video and return it
    def get_video(self):
        #return cv2.VideoCapture('rtsp://10.10.5.200:554/user=admin&password=&channel=1&stream=0.sdp?')
        return cv2.VideoCapture(0)

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
            face_locations = face_recognition.face_locations(rgb_small_frame,model='hog',number_of_times_to_upsample=2)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
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
        if os.path.exists('encodings.txt')==True and os.path.exists('names.txt')==True:
            with open("encodings.txt", "rb") as f1:
                known_face_encodings= pickle.load(f1)
            with open("names.txt", "rb") as f2:
                known_face_names = pickle.load(f2)
        else:
            Face_Encodings.face_encodings(self)
        while True:
            ret, frame = video_source.read()
            #frame2=cv2.resize(frame,(680,480),fx=0,fy=0,interpolation=cv2.INTER_CUBIC)
            assert ret
            faces=self.face_recognition(frame,known_face_encodings,known_face_names)
            for name in set(faces):
                s1 = slice(9, -4)
                self.Attendance(name)
            print(faces)

a = Face_Recognition()
a()

