import mediapipe as mp
import cv2
import numpy as np
import pyautogui
import math



class move_mouse:

    def __init__(self):

        self.prev_theta = -100

        self.mp_drawings = mp.solutions.drawing_utils

        self.mp_hands = mp.solutions.hands

        

        

    def process(self,multi_hand_landmarks,img,px,height ,width,lenght = 50):

        if(multi_hand_landmarks):

            two_hands = len(multi_hand_landmarks) == 2
            
            for i , hand  in enumerate(multi_hand_landmarks):
    
                self.mp_drawings.draw_landmarks(img , hand , self.mp_hands.HAND_CONNECTIONS , 
                                           self.mp_drawings.DrawingSpec( color = (0,0,255) , thickness = 1 , circle_radius = 2) ,
                                           self.mp_drawings.DrawingSpec(color = (255,0,0) , thickness = 1 ) )
    

          
                if(two_hands):
                   
                    hx , hy = multi_hand_landmarks[0].landmark[0].x , multi_hand_landmarks[0].landmark[0].y
                    
                    if(self.whichhand(px,hx) == "left" ):

                       if(self.isOpened(multi_hand_landmarks[0].landmark)):
                           img , theta = self.angle(multi_hand_landmarks[1].landmark,height,width,img)

                            #FOR SMOOTHNESS
                            # IF THE DIFFERENCE BETWEEN CURRENT THETA AND PREVIOUS THETA WE CAN MOVE IN THE DIRECTION OF PREVIOUS THETA FOR SMOOTHNESS
                            
                           if( abs(self.prev_theta - theta) <= 15):
        
                               self.mouse_move(self.prev_theta,length = lenght)
                               
                           else:
                              
                               self.mouse_move(theta,length = lenght)
                               self.prev_theta = theta
                        
                    else:

                        if(self.isOpened(multi_hand_landmarks[1].landmark)):
                           img , theta = self.angle(multi_hand_landmarks[0].landmark,height,width,img)
                            
                           if( abs(self.prev_theta - theta) <= 15):
        
                               self.mouse_move(self.prev_theta,length = lenght)
                               
                           else:
                              
                               self.mouse_move(theta,length = lenght)
                               self.prev_theta = theta
                        

                    two_hands = False


            return img
            


        return img

    
    def whichhand(self , px,hx):

        if(hx > px):
            return "left"
        return "right"


    def isOpened(self, landmark):

        y1_1 = landmark[4].y
        y1_2 = landmark[3].y
    
        y2_1 = landmark[8].y
        y2_2 = landmark[7].y
    
        y3_1 = landmark[12].y
        y3_2 = landmark[11].y
    
        y4_1 = landmark[16].y
        y4_2 = landmark[15].y
    
        y5_1 = landmark[20].y
        y5_2 = landmark[19].y
    
        if(y1_1 < y1_2 and y2_1 < y2_2 and y3_1 < y3_2 and y4_1 < y4_2 and y5_1 < y5_2):
            return True
            
        return False


    def angle(self,landmark,h,w,img):
        x1 , y1 = w*landmark[8].x , h*landmark[8].y
    
        x2 , y2 = w*landmark[5].x , h*landmark[5].y
    
        radian = np.arctan2(y2-y1,x2-x1)
        
        theta = np.degrees(radian)
    
        if theta < 0:
            theta = 360 + theta
    
        
        return img,theta
    
                            
    def mouse_move(self,theta,length):

        cx , cy  = pyautogui.position()
    
        # To move a position (x , y ) by the angle theta:
        # displacement in x= length⋅cos(angle)
        # displacement in y=length⋅sin(angle)
        # new x =  length + displacement in x
        # new y = lenth   - displacement in y
    
        theta_in_radian = np.radians(theta)
    
        dx = length * math.cos(theta_in_radian)
        dy = length * math.sin(theta_in_radian)
    
        nx = cx + dx
        ny = cy - dy
    
        
        pyautogui.moveTo(nx,ny , _pause = False)
            
            
        
if __name__ == "__main__":

    mp_pose  = mp.solutions.pose.Pose(model_complexity = 1 , min_tracking_confidence  = 0.5 , min_detection_confidence = 0.5)
    mp_hand = mp.solutions.hands.Hands(model_complexity = 1 , min_tracking_confidence  = 0.5 , min_detection_confidence = 0.5)
    
    cap = cv2.VideoCapture(0)

    mouse_mover = move_mouse()

    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    

    while cap.isOpened() :

        ret  , frame = cap.read()


        hand_results = mp_hand.process(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
        pose_results = mp_pose.process(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))

        

        px , py = pose_results.pose_landmarks.landmark[0].x , pose_results.pose_landmarks.landmark[0].y

        multi_hand_landmarks = hand_results.multi_hand_landmarks

        frame = mouse_mover.process(multi_hand_landmarks,frame,px,height,width)
    
        cv2.imshow("windows",frame)


        if cv2.waitKey(10) & 0xFF == ord('q'):
            cap.release()
            break
    
    cv2.destroyAllWindows()
        

    