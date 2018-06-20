#！/bin/python
#--*-- coding: utf-8 --*--

import cv2
import sys
from PIL import Image

def CatchUsbVideo(windowName, cameraIdx):
  cv2.namedWindow(windowName)

  cap = cv2.VideoCapture(cameraIdx)

  classfier = cv2.CascadeClassifier("./haarcascades/haarcascade_frontalface_alt2.xml")
  color = (0, 255, 0)
  
  while cap.isOpened:
    ok, frame = cap.read()
    if not ok:
      break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faceRects = classfier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
    if len(faceRects) > 0:
      for faceRect in faceRects:
        x, y, w, h = faceRect
        cv2.rectangle(frame, (x-10, y-10), (x+w+10, y+h+10), color, 2)

    cv2.imshow(windowName, frame)
    c = cv2.waitKey(10)
    if c & 0xFF == ord('q'):
      break
  
  cap.release()
  cv2.destroyAllWindows()

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print("Usage: %s camera_id\n" % (sys.argv[0]))
  else:
    CatchUsbVideo("截取视频流", int(sys.argv[1]))