import threading
import time
import time as t
import cv2 as cv
import os
from datetime import date,datetime
from collections import deque


class Queue:
    def __init__(self,buffer=None):
        self.buffer = deque()
        self.max_size = 10
    def enqueue(self, val):
        if len(self.buffer) > self.max_size:
            self.buffer.popleft()
        self.buffer.appendleft(val)
    def dequeue(self):
        if not self.is_empty():
            return self.buffer.pop()
    def is_empty(self):
        return len(self.buffer) == 0
    def size(self):
        return len(self.buffer)

class Detect_Queue(Queue):
    def __init__(self):
        super().__init__()
class Record_Queue(Detect_Queue):
    def __init__(self):
        super().__init__()


def file_handler():
    directory_path = "C:\\Users\\saler\\Desktop\\Programing\\motionDetection\\videos"
    files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if
             os.path.isfile(os.path.join(directory_path, f))]
    now = datetime.now()
    now = now.strftime("%d-%m-%Y_%H-%M-%S")
    files.sort(key=os.path.getctime, reverse=True)
    if files:
        latest_file = files[0]
        latest = latest_file.split("\\")[-1]
        latest_int = int(latest[latest.index("o")+1:latest.find("(")]) + 1
        return f"../videos/video{latest_int}({now}).avi"
    else:
        return f"../videos/video0({now}).avi"



def options_video(cap, flag=False):
    filename = file_handler()
    frames_per_second = 30.0
    res = '480p'
    def change_res(cap, width, height):
        cap.set(3,width)
        cap.set(4,height)

    STD_DIMENSIONS = {
        "480p": (640, 480),
        "720p": (1280, 720),
        "1080p": (1920, 1010),
        "4k": (3840, 2160),
    }
    def get_dims(cap, res="720p"):
        width, height = STD_DIMENSIONS['480p']
        if res in STD_DIMENSIONS:
            width, height = STD_DIMENSIONS[res]
        if not flag:
            change_res(cap,width,height)
        return width, height
    dims = get_dims(cap, res=res)

    VIDEO_TYPE = {
        'avi': cv.VideoWriter_fourcc(*'XVID'),
        # 'mp4': cv2.VideoWriter_fourcc(*'H264'),
        'mp4': cv.VideoWriter_fourcc(*'XVID'),
        "mjpg":cv.VideoWriter_fourcc(*"MJPG"),
    }

    def get_video_type(filename):
        filename, ext = os.path.splitext(filename)
        if ext in VIDEO_TYPE:
            return VIDEO_TYPE[ext]
        return VIDEO_TYPE['avi']
    video_type_cv2 = get_video_type(filename)
    out = cv.VideoWriter(filename, video_type_cv2, frames_per_second, dims) # width, height
    return out

class detect_and_Record:
    def __init__(self,camera_index):
        self.is_recording = False
        self.not_recording = True
        self.haar_cascade = cv.CascadeClassifier('cascades/haar_face.xml')
        self.detect_queue = Detect_Queue()
        self.record_queue = Record_Queue()
        self.display_queue = Queue()
        self.stop_event = threading.Event()
        self.capture = cv.VideoCapture(camera_index)
        if not self.capture.isOpened():
            print("Something went wrong")
        self.record = options_video(self.capture)
        self.lock = threading.Lock()
        self.capture_thread = threading.Thread(target=self.capture_frames, args=())
        self.capture_thread.start()
        #------------------------------------------------------
        self.detect_thread = threading.Thread(target=self.detect)
        self.detect_thread.start()
        self.record_thread = threading.Thread(target=self.record_video)
        self.record_thread.start()
        # --------------------------------------------------------------
        self.display_thread = threading.Thread(target=self.display_frame)
        self.display_thread.start()
        self.pre_timeframe = 0

    def detect(self):
        while not self.stop_event.is_set():
            if not self.detect_queue.is_empty():
                frame = self.detect_queue.dequeue()
                gray_frame = cv.cvtColor(frame, cv.COLOR_BGRA2GRAY)
                faces = self.haar_cascade.detectMultiScale(gray_frame, 1.3, 3)
                if self.not_recording and len(faces) !=0:
                    self.is_recording = True
                    self.not_recording = False
                for (x, y, w, h) in faces:
                    cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if self.is_recording:
                    cv.circle(frame, (40, 60), 20, (0, 0, 255), -1)
                self.display_queue.enqueue(frame)
            if cv.waitKey(1) == ord('q'):
                self.stop_event.set()
                break
        cv.destroyAllWindows()

    def record_video(self):
        duration = 10
        current_time = None
        start_time = True
        while not self.stop_event.is_set():
            if not self.record_queue.is_empty():
                frame = self.record_queue.dequeue()
                if self.is_recording:
                    self.record.write(frame)
                    # This if statement is when the current time is set
                    if start_time:
                        current_time = t.time()
                        start_time = False
                    # This if is when 10 seconds passes
                    if int(t.time()) - int(current_time) >= duration:
                        self.is_recording = False
                        self.not_recording = True
                        start_time = True
                        self.record.release()
                        self.record = options_video(self.capture, flag=True)
            if cv.waitKey(1) == ord('q'):
                self.stop_event.set()
                break
        cv.destroyAllWindows()

    def display_frame(self):
        while not self.stop_event.is_set():
            if not self.display_queue.is_empty():
                frame = self.display_queue.dequeue()
                self.pre_timeframe = self.print_Frames(frame, self.pre_timeframe)
                cv.imshow(f"Live vido 0", frame)
            if cv.waitKey(1) == ord('q'):
                self.stop_event.set()
                break
        cv.destroyAllWindows()
    def capture_frames(self):
        target_fps = 30
        frame_duration = 1.0/target_fps
        while not self.stop_event.is_set():
            start_time = time.time()
            ret, frame = self.capture.read()
            if not ret:
                print("Error: Can't receive frame. Exiting...")
                break
            recording_frame = frame.copy()
            self.record_queue.enqueue(recording_frame)
            self.detect_queue.enqueue(frame)
            # ------------------------------------------------------
            elapsed_time = time.time() - start_time
            time_to_wait = frame_duration - elapsed_time
            if time_to_wait > 0:
                time.sleep(time_to_wait)
            if cv.waitKey(1) == ord('q'):
                self.stop_event.set()
                break
        self.capture.release()
        self.record.release()
        self.capture_thread.join()
        self.display_thread.join()
        self.detect_thread.join()
        self.record_thread.join()
        cv.destroyAllWindows()

    def print_Frames(self,frame, pre_timeframe):
        new_timeframe = t.time()
        fps = int(1 / (new_timeframe - pre_timeframe))
        pre_timeframe = new_timeframe
        cv.putText(frame, f"FPS: {fps}", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
        return pre_timeframe


camera = detect_and_Record(0)
def Tracking_Camera(cap_idx):

    cap = cv.VideoCapture(cap_idx)
    object_detector = cv.createBackgroundSubtractorMOG2()
    while True:
        ret, frame = cap.read()
        # Object detection
        mask = object_detector.apply(frame)
        countours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        for cnt in countours:
            # Calculate area and remove small elements
            area = cv.contourArea(cnt)
            if area > 100:
                cv.drawContours(frame, [cnt], -1, (0,255,0), 2 )

        cv.imshow("Resized", frame)
        # cv.imshow('Mask', mask)

        if cv.waitKey(5) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()