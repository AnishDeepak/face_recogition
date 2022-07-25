import numpy as np
import cv2
# import pafy
import pandas as pd
from imutils import paths
import face_recognition
import pickle
import os
import pickle
from connet_sql_ssh import Connect


class Face_Encodings:

    def check_id_img_dir(self,auto_id):
        if len(list(paths.list_images('inndata_emp_images/emp-'+str(auto_id))))>0:
            return True
    def face_encodings(self):
        known_face_encodings=[]
        known_face_names=[]
        no_img_ids=[]
        if  os.path.exists('inndata_emp_images')==False:
            Connect.down_from_remote(self)
        imagePaths = list(paths.list_images('inndata_emp_images'))
        for (i, imagePath) in enumerate(imagePaths):
            folder_name = imagePath.split(os.path.sep)[-2]
            id=int(folder_name[-1])
            print(folder_name)

            emp_table = Connect.get_auto_id(self)
            for first_name, lst_name, auto_id in emp_table:
                dir_exist=self.check_id_img_dir(auto_id)
                if dir_exist==True:
                    if id == auto_id:
                        print(first_name + ' ' + lst_name)
                        emp_name = first_name + ' ' + lst_name
                        continue
                else:
                    no_img_emp_name=first_name + ' ' + lst_name
                    if no_img_emp_name not in no_img_ids:
                        no_img_ids.append(no_img_emp_name)

            known_face_names.append(emp_name)
            image = face_recognition.load_image_file(imagePath)
            face_encoding = face_recognition.face_encodings(image, num_jitters=2)[0]
            known_face_encodings.append(face_encoding)

            with open('encodings.txt', 'wb') as f1:
                pickle.dump(known_face_encodings, f1)
            with open('names.txt', 'wb') as f2:
                pickle.dump(known_face_names, f2)

        return no_img_ids

    def __call__(self):
        names=[]
        names=self.face_encodings()
        print('No images for these employees:',names)

b = Face_Encodings()
b()