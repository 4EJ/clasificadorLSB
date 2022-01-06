from tensorflow.keras.models import load_model
from tensorflow.keras import Model
import numpy as np
import cv2
import random
import os
from sklearn.model_selection import train_test_split
from data_generator import DataGenerator
import matplotlib.pyplot as plt
import threading

from callback_training import CallbackTraining

class TrainingClassifier(threading.Thread):
    def __init__(self, path_model, epochs, training_model_gui):
        threading.Thread.__init__(self)
        self.path_model = path_model
        self.epochs = epochs
        self.training_model_gui = training_model_gui

        self.model = None
        self.path_videos_lsb = 'videos_lsb'
        self.signs = [
            "agua", "aprender", "calle", "comer",
            "derecha", "dinero", "futbol", "gracias",
            "hospital", "jugar", "mama", "mañana",
            "no querer", "pedir", "presidente", "que"
            ]
        self.labels = None
        self.ids_dataset = None
        self.sink = 'dataset/'
        
        self.img_cols = 112
        self.img_rows = 112
        self.img_depth = 15

        self.X_train = None
        self.X_dev = None
    
    

    def run(self):
        self.training_model_gui.update_label_epochs_training('Generando conjunto de entrenamiento en: ' + self.sink)
        self.generate_dataset()
        self.model = load_model(self.path_model)

        params = {'dim': (self.img_depth, self.img_rows, self.img_cols),
          'batch_size': 16,
          'n_classes': len(self.signs),
          'n_channels': 1,
          'shuffle': True,
          'path_data': self.sink
        }

        
        training_generator = DataGenerator(self.X_train, self.labels, **params)
        dev_generator = DataGenerator(self.X_dev, self.labels, **params)
        
        self.training_model_gui.evaluation_training_process(True, 'Entrenando el modelo')
        
        callback = CallbackTraining(self.epochs, self.training_model_gui)
        hist = self.model.fit_generator(generator = training_generator,
                          validation_data = dev_generator,
                          epochs = self.epochs,
                          callbacks = [callback])
        name_model = self.path_model.split('.')[0]
        path_new_model = name_model + '_retrained.h5' 
        self.model.save(path_new_model)
        self.training_model_gui.evaluation_training_process(False, 'Entrenamiento finalizado, modelo guardado en: '+ path_new_model)
        
    def generate_dataset(self):
        self.ids_dataset = []
        self.labels = {}
        self.__verify_sink_path()
        id_sign = 0
        
        for sign in self.signs:
            path_sign = self.path_videos_lsb + '/' + sign + '/'
            self.__process_videos_of_sign(id_sign, path_sign)
            id_sign = id_sign + 1

        self.__split_dataset()
    
    def __split_dataset(self):
        self.X_train, self.X_dev = train_test_split(self.ids_dataset, train_size = 0.8)

    def __verify_sink_path(self):
        if os.path.isdir(self.sink):
            videos = os.listdir(self.sink)
            for video in videos:
                path_video = self.sink + video
                os.remove(path_video)
        else:
            os.mkdir(self.sink)

    def __process_videos_of_sign(self, id_sign, path):
        if os.path.isdir(path):
            videos = os.listdir(path)

            for video in videos:
                path_video = path + video
                cap = cv2.VideoCapture(path_video)

                id_video = video.split('.')[0]
                self.ids_dataset.append(id_video)
                self.labels[id_video] = id_sign

                frames = self.__selection_of_frames(cap)
                self.__save_frames(self.sink + id_video, frames)
    

    def __save_frames(self, path, frames):
        np.save(path, frames)


    def __selection_of_frames(self, video):
        tot_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        step = (tot_frames * 1.0) / (self.img_depth * 1.0)
        i = 0
        cnt = step
        searched = round(cnt) - 1
        frames = []

        while len(frames) < 15:
            i = i + 1
            video.set(1, searched)
            ret, frame = video.read()
            frame = cv2.resize(frame, (self.img_rows, self.img_cols), interpolation = cv2.INTER_AREA)
                
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = self.to_one_channel(frame)
            
            frames.append(frame)
            cnt = cnt + step
            searched = round(cnt) - 1
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        frames = np.array(frames)

        if frames.shape[0] != self.img_depth:
            print(frames.shape[0])
        
        return frames


    def to_one_channel(self, frame):
        res = np.zeros((self.img_rows, self.img_cols, 1))
        res[:, :, 0] = frame[:, :]
        return res