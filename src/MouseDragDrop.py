import cv2
import math
from pynput.mouse import Button

def MouseDragDrop(frame, landmarkList, mouse):
    dragged = False
    if(len(landmarkList) != 0):
        # Gets landmarks of index and middle finger
        thumb_x, thumb_y = landmarkList[4][1], landmarkList[4][2]
        index_x, index_y = landmarkList[8][1], landmarkList[8][2]

        cv2.circle(frame, (thumb_x, thumb_y),
                   15, (255, 0, 0), cv2.FILLED)
        cv2.circle(frame, (index_x, index_y), 15, (255, 0, 0), cv2.FILLED)

        cv2.line(frame, (thumb_x, thumb_y),
                 (index_x, index_y), (255, 255, 0), 2)

        # Calculate center
        center_x, center_y = (thumb_x+index_x)//2, (thumb_y+index_y)//2

        # Get distance
        distance = math.sqrt(
            math.pow((thumb_x-index_x), 2) + math.pow((thumb_y-index_y), 2))

        # Detect distance
        if(distance < 50):
            cv2.circle(frame, (center_x, center_y),
                       15, (0, 255, 0), cv2.FILLED)
            if(dragged != True):
                mouse.press(Button.left)
                dragged = True
        if(distance > 50):
            cv2.circle(frame, (center_x, center_y),
                       15, (0, 0, 255), cv2.FILLED)
            mouse.release(Button.left)
            dragged = False
