import tkinter as tk
from tkinter import ttk
import PIL.Image, PIL.ImageTk
import time
import cv2


class App:
    def __init__(self, window, window_title, video_capture, video_classifier_lsb):
        self.window = window #root
        self.window.title(window_title)
        
        self.label_word = tk.Label(window, text='', font=('times', 30, 'bold'), bg='#f7f7f7')
        self.label_word.pack(fill = tk.X)

        #the states 0: nothing, 1: count, 2: init record
        self.counter = 0
        self.start_time = 0

        #create video_classifier_lsb
        self.video_classifier_lsb = video_classifier_lsb
        
        # open video source (by default this will try to open the computer webcam)
        self.video_capture = video_capture

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width = self.video_capture.width, height = self.video_capture.height)
        self.canvas.pack(fill = tk.BOTH, expand = 1)

        #video control buttons
        self.start_button=tk.Button(window, text='GRABAR', command=self.start_recording)
        self.start_button.pack(side=tk.LEFT)

        self.select_file_button = tk.Button(window, text = 'SELECCIONAR VIDEO', command = self.open_file)
        self.select_file_button.pack(side = tk.LEFT)

        self.limit_count = 3
        
        self.frames = []

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 1
        self.update()
        self.window.mainloop()


    def start_recording(self):
        self.counter = 1
        self.frames = []
        self.start_time = time.time()

    def open_file(self):
        self.label_word.config(text = '')
        path = tk.filedialog.askopenfilename(initialdir = '/home/heredia/Desktop/Python/GUI/Video capture/', title = 'Seleccionar video', filetypes = (("jpeg files","*.avi"), ("jpeg files","*.mp4"), ("all files","*.*")))
        self.video_capture.read_file(path)
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
        elif self.counter == 2:
            if time_elapsed >= 3:
                self.counter = 0
                sign = self.video_classifier_lsb.predict(self.frames)
                self.label_word.config(text = 'Palabra: ' + sign)
            else:
                self.frames.append(frame)
                #self.label_word.config(text= "0" + str(time_elapsed))
        elif self.counter == 3:
            if ret:
                self.frames.append(frame)
            else:
                self.counter = 0
                sign = self.video_classifier_lsb.predict(self.frames)
                self.label_word.config(text = 'Palabra: ' + sign)

        if ret:
            self.__update_canvas(frame)

        self.window.after(self.delay, self.update)
    
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