import threading
import time
import time as t
import cv2 as cv
import os
from datetime import datetime
from collections import deque
import calendar
import shutil


class Queue:
    def __init__(self,buffer=None):
        self.buffer = deque()
        self.max_size = 50
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

# date: 11-02-2024
# time: 18-47-59
def make_dirs(latest_day,latest_date,next):
    if int(latest_date) < int(next[1]):
            os.makedirs(f"C:\\Users\\saler\\Desktop\\Programing\\motionDetection\\videos\\{next[1]}\\{next[0]}",exist_ok=True)
            return f'C:\\Users\\saler\\Desktop\\Programing\\motionDetection\\videos\\{next[1]}\\{next[0]}'
    elif int(latest_day) < int(next[0]):
            os.makedirs(f"C:\\Users\\saler\\Desktop\\Programing\\motionDetection\\videos\\{latest_date}\\{next[0]}",exist_ok=True)
            return f'C:\\Users\\saler\\Desktop\\Programing\\motionDetection\\videos\\{latest_date}\\{next[0]}'
    elif int(latest_day) == int(next[0]) and int(latest_date) == int(next[1]):
        return f"C:\\Users\\saler\\Desktop\\Programing\\motionDetection\\videos\\{latest_date}\\{latest_day}"

def make_empty_dirs():
    month_path = "C:\\Users\\saler\\Desktop\\Programing\\motionDetection\\videos"
    all_entries = os.listdir(month_path)
    month_dirs = [entry for entry in all_entries if os.path.isdir(os.path.join(month_path, entry))]
    if len(month_dirs) > 2:
        delete_dir(f"C:\\Users\\saler\\Desktop\\Programing\\motionDetection\\videos\\{month_dirs[0]}")
    next = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    date,_ = next.split("_")
    date= date.split('-')
    if month_dirs:
        latest_month_dir = month_dirs[-1]
        day_path = f"C:\\Users\\saler\\Desktop\\Programing\\motionDetection\\videos\\{latest_month_dir}"
        all_day_entries = os.listdir(day_path)
        day_dirs = [entry for entry in all_day_entries if os.path.isdir(os.path.join(day_path, entry))]
        if day_dirs:
            latest_day_dir = day_dirs[-1]
            return make_dirs(latest_day_dir,latest_month_dir,date)
        else:
            os.makedirs(f"C:\\Users\\saler\\Desktop\\Programing\\motionDetection\\videos\\{latest_month_dir}\\{date[0]}",exist_ok=True)
            return f"C:\\Users\\saler\\Desktop\\Programing\\motionDetection\\videos\\{latest_month_dir}\\{date[0]}"
    else:
        os.makedirs(f"C:\\Users\\saler\\Desktop\\Programing\\motionDetection\\videos\\{date[1]}\\{date[0]}", exist_ok=True)
        return f"C:\\Users\\saler\\Desktop\\Programing\\motionDetection\\videos\\{date[1]}\\{date[0]}"

def file_handler():
    directory_path = make_empty_dirs()
    files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if
             os.path.isfile(os.path.join(directory_path, f))]
    now = datetime.now()
    now = now.strftime("%d-%m-%Y_%H-%M-%S")
    files.sort(key=os.path.getctime, reverse=True)
    if files:
        latest_file = files[0]
        latest = latest_file.split("\\")[-1]
        latest_int = int(latest[latest.index("o") + 1:latest.find("(")]) + 1
        return f"{directory_path}\\video{latest_int}({now}).avi"
    else:
        return f"{directory_path}\\video0({now}).avi"
def delete_dir(path):
    shutil.rmtree(path)


def options_video(cap, flag=False):
    filename = file_handler()
    frames_per_second = 8
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
        self.camera_index = camera_index
        self.haar_cascade = cv.CascadeClassifier('cascades/haar_face.xml')
        self.detect_queue = Detect_Queue()
        self.record_queue = Record_Queue()
        self.display_queue = Queue()
        self.stop_event = threading.Event()
        self.capture = cv.VideoCapture(camera_index)
        self.detection_back = cv.createBackgroundSubtractorMOG2(history=100, varThreshold=40)
        if not self.capture.isOpened():
            print("Something went wrong")
        self.record = options_video(self.capture)
        #------------------------------------------------------
        self.detect_thread = threading.Thread(target=self.detect)
        self.record_thread = threading.Thread(target=self.record_video)
        # --------------------------------------------------------------
        self.pre_timeframe = 0

    def detect(self):
        while not self.stop_event.is_set():
            if not self.detect_queue.is_empty():
                find_countorurs = False
                frame = self.detect_queue.dequeue()
                # gray_frame = cv.cvtColor(frame, cv.COLOR_BGRA2GRAY)
                mask = self.detection_back.apply(frame)
                c,_ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
                for cnt in c:
                    area = cv.contourArea(cnt)
                    if area > 500:
                        x,y,w,h = cv.boundingRect(cnt)
                        cv.rectangle(frame,(x,y), (x+w, y+h), (0,255,0), 3)
                        find_countorurs = True
                if self.not_recording and find_countorurs:
                    self.is_recording = True
                    self.not_recording = False
                if self.is_recording:
                    cv.circle(frame, (40, 60), 20, (0, 0, 255), -1)
                self.pre_timeframe = self.print_Frames(frame, self.pre_timeframe)
                cv.imshow(f"Live {self.camera_index}", frame)
            if cv.waitKey(1) == ord('q'):
                self.stop_event.set()
                break

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

    def capture_frames(self):
        self.detect_thread.start()
        self.record_thread.start()
        target_fps = 8
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
capture_thread = threading.Thread(target=camera.capture_frames)
capture_thread.start()
capture_thread.join()
