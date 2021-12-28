from tensorflow.keras.models import load_model
from tensorflow.keras import Model
import numpy as np
import cv2
import random

class VideoClassifierLSB:
    def __init__(self):
        self.model = None
        self.signs = ['agua', 'aprender', 'calle', 'comer', 'derecha', 'dinero',
                    'futbol', 'gracias', 'hospital', 'jugar', 'mama', 'mañana',
                    'no querer', 'pedir', 'presidente', 'que']

    def set_model(self, path_model):
        self.model = load_model(path_model)
        input_shape = self.model.layers[0].input_shape[0]
        _, depth, rows, cols, channels = input_shape

        self.img_depth = depth
        self.img_width = rows
        self.img_height = cols
    
    def there_is_model(self):
        exist = False
        if self.model != None:
            exist = True
        return exist

    def init_conv_layers(self):
        self.models_conv_layers = []
        for i in range(len(self.model.layers)):
            layer = self.model.layers[i]
            if 'conv' not in layer.name:
                continue
            model_conv_layer = Model(inputs = self.model.inputs, outputs = self.model.layers[i].output)
            self.models_conv_layers.append(model_conv_layer)

    def predict(self, frames):
        if self.model == None:
            return None
        
        frames = self.__selection_of_frames(frames)
        
        X = []
        X.append(frames)
        X = np.array(X)

        X = X.astype('float32')
        X /= 255.0

        Y = self.model.predict(X)

        pos = np.argmax(Y)
        sign = self.signs[pos]

        self.__notify_features_map(X)
        self.prediction_details_gui.set_top_3_signs_predicted(self.generate_top_3_signs_predicted(Y))
        return sign
    
    def generate_top_3_signs_predicted(self, Y):
        probabilities = []
        i = 0
        for y1 in Y[0]:
            probabilities.append((y1, i))
            i = i + 1
        
        probabilities_sorted = sorted(probabilities, key = lambda x: x[0], reverse = True)
        
        report_top3 = ''
        for top_i in range(0, 3):
            probability = probabilities_sorted[top_i]
            value = probability[0]
            id_sign = probability[1]
            sign = self.signs[id_sign]
            report_top3 = report_top3 + sign + ': ' + str(value) + '\n'
        return report_top3 


    def __notify_features_map(self, X):
        self.init_conv_layers()
        features = []
        for model_conv_layer in self.models_conv_layers:
            features_map = model_conv_layer.predict(X)
            n = features_map.shape[1]
            m = features_map.shape[4]
            for k in range(0, 10):
                i = random.randint(0, n-1)
                j = random.randint(0, m-1)
                feature = features_map[0, i, :, :, j]
                features.append(feature)
                
        self.prediction_details_gui.set_features_map(features)


    def __selection_of_frames(self, video):
        frames = []
        frames_rgb = []
        tot_frames = len(video)
        step = (tot_frames * 1.0) / (self.img_depth * 1.0)
        
        cnt = step
        searched = int(cnt) - 1
        
        while len(frames) < 15 and searched < tot_frames:
            frame = video[searched]
            frame = cv2.resize(frame,(self.img_width, self.img_height),interpolation=cv2.INTER_AREA)
            
            frames_rgb.append(frame)

            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            frame = self.to_one_channel(frame)
                    
            frames.append(frame)

            cnt = cnt + step
            searched = int(cnt) - 1
            
        frames = np.array(frames)
        
        if frames.shape[0] != 15 :
            print(frames.shape[0])
        
        self.prediction_details_gui.set_selected_frames(frames_rgb)
        
        return frames
    
    def to_one_channel(self, frame):
        res = np.zeros((self.img_width, self.img_height, 1))
        res[:, :, 0] = frame[:, :]
        return res
    
    def set_prediction_details_gui(self, prediction_details_gui):
        self.prediction_details_gui = prediction_details_gui