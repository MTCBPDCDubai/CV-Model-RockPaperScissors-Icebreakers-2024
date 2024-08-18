import cv2
import supervision as sv
from ultralytics import YOLOv10
import os
import time

model = YOLOv10(f'best.pt')

timer = 0
stateResult = False
startGame = False

cap = cv2.VideoCapture(0)
custom_width = 1280
custom_height = 720
cap.set(3, custom_width)
cap.set(4, custom_height)

bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()

if not cap.isOpened():
    print("Unable to read camera feed")

while True:
    imgBG = cv2.imread("Resources/MTC_bg.png")
    imgBG = cv2.resize(imgBG, (custom_width, custom_height))
    ret, frame = cap.read()
    imgScaled = cv2.resize(frame,(0,0),None,0.625,0.625)
    imgScaled = imgScaled[:,229:491]
    annotated_image=imgScaled
    if not ret:
        break

    if startGame:
        if stateResult is False:
            timer = time.time() - startTime
            cv2.putText(imgBG,str(int(timer)),(630,460),cv2.FONT_HERSHEY_PLAIN,6,(0,0,0),4)
            
            if timer > 3:
                stateResult = True
                timer = 0
        
                results = model(imgScaled)[0]
                detections = sv.Detections.from_ultralytics(results)
                # print("results:",results)
                class_name = detections.data['class_name'][0]
                


                annotated_image = bounding_box_annotator.annotate(scene=imgScaled, detections=detections)
                annotated_image = label_annotator.annotate( scene=annotated_image, detections=detections)

    imgBG[160:610,868:1130] =annotated_image
    cv2.imshow('Webcam', imgBG)
    k = cv2.waitKey(1)
    if k == ord('s'):
        startGame = True
        startTime = time.time()

    if k%256 ==27:
        print("Escape hit, closing...")
        break
    
cap.release()
cv2.destroyAllWindows()