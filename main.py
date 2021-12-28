from classifier import VideoClassifierLSB
from video_capture import VideoCapture
from app import App
import tkinter as tk

def main():
    video_source = 0
    video = VideoCapture(video_source)
    classifier = VideoClassifierLSB()
    title = 'CLASIFICADOR DE VIDEOS DE LA LENGUA DE SEÑAS BOLIVIANA'
    window = tk.Tk()
    app = App(window, title, video, classifier)


if __name__ == '__main__':
    main()