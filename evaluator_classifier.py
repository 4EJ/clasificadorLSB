import threading
from tensorflow.keras.models import load_model
from tensorflow.keras import Model
from data_generator import DataGenerator
from sklearn.metrics import classification_report, confusion_matrix
import csv
import numpy as np
from callback_evaluator import CallbackEvaluator

class EvaluatorClassifier(threading.Thread):
    def __init__(self, training_model_gui, path_model):
        threading.Thread.__init__(self)
        self.training_model_gui = training_model_gui
        self.path_model = path_model
        self.model = load_model(self.path_model)

        self.img_cols = 112
        self.img_rows = 112
        self.img_depth = 15
    
        self.root_path = 'data_test/'
        self.path_partition = self.root_path + 'partition_test.csv'
        self.path_labels = self.root_path + 'labels_test.csv'
        self.path_dataset = self.root_path + 'data/'

        self.params = {'dim': (self.img_depth, self.img_rows, self.img_cols),
          'batch_size': 1,
          'n_classes': 16,
          'n_channels': 1,
          'shuffle': False,
          'path_data': self.path_dataset
        }

        self.signs = [
            "agua", "aprender", "calle", "comer",
            "derecha", "dinero", "futbol", "gracias",
            "hospital", "jugar", "mama", "mañana",
            "no querer", "pedir", "presidente", "que"
        ]

        self.read_dataset_references()
    
    def read_dataset_references(self):
        self.partition = []
        self.labels = {}

        with open(self.path_partition) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.partition.append(row[0])
        
        with open(self.path_labels) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.labels[row[0]] = int(row[1])
    
    def get_labels(self):
        labels_ans = []
        for id in self.partition:
            labels_ans.append(self.labels[id])
        return labels_ans

    def run(self):
        self.training_model_gui.evaluation_training_process(True, 'Evaluando el modelo')
        test_gen = DataGenerator(self.partition, self.labels, **self.params)
        callback = CallbackEvaluator(test_gen.__len__(), self.training_model_gui)
        Y_pred = self.model.predict_generator(test_gen, callbacks = [callback])
        Y_pred = np.argmax(Y_pred, axis = 1)
        Y = self.get_labels()
        Y = np.array(Y)
        #confusion_matrixx = confusion_matrix(Y, Y_pred)
        classification_reportt = classification_report(Y, Y_pred, target_names = self.signs)
        classification_reportt = classification_reportt.replace('support', 'videos')
        index = classification_reportt.find('macro')
        classification_reportt = classification_reportt[:index]
        classification_reportt = classification_reportt.replace('accuracy', 'exactitud')
        classification_reportt = classification_reportt.replace('recall', 'sensibilidad')
        classification_reportt = classification_reportt.replace('f1-score', 'puntaje-f1')
        self.training_model_gui.evaluation_training_process(False, 'EVALUACION FINALIZADA') 
        
        #report = 'MATRIZ DE CONFUSION\n' + str(confusion_matrixx) + '\n\n'
        report = 'Resultados\n' + classification_reportt

        self.training_model_gui.add_text_details(report)

