import cv2
import time
from pyfirmata import Arduino, util

from helpers import make_request_json, send_request, determine_trash

board = Arduino("COM3")
iter8 = util.Iterator(board)
iter8.start()
servo = board.get_pin("d:9:s")

CAMERA = cv2.VideoCapture(1)
CAMERA_WARMUP_DURATION = 1 #second
TRASH_STABILISING_DURATION = 2 #seconds
SERVO_ROTATION_DURATION = 2 #seconds
FPS = 25
MIN_BACKGROUND_DIFF = 5000

background = None
trash_detected = False

frame_no = 0
trash_frame_to_process = 0

def rotate_servo(angle):
    servo.write(angle)
    time.sleep(SERVO_ROTATION_DURATION)

rotate_servo(90)

while True:
    frame_no += 1
    time.sleep(1 / FPS)

    ret, frame = CAMERA.read()

    if not ret:
        break
    
    if frame_no == trash_frame_to_process + 1:
        continue

    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grayFrame = cv2.GaussianBlur(grayFrame, (21, 21), 0)
    
    if background is None and frame_no == CAMERA_WARMUP_DURATION * FPS:
        background = grayFrame
    
    if background is not None:
        if not trash_detected:
            frameDiff = cv2.absdiff(background, grayFrame)
            thresh = cv2.threshold(frameDiff, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            _, contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                if cv2.contourArea(contour) > MIN_BACKGROUND_DIFF:
                    trash_detected = True
                    trash_frame_to_process = frame_no + TRASH_STABILISING_DURATION * FPS
        
        if trash_detected and frame_no == trash_frame_to_process:
            _, buffer = cv2.imencode(".png", frame)
            request_json = make_request_json(buffer)
            responses = send_request(request_json)
            trash = determine_trash(responses)

            if trash == "bottle":
                rotate_servo(180)
            else:
                rotate_servo(0)
            
            rotate_servo(90)
            trash_detected = False

    cv2.imshow("frame", frame)

    # ESC
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

CAMERA.release()
cv2.destroyAllWindows()
