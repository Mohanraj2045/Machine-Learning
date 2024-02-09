import numpy as np
import mediapipe as mp
import pyautogui
import time
import cv2
import matplotlib.pyplot as plt


class control_action:

    def __init__(self):

        self.button_classes = {"shoot" : "left" , "reload" :  "r" ,  "jump": "space" } 
        

    def process( self, right_hand_landmark):

        self.job = None
        if(self.isShoot(right_hand_landmark)):
            pyautogui.click( button = self.button_classes["shoot"] ,clicks = 11)
            self.job = "shoot"

        elif(self.isLoad(right_hand_landmark)):
            pyautogui.keyDown(self.button_classes["reload"])
            pyautogui.keyUp(self.button_classes["reload"])
            self.job = "reload"

        elif(self.isJump(right_hand_landmark)):
            pyautogui.keyDown(self.button_classes["jump"])
            pyautogui.keyUp(self.button_classes["jump"])
            self.job = "jump"
            
        return  self.job


        

    def isShoot(self,landmark):

        y7,y8 = landmark[7].y , landmark[8].y

        y11,y12 = landmark[11].y , landmark[12].y


        if not (y7 > y8 and y11 > y12):
            return False
        
        y15 , y16 = landmark[15].y , landmark[16].y

        y19 , y20 = landmark[19].y , landmark[20].y

        if (y15 > y16 and y19 > y20):
            return False

        return 1

    def isLoad(self,landmark):

        y11,y12 = landmark[11].y , landmark[12].y
        y15 , y16 = landmark[15].y , landmark[16].y
        y19 , y20 = landmark[19].y , landmark[20].y

        if( not (y11 > y12 and y15 > y16 and y19 > y20)):
            return False

        y8 = landmark[8].y
        y4 = landmark[4].y
        
        if( not (abs(y8-y4) <= 0.1)):
            return False
        return 2
            

    def isJump(self,landmark):

        y7,y8 = landmark[7].y , landmark[8].y

        if(not(y7 > y8)):
            return False

        y11,y12 = landmark[11].y , landmark[12].y
        y15 , y16 = landmark[15].y , landmark[16].y
        y19 , y20 = landmark[19].y , landmark[20].y

        if( (y11 > y12 and y15 > y16  and y19 > y20)):
            return False
        return 3

        


if __name__ == "__main__" :

    mp_hand = mp.solutions.hands
    detector = mp_hand.Hands()

    button = control_action()
    

    cap = cv2.VideoCapture(0)

    while cap.isOpened():

        ret , img = cap.read()
        img = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
        try:
            results = detector.process(img)
            button.process(results.multi_hand_landmarks[0].landmark)
        except:
            pass
        
            
        cv2.imshow("windows" ,img)
    
        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            break
    
    cv2.destroyAllWindows()


        
       
       
        
    
    