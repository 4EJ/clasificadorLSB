import tkinter as tk
from tkinter import ttk
from tkinter import font
#import PIL.Image, PIL.ImageTk
import time
#import cv2

from sign_recognition_gui import SignRecognitionGUI
from prediction_details_gui import PredictionDetailsGUI
from training_model_gui import TrainingModelGUI

class App:
    def __init__(self, window, window_title, video_capture, video_classifier_lsb):
        self.window = window #root
        self.window.title(window_title)
        
        font = tk.font.Font(family='helvetica', size=16)
        s = ttk.Style()
        s.theme_use('default')
        s.configure('TNotebook.Tab', font = font)
        s.map("TNotebook", background= [("selected", "green3")])
        
        
        tabControl = ttk.Notebook(window)
  
        self.sign_recognition_gui = SignRecognitionGUI(tabControl, video_capture, video_classifier_lsb)
        self.prediction_details_gui = PredictionDetailsGUI(tabControl)
        self.training_model_gui = TrainingModelGUI(tabControl)
        video_classifier_lsb.set_prediction_details_gui(self.prediction_details_gui)


        tabControl.add(self.sign_recognition_gui, text ='Reconocimiento y recolección de videos')
        tabControl.add(self.prediction_details_gui, text ='Detalles del reconocimiento')
        tabControl.add(self.training_model_gui, text ='Entrenamiento')
        tabControl.pack(expand = 1, fill ="both")
        self.window.mainloop()
    
