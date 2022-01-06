import tkinter.filedialog
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
import PIL.Image, PIL.ImageTk
import time
import cv2

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

from training_classifier import TrainingClassifier
from evaluator_classifier import EvaluatorClassifier

class TrainingModelGUI(tk.Frame):
    def __init__(self, tabcontrol):
        tk.Frame.__init__(self, tabcontrol)
        self.pack(fill=tk.BOTH, expand=1)

        self.frame_buttons = tk.Frame(self)
        self.frame_buttons.pack(side = tk.TOP)
        
        #FONT
        font = tk.font.Font(family='helvetica', size=16)
        
        self.select_model_button=tk.Button(self.frame_buttons, text='Seleccionar modelo', command=self.select_model, font= font)
        self.select_model_button.grid(row = 0)
        
        self.label_model_selected = tk.Label(self.frame_buttons, text='', font = font)
        self.label_model_selected.grid(row = 0, column = 1)

        self.label_epochs = tk.Label(self.frame_buttons, text='Cantidad de épocas', font = font)
        self.label_epochs.grid(row = 1)

        self.input_epochs = tk.Entry(self.frame_buttons, font = font)
        self.input_epochs.grid(row = 1, column = 1)

        self.train_button=tk.Button(self.frame_buttons, text='     Entrenar     ', font = font, command=self.train_model)
        self.train_button.grid(row = 2, column = 0)

        self.evaluation_button=tk.Button(self.frame_buttons, text='     Evaluar      ', font = font, command=self.evaluate_model)
        self.evaluation_button.grid(row = 2, column = 1)

        #PROGRESS BAR
        self.frame_progress_bar = tk.Frame(self)
        self.frame_progress_bar.pack(side = tk.TOP)

        self.label_epochs_training = tk.Label(self.frame_progress_bar, text='', font = font)
        self.label_epochs_training.pack()

        self.progress_training = ttk.Progressbar(self.frame_progress_bar, orient = tk.HORIZONTAL, length = 500, mode = 'determinate')
        self.progress_training.pack()

        self.progress_training.pack_forget()

        #GRAPHICS
        self.frame_graphics = tk.Frame(self)
        self.frame_graphics.pack(side = tk.LEFT, padx = (100, 100))        
        self.history = []
        self.generate_graphics(None)


        #TEXT DETAILS TRAINING/TEST
        self.frame_text_details = tk.Frame(self)
        self.frame_text_details.pack(side = tk.LEFT, padx = (100, 100))
        self.text_details = tk.Text(self.frame_text_details, height = 42, width = 60, font = font)
        self.text_details.pack()
        
        #model classifier
        self.model_path = None

    def generate_graphics(self, accuracy_epoch):
        plt.figure(1).clear()
        fig = plt.figure(1)
        self.canvas = FigureCanvasTkAgg(fig, master=self.frame_graphics)
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.grid(row=0, column=0)
        if accuracy_epoch != None:
            self.history.append(accuracy_epoch)
        
        y = np.array(self.history)
        plt.plot(y)
        plt.yticks(np.arange(0, 1.1, 0.1))

        plt.title('Exactitud del modelo')
        plt.ylabel('Exactitud')
        plt.xlabel('Época')
    
    def select_model(self):
        path = tk.filedialog.askopenfilename(initialdir = '', title = 'Seleccionar modelo', filetypes = (("h5 files","*.h5"), ("all files","*.*")))
        sub_path = path.split('/')
        file_name = sub_path[len(sub_path)-1]
        file_name_subcads = file_name.split('.')
        ext_file_name = file_name_subcads[len(file_name_subcads) - 1]
        if isinstance(path, str) and path != '' and ext_file_name == 'h5' :
            self.label_model_selected.configure(text = file_name)
            self.model_path = path

    def train_model(self):
        epochs = self.input_epochs.get()
        if not self.model_path or self.model_path == '':
            messagebox.showwarning("Precaución",  "Seleccione el modelo para realizar el entrenamiento")    
        elif not epochs.isdigit():
            messagebox.showwarning("Precaución",  "Ingrese la cantidad de épocas, valor numérico")    
        else:
            self.history = []
            self.generate_graphics(None)
            epochs = int(epochs)
            self.text_details.delete('1.0', tk.END)
            training_classifier = TrainingClassifier(self.model_path, epochs, self)
            training_classifier.start()
    
    def evaluate_model(self):
        self.text_details.delete('1.0', tk.END)
        evaluator_classifier = EvaluatorClassifier(self, self.model_path)
        evaluator_classifier.start()
    
    def activate_progress_bar(self):
        self.progress_training.pack()
    
    def hide_progress_bar(self):
        self.update_progress_bar(0)
        self.progress_training.pack_forget()
    
    def update_progress_bar(self, total):
        self.progress_training['value'] = total
    
    def update_label_epochs_training(self, text):
        self.label_epochs_training.configure(text = text)

    def add_text_details(self, text):
        self.text_details.insert(tk.END, text)
    
    def evaluation_training_process(self, start, text):
        self.update_label_epochs_training(text)
        if start:
            self.activate_progress_bar()
        else:
            self.hide_progress_bar()

