# Importing required modules
from imutils.video import WebcamVideoStream
import imutils
import cv2
import time
import numpy as np
import HandDetector
import pyautogui
import math
from pynput.mouse import Button, Controller

# Get the controller object
mouse = Controller()
# Initialise the camera object
vs = WebcamVideoStream(src=0).start()

# Initialise hand detection
detector = HandDetector.Detector().start()
# Get the screen size
screen = pyautogui.size()

# Required variables
pTime = 0
smooth = 5
previousLocation = [0, 0]
currentLocation = [0, 0]

while True:
    # Read the frame
    frame = vs.read()
    # Resize the frame's width to 600px
    frame = imutils.resize(frame, width=1000)
    # Flip the frame to selfie mode
    frame = cv2.flip(frame, 1)

    # Get the height, width and channel from the frame
    height, width, channel = frame.shape

    # Get FPS
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    # Show FPS
    cv2.putText(frame, f"FPS: {int(fps)}",
                (40, 40), cv2.FONT_HERSHEY_PLAIN, 2, (10, 0, 18), 2)

    # Show instruction to quit the window
    cv2.putText(frame, f"Press 'q' to exit",
                (40, 80), cv2.FONT_HERSHEY_PLAIN, 2, (10, 0, 18), 2)

    # Finds index of each landmark on the recognised hand
    landmarkList = detector.findIndex(frame)
    # Get which fingers are raised up
    fingers = detector.fingerIsUp()

    # Make the movable area
    cv2.rectangle(frame, (100, 30), (width-100, height-200), (0, 255, 0), 2)

    if(len(landmarkList) != 0):
        # Gets landmarks of index and middle finger
        thumb_x, thumb_y = landmarkList[4][1], landmarkList[4][2]
        index_x, index_y = landmarkList[8][1], landmarkList[8][2]
        middle_x, middle_y = landmarkList[12][1], landmarkList[12][2]

        # Convert the finger coordinates into screen coordinates
        mouseX = np.interp(index_x, [100, width-100], [0, screen[0]])
        mouseY = np.interp(index_y, [30, height-200], [0, screen[1]])
        # Make the cursor go to the extreme corner
        pyautogui.FAILSAFE = False

        # If the index finger is only raised up
        if(fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0):
            # Making mouse smooth
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

        # If the index and middle finger is both up
        if(fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0):
            # Make indicator at index finger, middle finger and a line between them
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
                mouse.click(Button.left)
            if(distance > 50):
                cv2.circle(frame, (center_x, center_y),
                           15, (0, 0, 255), cv2.FILLED)

    # Show the frame in a window
    cv2.imshow("AI Mouse", frame)
    # Updates the frame simulataneously

    # If the 'q' key is pressed then exit the window
    if(cv2.waitKey(5) & 0xFF == ord('q')):
        break

# destroy all the windows
cv2.destroyAllWindows()
# Stop recording
vs.stop()
