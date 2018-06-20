#！/bin/python
#--*-- coding: utf-8 --*--

import cv2
import sys
from PIL import Image

def CatchPICFromVideo(windowName, cameraIdx, catchPicNum, pathName):
  cv2.namedWindow(windowName)

  cap = cv2.VideoCapture(cameraIdx)

  classfier = cv2.CascadeClassifier("./haarcascades/haarcascade_frontalface_alt2.xml")
  color = (0, 255, 0)
  
  num = 0
  while cap.isOpened:
    ok, frame = cap.read()
    if not ok:
      break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faceRects = classfier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
    if len(faceRects) > 0:
      for faceRect in faceRects:
        x, y, w, h = faceRect

        imgName = '%s/%d.jpg' % (pathName, num)
        image = frame[y-10:y+h+10, x-10:x+w+10]
        cv2.imwrite(imgName, image)

        num += 1
        if num > (catchPicNum):
          break

        cv2.rectangle(frame, (x-10, y-10), (x+w+10, y+h+10), color, 2)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, 'num:%d' % (num), (x+30, y+30), font, 1, (255, 0, 255), 4)

    if num > (catchPicNum): break

    cv2.imshow(windowName, frame)
    c = cv2.waitKey(10)
    if c & 0xFF == ord('q'):
      break
  
  cap.release()
  cv2.destroyAllWindows()

if __name__ == '__main__':
  if len(sys.argv) != 4:
    print("Usage: %s camera_id face_num_max path_name\n" % (sys.argv[0]))
  else:
    CatchPICFromVideo("截取人脸", int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])