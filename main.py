import cv2
import HandDetector

# Initialise camera object
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Set the width and height of the opencv window
cap.set(3, 800)
cap.set(4, 500)

# Initialise hand detection
detector = HandDetector.Detector()

while cap.isOpened():
    # Reads the camera
    success, video = cap.read()
    if not success:
        print("Ignoring empty camera frame....")
        continue

    # Flip the screen to give a selfie view
    video = cv2.flip(video, 1)

    # Finds index of each landmark on the recognised hand
    landmarkList = detector.findIndex(video)

    if(len(landmarkList) != 0):
        # Gets landmarks of index finger
        index_tip = landmarkList.get(8)

        if(index_tip):
            # Get the x and y coordinates from the landmarks
            index_tip_x, index_tip_y = index_tip[0], index_tip[1]

            # Draw circles on the indexes and a line in between them
            cv2.circle(video, (index_tip_x, index_tip_y-15),
                       15, (94, 138, 255), cv2.FILLED)

    # Show the window
    cv2.imshow('AI Mouse', video)
    # Press 'q' to quit window
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# Release the camera
cap.release()
