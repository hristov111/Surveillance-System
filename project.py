import threading
import time as t
from datetime import date
import cv2 as cv
import os
from datetime import date,datetime
import numpy as np
from collections import deque


class Queue:
    def __init__(self,buffer=None):
        self.buffer = deque()
    def enqueue(self, val):
        self.buffer.appendleft(val)
    def dequeue(self):
        return self.buffer.pop()
    def is_empty(self):
        return len(self.buffer) == 0
    def size(self):
        return len(self.buffer)

class Dict:
    def __init__(self):
        self.dict = {}
    def add(self,canvas, is_recording,not_recording):
        self.dict['canvas'] = canvas
        self.dict['is_recording'] = is_recording
        self.dict['not_recording'] = not_recording
    def clear(self):
        self.dict.clear()

    def size(self):
        return len(self.dict)
    def empty(self):
        return len(self.dict) == 0

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
    frames_per_second = 15.0
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

def detect(frame,recording,not_recording):
    haar_cascade = cv.CascadeClassifier('cascades/haar_face.xml')
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGRA2GRAY)
    faces = haar_cascade.detectMultiScale(gray_frame, 1.3,4)
    for(x,y,w,h) in faces:
        if not_recording:
            recording = True
            not_recording = False
        cv.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
    return (frame,recording,not_recording)


def print_Frames(frame, pre_timeframe):
    new_timeframe = t.time()
    fps = int(1 / (new_timeframe - pre_timeframe))
    pre_timeframe = new_timeframe
    cv.putText(frame, f"FPS: {fps}", (10,30), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1)
    return pre_timeframe
stop_event = threading.Event()
def display_frame(queue, idx,stop_event):
    frame = None
    while not stop_event.is_set():
        if not queue.is_empty():
            frame = queue.dequeue()
            cv.imshow(f"Live vido {idx}", frame)
        if cv.waitKey(1) == ord('q'):
            stop_event.set()
            break
    cv.destroyAllWindows()





def Inner_Camera(camera_index):
    duration = 10
    start_time = True
    current_time = None
    is_recording = False
    not_recording = True
    queue = Queue()
    dict = Dict()
    capture = cv.VideoCapture(camera_index)
    display_thread = threading.Thread(target=display_frame, args=(queue, camera_index,stop_event))
    display_thread.start()
    detect_thread = threading.Thread(target=detect, args=())
    if not capture.isOpened():
        return "Something went wrong"
    record = options_video(capture)
    pre_timeframe = 0
    while not stop_event.is_set():
        ret, frame = capture.read()
        if not ret:
            print("Error: Can't receive frame. Exiting...")
            break
        # Recording ------------------------------------------------
        if is_recording:
            record.write(frame)
            cv.circle(frame, (40, 60), 20, (0, 0, 255), -1)
            # This if statement is when the current time is set
            if start_time:
                current_time = t.time()
                start_time = False
            # This if is when 10 seconds passes
            if int(t.time()) - int(current_time) >= duration:
                is_recording = False
                not_recording = True
                start_time = True
                record.release()
                record = options_video(capture, flag=True)
        # -----------------------------------------------------
        # FPS Displaying
        pre_timeframe = print_Frames(frame, pre_timeframe)
        # ------------------------------------------------------
        canvas,is_recording,not_recording = detect(frame,is_recording,not_recording)
        # Add to the queue
        queue.enqueue(canvas)
        # Display from the queue
        if cv.waitKey(1) == ord('q'):
            break
    capture.release()
    display_thread.join()
    record.release()
    cv.destroyAllWindows()

# This is threeading between the capture and the displaying
capture_thread = threading.Thread(target=Inner_Camera, args=("http://192.168.0.123:4747/video",))
capture_thread.start()
capture_thread.join()




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

# Outside_Camera("OpenCv/Photos/highway.mp4")

