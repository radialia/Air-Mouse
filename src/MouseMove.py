import cv2
import numpy as np

smooth = 5
previousLocation = [0, 0]
currentLocation = [0, 0]


def MouseMove(frame, landmarkList, screen, mouse):
    height, width, channel = frame.shape

    if(len(landmarkList) != 0):
        index_x, index_y = landmarkList[8][1], landmarkList[8][2]

        mouseX = np.interp(index_x, [100, width-100], [0, screen[0]])
        mouseY = np.interp(index_y, [30, height-200], [0, screen[1]])

        currentLocation[0] = previousLocation[0] + \
            (mouseX - previousLocation[0])/smooth

        currentLocation[1] = previousLocation[1] + \
            (mouseY - previousLocation[1])/smooth

        # Mouse cursor
        cv2.circle(frame, (index_x, index_y), 15, (0, 0, 255), cv2.FILLED)
        # Move mouse
        mouse.position = (currentLocation[0], currentLocation[1])
        # Swap values
        previousLocation[0], previousLocation[1] = currentLocation[0], currentLocation[1]
