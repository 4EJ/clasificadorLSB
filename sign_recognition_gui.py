import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import font
import PIL.Image, PIL.ImageTk
import time
import cv2

class SignRecognitionGUI(tk.Frame):
    def __init__(self, tabcontrol, video_capture, video_classifier_lsb):
        tk.Frame.__init__(self, tabcontrol)
        self.pack(fill=tk.BOTH, expand=1)

        self.label_word = tk.Label(self, text='', font=('times', 30, 'bold'), bg='#f7f7f7')
        self.label_word.pack(fill = tk.X)

        #the states 0: nothing, 1: count, 2: init record
        self.counter = 0
        self.start_time = 0

        #create video_classifier_lsb
        self.video_classifier_lsb = video_classifier_lsb
        
        # open video source (by default this will try to open the computer webcam)
        self.video_capture = video_capture

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(self, width = self.video_capture.width, height = self.video_capture.height)
        self.canvas.pack(fill = tk.BOTH, expand = 1)
        
        # Font
        font = tk.font.Font(family='helvetica', size=16)
        
        #select model
        self.select_model_button = tk.Button(self, text = 'Seleccionar clasificador', command = self.open_model, font = font)
        self.select_model_button.pack(side = tk.LEFT, expand = 0)

        #select camera
        #self.label_camera = tk.Label(self, text='SELECCIONAR CAMARA: ', font=('times', 10, 'bold'), bg='#f7f7f7')
        self.label_camera = tk.Label(self, text = 'Seleccionar cámara: ', font = font)
        self.label_camera.pack(side = tk.LEFT, expand = 0)

        #combo box of availables cameras
        sources = self.video_capture.get_video_sources()
        
        self.combo_cameras = ttk.Combobox(self, values = sources, font = font)
        self.combo_cameras.current(0)
        self.combo_cameras.pack(side = tk.LEFT, expand = 0)
        self.combo_cameras.bind("<<ComboboxSelected>>", self.change_camera)


        #video control buttons
        self.start_button=tk.Button(self, text='Reconocer video vivo', command=self.start_recording, font = font)
        self.start_button.pack(side=tk.LEFT, expand = 0)

        self.select_file_button = tk.Button(self, text = 'Reconocer archivo video', command = self.open_file, font = font)
        self.select_file_button.pack(side = tk.LEFT, expand = 0)
        
        
        #combo box of signs

        self.collect_video_button=tk.Button(self, text='Recolectar video', command=self.collect_video, font = font)
        self.collect_video_button.pack(side=tk.LEFT)

        self.signs = [
            "agua", "aprender", "calle", "comer",
            "derecha", "dinero", "futbol", "gracias",
            "hospital", "jugar", "mama", "mañana",
            "no querer", "pedir", "presidente", "que"
            ]

        self.combo_signs = ttk.Combobox(self, values = self.signs, font = font)
        self.selected_sign = self.signs[0]
        self.combo_signs.current(0)
        self.combo_signs.pack(side = tk.LEFT)
        self.combo_signs.bind("<<ComboboxSelected>>", self.change_sign)

        
        self.limit_count = 3   
        self.frames = []
        self.is_video_collection = False

        self.path_videos_lsb = 'videos_lsb'

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 1
        self.update()
            
    
    def change_sign(self, event):
        self.selected_sign = self.combo_signs.get()
    
    def change_camera(self, event):
        video_source = self.combo_cameras.get()
        self.video_capture.set_video_source(int(video_source))
    
    def collect_video(self):
        self.counter = 1
        self.frames = []
        self.start_time = time.time()
        self.is_video_collection = True

    def start_recording(self):
        if self.video_classifier_lsb.there_is_model():
            self.counter = 1
            self.frames = []
            self.start_time = time.time()
        else:
            messagebox.showwarning("Precaucion",  "Seleccione el modelo para realizar el reconocimiento")


    def open_file(self):
        if self.video_classifier_lsb.there_is_model():
            self.label_word.config(text = '')
            path = tk.filedialog.askopenfilename(initialdir = '', title = 'Seleccionar video', filetypes = (("jpeg files","*.avi"), ("jpeg files","*.mp4"), ("all files","*.*")))
            if isinstance(path, str) and path != '':
                self.video_capture.read_file(path)
                self.counter = 3
                self.frames = []
        else:
            messagebox.showwarning("Precaucion",  "Seleccione el modelo para realizar el reconocimiento")
    
    def open_model(self):
        self.label_word.config(text = '')
        path = tk.filedialog.askopenfilename(initialdir = '', title = 'Seleccionar modelo clasificador', filetypes = (("jpeg files","*.h5"), ("all files","*.*")))
        if isinstance(path, str) and path != '':
            self.video_classifier_lsb.set_model(path)
            self.counter = 3
            self.frames = []

    def __update_canvas(self, frame):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        frame_canvas = cv2.resize(frame,(canvas_width, canvas_height),interpolation=cv2.INTER_AREA)
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame_canvas))
        self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)


    def update(self):
        # Get a frame from the video source
        ret, frame = self.video_capture.get_frame()

        time_elapsed = int(time.time() - self.start_time)

        #INICIAR CONTADOR
        if self.counter == 1:
            self.label_word.config(text = '')
            if time_elapsed < self.limit_count:
                k = self.limit_count - time_elapsed
                frame = self.__update_counter(time_elapsed, frame)
                #self.label_word.config(text= str(k))
            else:
                #self.label_word.config(text="YA")
                frame = self.__update_counter(time_elapsed, frame)
                self.counter = 2
                self.start_time = time.time()
        #RECONOCER VIDEO VIVO
        elif self.counter == 2:
            if time_elapsed >= 3:
                self.counter = 0
                if self.is_video_collection:
                    self.is_video_collection = False
                    self.video_capture.save_video(self.path_videos_lsb, self.frames, self.selected_sign)
                    self.label_word.config(text="Video guardado correctamente")
                else:
                    sign = self.video_classifier_lsb.predict(self.frames)
                    self.label_word.config(text = 'Palabra: ' + sign)
            else:
                self.frames.append(frame)
                #self.label_word.config(text= "0" + str(time_elapsed))
        #RECONOCER ARCHIVO VIDEO
        elif self.counter == 3:
            if ret:
                self.frames.append(frame)
            else:
                self.counter = 0
                sign = self.video_classifier_lsb.predict(self.frames)
                self.label_word.config(text = 'Palabra: ' + sign)

        if ret:
            self.__update_canvas(frame)

        self.after(self.delay, self.update)
    
    def __update_counter(self, time_elapsed, frame):
        font = cv2.FONT_ITALIC 
        pos = (300, 350) 
        font_scale = 3
        color = (255, 255, 255)
        # Line thickness of 2 px 
        thickness = 3
        
        k = self.limit_count - time_elapsed
        if k > 0:
            text = str(k)
        else:
            text = 'YA'
        frame = cv2.putText(frame, text, pos, font,  
                   font_scale, color, thickness, cv2.LINE_AA) 

        return frame