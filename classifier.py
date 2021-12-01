from tensorflow.keras.models import load_model
import numpy as np
import cv2

class VideoClassifierLSB:
    def __init__(self, path_model):
        self.model = load_model(path_model)
        self.signs = ['agua', 'aprender', 'calle', 'comer', 'derecha', 'dinero',
                    'futbol', 'gracias', 'hospital', 'jugar', 'mama', 'mañana',
                    'no querer', 'pedir', 'presidente', 'que']

        input_shape = self.model.layers[0].input_shape[0]
        _, depth, rows, cols, channels = input_shape

        self.img_depth = depth
        self.img_width = rows
        self.img_height = cols

    def predict(self, frames):
        frames = self.__selection_of_frames(frames)
        
        X = []
        X.append(frames)
        X = np.array(X)

        X = X.astype('float32')
        X /= 255.0

        Y = self.model.predict(X)

        pos = np.argmax(Y)
        sign = self.signs[pos]
        #print(Y)
        #print(str(pos) + ': ' + sign)

        return sign

    def __selection_of_frames(self, video):
        frames = []
        tot_frames = len(video)
        step = (tot_frames * 1.0) / (self.img_depth * 1.0)
        
        i = 0
        cnt = step
        searched = int(cnt) - 1
        
        while len(frames) < 15 and searched < tot_frames:
            frame = video[searched]
            frame = cv2.resize(frame,(self.img_width, self.img_height),interpolation=cv2.INTER_AREA)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            frame = self.to_one_channel(frame)
                    
            frames.append(frame)

            cnt = cnt + step
            searched = int(cnt) - 1
            
        frames = np.array(frames)
        
        if frames.shape[0] != 15 :
            print(frames.shape[0])
        
        return frames
    
    def to_one_channel(self, frame):
        res = np.zeros((self.img_width, self.img_height, 1))
        res[:, :, 0] = frame[:, :]
        return res