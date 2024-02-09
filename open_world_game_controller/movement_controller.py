import pickle
import numpy as np
import time
import pyautogui
import mediapipe as mp
import cv2



class control_movement :

    def __init__(self):

        self.hand_landmarks = [11,13,15,17,19,21,12,14,16,18,20,22]
        self.model = pickle.load( open("direction_of_motion_detctor.pkl" , "rb"))
        self.classes = {0 : "None" , 1 :"up" , 2 : "down", 3 : "left", 4 : "right"  }
        self.buttons = {1 : "w" , 2 : "s" , 3 : "a" , 4 : "d" }
        self.prev = 0
        self.hold = False

    def process(self,landmarks):

        s = np.array( [[landmarks[i].x , landmarks[i].y , landmarks[i].x , landmarks[i].visibility] for i in self.hand_landmarks]).flatten().reshape(1,-1)

        p = int(self.model.predict(s)[0])

        if(p == 0): 
            if(self.hold):
                self.hold = False
                print(self.buttons[self.prev])
                pyautogui.keyUp(self.buttons[self.prev])
            self.prev = 0

            return  [None , self.classes[0]]
        else:
            
            if(p != self.prev ):
                
                if(self.hold):
                    pyautogui.keyUp(self.buttons[self.prev])
                self.prev = p
                pyautogui.keyDown(self.buttons[p])

            self.hold = True
           
            return  [p , self.classes[p]]
                


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)

    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    control = control_movement()

    mp_pose = mp.solutions.pose.Pose()

    while True:

        ret , frame = cap.read()
        results = mp_pose.process(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
        l,frame = control.process(results.pose_landmarks.landmark,frame)

        cv2.imshow("windows" ,frame)

        

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()