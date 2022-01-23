import cv2
import mediapipe as mp
from threading import Thread


class Detector():
    def __init__(self, mode=False, maxHands=1, model_complexity=0, detectionCon=0.7, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.model_complexity = model_complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.mpDraw = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.tipIds = [4, 8, 12, 16, 20]

    def start(self):
        Thread(target=self.startDetecting, args=()).start()
        return self

    def startDetecting(self):
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.model_complexity,
                                        min_detection_confidence=self.detectionCon, min_tracking_confidence=self.trackCon)

    def findIndex(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        self.landmarkList = []

        if self.results.multi_hand_landmarks:
            for landmark in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(
                    img,
                    landmark,
                    self.mpHands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style())
            for id, landmark in enumerate(self.results.multi_hand_landmarks[0].landmark):
                height, width, _ = imgRGB.shape
                x, y = int(landmark.x * width), int(landmark.y * height)
                self.landmarkList.append([id, x, y])

        return self.landmarkList

    def fingerIsUp(self):
        self.fingersUp = []

        if(self.landmarkList):
            if(self.landmarkList[self.tipIds[0] - 1][1] > self.landmarkList[self.tipIds[0]][1]):
                self.fingersUp.append(1)
            else:
                self.fingersUp.append(0)

            for id in range(1, 5):
                if self.landmarkList[self.tipIds[id]][2] < self.landmarkList[self.tipIds[id] - 2][2]:
                    self.fingersUp.append(1)
                else:
                    self.fingersUp.append(0)
        return self.fingersUp

    def findCenter(self):
        pass
