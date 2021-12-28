import cv2
import time
import os

class VideoCapture:

    def __init__(self, video_source = 0):
        self.__detect_connected_webcams()
        self.video_source = self.video_sources[0]
        self.set_video_source(self.video_source)
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

        
    def set_video_source(self, video_source):
        self.video_source = video_source
        self.capturer = cv2.VideoCapture(self.video_source)
        

    def get_video_sources(self):
        return self.video_sources

    def __detect_connected_webcams(self):
        self.video_sources = []
        for i in range(8):
            cap = cv2.VideoCapture(i)
            if not (cap is None or not cap.isOpened()):
                self.video_sources.append(i)

    def get_frame(self):
        if self.recording:
            if self.capturer.isOpened():
                ret, frame = self.capturer.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    return (ret, frame)
                else:
                    return (ret, None)
            else:
                return (None, None)
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
    
    def save_video(self, path_root, frames, sign):
        if not os.path.isdir(path_root):
            os.mkdir(path_root)
        full_path = path_root + '/' + sign
        
        if not os.path.isdir(full_path):
            os.mkdir(full_path)
        list_videos = os.listdir(full_path)
        index = 1 + self.__count_files(list_videos)

        path_video = full_path + '/' + sign + '_' + str(index) + '.avi'
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        
        out = cv2.VideoWriter(path_video, fourcc, 15, (640, 480))

        for frame in frames:
            out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))


    def __count_files(self, folder):
        ext = '.avi'
        cnt = 0
        for x in folder:
            if ext in x:
                cnt = cnt + 1
        return cnt