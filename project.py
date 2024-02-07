import threading
import time as t
import cv2 as cv
import cv2
import os
def options_video(cap):
    filename = '../video.avi'
    frames_per_second = 24.0
    res = '720p'
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
        change_res(cap,width,height)
        return width, height
    dims = get_dims(cap, res=res)

    VIDEO_TYPE = {
        'avi': cv2.VideoWriter_fourcc(*'XVID'),
        # 'mp4': cv2.VideoWriter_fourcc(*'H264'),
        'mp4': cv2.VideoWriter_fourcc(*'XVID'),
    }

    def get_video_type(filename):
        filename, ext = os.path.splitext(filename)
        if ext in VIDEO_TYPE:
            return VIDEO_TYPE[ext]
        return VIDEO_TYPE['avi']
    video_type_cv2 = get_video_type(filename)
    out = cv.VideoWriter(filename, video_type_cv2, frames_per_second, dims) # width, height
    return out

def detect(gray, frame):
    haar_cascade = cv.CascadeClassifier('cascades/haar_face.xml')
    faces = haar_cascade.detectMultiScale(gray, 1.3,3)
    for(x,y,w,h) in faces:
        cv.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
    return frame



def Inner_Camera(camera_index):
    is_recording = False
    capture = cv.VideoCapture(camera_index)
    if not capture.isOpened():
        print("Something wen wrong")
    record = options_video(capture)
    pre_timeframe = 0
    while True:
        ret, frame = capture.read()
        if not ret:
            print("Error: Can't receive frame. Exiting...")
        # FPS Displaying
        new_timeframe = t.time()
        fps = int(1/(new_timeframe-pre_timeframe))
        pre_timeframe = new_timeframe
        cv.putText(frame, f"FPS: {fps}", (10,30), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1)

        gray_frame = cv.cvtColor(frame, cv.COLOR_BGRA2GRAY)
        canvas = detect(gray_frame, frame)
        cv.imshow(f"Live video {camera_index}", canvas)

        if cv.waitKey(1) == ord('q'):
            break

    capture.release()
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

