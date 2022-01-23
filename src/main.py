# Importing required modules
from imutils.video import WebcamVideoStream
import imutils
import cv2
import time
import HandDetector
import pyautogui
from pynput.mouse import Controller


from MouseMove import MouseMove
from MouseClick import MouseClick
from MouseDragDrop import MouseDragDrop

# Get the controller object
mouse = Controller()
# Initialise the camera object
vs = WebcamVideoStream(src=1).start()

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
        # Make the cursor go to the extreme corner
        pyautogui.FAILSAFE = False

        # If the index finger is only raised up
        if(fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0):
            MouseMove(frame, landmarkList, screen, mouse)

        # If the index and middle finger is both up
        if(fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1):
            MouseClick(frame, landmarkList, mouse)

        # If the thumb and index finger is both up
        if(fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0):
            MouseDragDrop(frame, landmarkList, mouse)

    # Show the frame in a window
    cv2.imshow("Air Mouse", frame)

    # If the 'q' key is pressed then exit the window
    if(cv2.waitKey(5) & 0xFF == ord('q')):
        break

# destroy all the windows
cv2.destroyAllWindows()
# Stop recording
vs.stop()
