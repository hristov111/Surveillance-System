import threading
import time as t
from datetime import date
import cv2 as cv
import cv2
import os
from datetime import date,datetime
import mss
import numpy as np

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
        return "../videos/video0.avi"



def options_video(cap, flag=False):
    filename = file_handler()
    frames_per_second = 10.0
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
        'avi': cv2.VideoWriter_fourcc(*'XVID'),
        # 'mp4': cv2.VideoWriter_fourcc(*'H264'),
        'mp4': cv2.VideoWriter_fourcc(*'XVID'),
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

def detect(gray, frame,recording,not_recording, duration):
    haar_cascade = cv.CascadeClassifier('cascades/haar_face.xml')
    faces = haar_cascade.detectMultiScale(gray, 1.3,4)
    for(x,y,w,h) in faces:
        if not_recording:
            recording = True
            not_recording = False
        cv.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
    return (frame,recording,not_recording,duration)



def Inner_Camera(camera_index):
    duration = 10
    start_time = True
    current_time = None
    is_recording = False
    not_recording = True
    capture = cv.VideoCapture(camera_index)
    if not capture.isOpened():
        return "Something wen wrong"
    record = options_video(capture)
    pre_timeframe = 0
    with mss.mss() as sct:
        monitor = {'top':0, "left":0, 'width': 640, 'height':480}
        while True:
            # ret, frame = capture.read()
            screenshot = sct.grab(monitor)
            frame = np.array(screenshot)
            frame = cv.cvtColor(frame, cv.COLOR_BGRA2BGR)
            # if not ret:
            #     print("Error: Can't receive frame. Exiting...")
            # Recording
            if is_recording:
                record.write(frame)
                cv.circle(frame, (40,60), 20, (0,0,255),-1)
                # This if statement is when the current time is set
                if start_time:
                    current_time = t.time()
                    start_time = False
                print(int(t.time()) - int(current_time))
                # This if is when 10 seconds passes
                if int(t.time()) - int(current_time) >= duration:
                    is_recording = False
                    not_recording = True
                    start_time = True
                    record.release()
                    record = options_video(capture,flag=True)
            # FPS Displaying
            new_timeframe = t.time()
            fps = int(1/(new_timeframe-pre_timeframe))
            pre_timeframe = new_timeframe
            cv.putText(frame, f"FPS: {fps}", (10,30), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1)

            gray_frame = cv.cvtColor(frame, cv.COLOR_BGRA2GRAY)
            canvas,is_recording,not_recording,duration = detect(gray_frame, frame,is_recording,not_recording,duration=duration)

            cv.imshow(f"Live video {camera_index}", canvas)

            if cv.waitKey(1) == ord('q'):
                break
        capture.release()
        record.release()
        cv.destroyAllWindows()

Inner_Camera(0)



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

