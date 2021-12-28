import numpy as np
from tensorflow.keras.utils import Sequence, to_categorical

class DataGenerator(Sequence):
    def __init__(self, ids, labels, batch_size = 32, dim = (15, 224, 224),
                n_channels = 3, n_classes = 16, shuffle = True, path_data = 'DATASET/data2_112/'):
        
        self.dim = dim
        self.batch_size = batch_size
        self.labels = labels
        self.ids = ids
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.path_data = path_data
        self.on_epoch_end()
        self.y_real = []

    def __len__(self):
        return int(np.floor(len(self.ids) / self.batch_size))
    
    def __getitem__(self, index):
        w = self.indexes[index * self.batch_size: (index + 1) * self.batch_size]

        ids_temp = [self.ids[i] for i in w]

        X, Y = self.__data_generation(ids_temp)

        X = X.astype('float32')
        X /= 255.0
        
        return X, Y
    
    def __data_generation(self, ids_temp):
        X = np.empty((self.batch_size, *self.dim, self.n_channels))
        y = np.empty((self.batch_size), dtype = int)

        for i, id in enumerate(ids_temp):
            X[i, ] = np.load(self.path_data + id + '.npy')
            y[i] = self.labels[id]
            self.y_real.append(y[i])
        
        Y = to_categorical(y, num_classes = self.n_classes)
        
        return X, Y

    
    def on_epoch_end(self):
        self.indexes = np.arange(len(self.ids))

        if self.shuffle == True:
            np.random.shuffle(self.indexes)