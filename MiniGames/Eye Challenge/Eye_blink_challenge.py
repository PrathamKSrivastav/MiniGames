import numpy as np
import cv2
import time

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')

first_read = True
eyes_open_start_time = None

cap = cv2.VideoCapture(0)
ret, img = cap.read()
while(ret):
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 5, 1, 1)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(200, 200))
    if(len(faces)>0):
        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            roi_face = gray[y:y+h, x:x+w]
            roi_face_clr = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_face, 1.3, 5, minSize=(50, 50))
            if(len(eyes)>=2):
                if(first_read):
                    cv2.putText(img, "press s to begin", (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2)
                else:
                    if eyes_open_start_time is None:
                        eyes_open_start_time = time.time()
                    else:
                        elapsed_time = time.time() - eyes_open_start_time
                        cv2.putText(img, f"Eyes Open for: {elapsed_time:.2f} seconds", (100, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2)
                        print(f"Eyes open for: {elapsed_time:.2f} seconds")
            else:
                if(first_read):
                    cv2.putText(img, "No eyes detected", (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2)
                else:
                    print(" you loose")
                    first_read = True
                    eyes_open_start_time = None
    else:
        cv2.putText(img,"No face detected",(100,100),cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0),2)

    cv2.imshow('img',img)
    a = cv2.waitKey(1)
    if(a==ord('q')):
        break
    elif(a==ord('s') and first_read):
        first_read = False

cap.release()
cv2.destroyAllWindows()
