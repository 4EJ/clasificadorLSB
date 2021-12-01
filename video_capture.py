import cv2
import matplotlib.pyplot as plt
import time

class VideoCapture:

    def __init__(self, video_source = 0):
        self.video_source = video_source
        self.capturer = cv2.VideoCapture(video_source)
        self.recording = True
        self.time_sleep = 0
        if not self.capturer.isOpened():
            raise ValueError("Unable to open video source", video_source)

        STD_DIMENSIONS =  {
            '480p': (640, 480),
            '600p': (800, 600),
            '960p': (960, 720),
            '720p': (1280, 720),
            '1280p': (1280, 960)
        }

        dim = '480p'
        res = STD_DIMENSIONS[dim]
        
        #set video sourec width and height
        self.capturer.set(3,res[0])
        self.capturer.set(4,res[1])

        self.width, self.height = res


    # To get frames
    def get_frame(self):
        if self.recording:
            if self.capturer.isOpened():
                ret, frame = self.capturer.read()
                if ret:
                    # Return a boolean success flag and the current frame converted to BGR
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    return (ret, frame)
                else:
                    return (ret, None)
            else:
                return (ret, None)
        else:
            ret, frame = self.capturer.read()
            time.sleep(self.time_sleep)
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                return (ret, frame)
            else:
                self.recording = True
                self.capturer = cv2.VideoCapture(self.video_source)
                return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.capturer.isOpened():
            self.capturer.release()
            cv2.destroyAllWindows()

    def read_file(self, path):
        self.recording = False
        self.capturer = cv2.VideoCapture(path)
        tot_frames = int(self.capturer.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = tot_frames / 3.0
        self.time_sleep = 1.0 / fps
        print('fps', fps, 'time_sleep', self.time_sleep)
        