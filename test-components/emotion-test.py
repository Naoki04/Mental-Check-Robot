import apiFunctions as api
import cv2
import time

device_num = 1
cap = cv2.VideoCapture(device_num)
time.sleep(1)
filename = api.capture_image(cap)
result = api.emotion_recognition(filename)
#メモリを解放して終了するためのコマンド
cap.release()
cv2.destroyAllWindows()