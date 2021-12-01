from classifier import VideoClassifierLSB
from video_capture import VideoCapture
from app import App
import tkinter as tk

def main():
    video_source = 1
    video = VideoCapture(video_source)
    
    #path_model = '3dcnn_17/model_3dcnn_17_64.h5'
    path_model = 'model_gray_3dcnn_6_96.h5'
    
    classifier = VideoClassifierLSB(path_model)
    
    title = 'CLASIFICADOR DE VIDEOS DE LA LENGUA DE SEÑAS BOLIVIANA'
    
    window = tk.Tk()
    app = App(window, title, video, classifier)


if __name__ == '__main__':
    main()