import cv2
import math
from pynput.mouse import Button


def MouseClick(frame, landmarkList, mouse):

    clicked = False
    if(len(landmarkList) != 0):
        # Gets landmarks of index and middle finger
        index_x, index_y = landmarkList[8][1], landmarkList[8][2]
        middle_x, middle_y = landmarkList[12][1], landmarkList[12][2]

        cv2.circle(frame, (index_x, index_y), 15, (255, 0, 0), cv2.FILLED)
        cv2.circle(frame, (middle_x, middle_y),
                   15, (255, 0, 0), cv2.FILLED)
        cv2.line(frame, (index_x, index_y),
                 (middle_x, middle_y), (255, 255, 0), 2)

        # Calculate center
        center_x, center_y = (index_x+middle_x)//2, (index_y+middle_y)//2

        # Get distance
        distance = math.sqrt(
            math.pow((index_x-middle_x), 2) + math.pow((index_y-middle_y), 2))

        # Detect distance
        if(distance < 50):
            cv2.circle(frame, (center_x, center_y),
                       15, (0, 255, 0), cv2.FILLED)
            if(clicked != True):
                mouse.click(Button.left, 1)
                clicked = True
        if(distance > 50):
            cv2.circle(frame, (center_x, center_y),
                       15, (0, 0, 255), cv2.FILLED)
            clicked = False
