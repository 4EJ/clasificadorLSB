import tkinter.filedialog
import tkinter as tk
from tkinter import ttk
import PIL.Image, PIL.ImageTk
import time
import cv2
from matplotlib import cm
import numpy as np


class PredictionDetailsGUI(tk.Frame):
    def __init__(self, tabcontrol):
        tk.Frame.__init__(self, tabcontrol)
        self.pack(fill=tk.BOTH, expand=1)

        self.frame_selected_frames = tk.Frame(self)
        self.frame_selected_frames.pack(side = tk.TOP)

        self.frames_features_map = []
        for i in range(0, 6):
            frame_features_map = tk.Frame(self)
            frame_features_map.pack(side = tk.TOP)
            self.frames_features_map.append(frame_features_map)
            if i == 0:
                label_main_title = tk.Label(frame_features_map, text='Mapa de características (Re-dimensionado A 112 x 112 píxeles)', font=('times', 16, 'bold'), bg='#f7f7f7')
                label_main_title.pack(side = tk.TOP, fill = tk.X)        

        #FRAME SELECTED FRAMES
        self.label_frames = tk.Label(self.frame_selected_frames, text='Frames seleccionados', font=('times', 16, 'bold'), bg='#f7f7f7')
        self.label_frames.pack(side = tk.TOP, fill = tk.X)

        self.labels_frames_selected = []
        for i in range(0, 15):
            label_frame_selected = tk.Label(self.frame_selected_frames, text = '')
            label_frame_selected.pack(side = tk.LEFT, expand = 0)
            self.labels_frames_selected.append(label_frame_selected)
        
        #FRAME FEATURES MAP
        self.labels_features_map = []
        self.labels_titles_features_map = []
        for frame_features_map in self.frames_features_map:
            label_title_conv = tk.Label(frame_features_map, text = '', font=('times', 16, 'bold'))
            label_title_conv.pack(side = tk.LEFT, expand = 0)
            self.labels_titles_features_map.append(label_title_conv)
            for i in range(0, 10):
                label_feature_map_temp = tk.Label(frame_features_map, text = '')
                label_feature_map_temp.pack(side = tk.LEFT, expand = 0)
                self.labels_features_map.append(label_feature_map_temp)
        
        #FRAME SOFTMAX DISTRIBUTION
        self.frame_top3_signs = tk.Frame(self)
        self.frame_top3_signs.pack(side = tk.TOP)

        self.label_top3_signs_title = tk.Label(self.frame_top3_signs, text='Top 3 señas más probables', font=('times', 16, 'bold'), bg='#f7f7f7')
        self.label_top3_signs_title.pack(side = tk.TOP, fill = tk.X)

        self.label_top3_signs_details = tk.Label(self.frame_top3_signs, text='', font=('times', 16, 'bold'), bg='#f7f7f7')
        self.label_top3_signs_details.pack(side = tk.TOP)


    
    def set_selected_frames(self, frames):
        i = 0
        for frame in frames:
            photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            label_frame_selected = self.labels_frames_selected[i]
            label_frame_selected.configure(image = photo)
            label_frame_selected.image = photo
            i = i + 1
    
    def set_features_map(self, frames):
        for i in range(0, len(self.labels_titles_features_map)):
            number_layer = str(i+1)
            frame_layer = frames[i*10]
            size_frame_layer = frame_layer.shape
            title = number_layer + '° capa de convolución\n Dimension-original ' + str(size_frame_layer[0]) + ' x ' + str(size_frame_layer[1]) + ' píxeles'
            label_title = self.labels_titles_features_map[i]
            label_title.configure(text = title)
        
        i = 0
        for frame in frames:
            image = PIL.Image.fromarray(np.uint8(cm.gist_earth(frame)*255))
            image = image.resize((112, 112), PIL.Image.ANTIALIAS)
            photo = PIL.ImageTk.PhotoImage(image = image)
            label_features_map = self.labels_features_map[i]
            label_features_map.configure(image = photo)
            label_features_map.image = photo
            i = i + 1
    
    def set_top_3_signs_predicted(self, report_top3):
        self.label_top3_signs_details.configure(text = report_top3)