import cv2
import os
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
             

import numpy as np

frame_RATE = 5

# STEP 2: Create an HandLandmarker object.
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options,
                                       num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)


mp_hands = mp.solutions.hands.Hands(static_image_mode=True, 
                                    max_num_hands=2, 
                                    min_detection_confidence=0.2,  # Adjust this value as needed
                                    min_tracking_confidence=0.2)

mp_pose = mp.solutions.pose.Pose(static_image_mode=True,                                     
                                    min_detection_confidence=0.2,  # Adjust this value as needed
                                    min_tracking_confidence=0.2)

def draw_landmarks(image, landmarks):
    for landmark in landmarks:
        x, y = int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)

def Handdraw_landmarks_on_image(rgb_image, detection_result):
  hand_landmarks_list = detection_result.multi_hand_landmarks
  annotated_image = np.copy(rgb_image)

  # Loop through the detected hands to visualize.
  for idx in range(len(hand_landmarks_list)):
    hand_landmarks = hand_landmarks_list[idx]

    # Draw the hand landmarks.
    hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
    hand_landmarks_proto.landmark.extend([
      landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
    ])
    solutions.drawing_utils.draw_landmarks(
      annotated_image,
      hand_landmarks_proto,
      solutions.hands.HAND_CONNECTIONS,
      solutions.drawing_styles.get_default_hand_landmarks_style(),
      solutions.drawing_styles.get_default_hand_connections_style())

    # Get the top left corner of the detected hand's bounding box.
    height, width, _ = annotated_image.shape
    x_coordinates = [landmark.x for landmark in hand_landmarks]
    y_coordinates = [landmark.y for landmark in hand_landmarks]
    # Draw handedness (left or right hand) on the image.
    

  return annotated_image

def fill_empty_landmarks(landmark_count):
    landmarks = []
    for item in range(landmark_count):
        landmarks.append((0,0))
    return landmarks
    

def get_pose_landmarks(pose_landmarker_result):
    
    if not pose_landmarker_result.pose_landmarks:
        return fill_empty_landmarks(33)
    
    pose_landmarks = []        
        
    for landmark in pose_landmarker_result.pose_landmarks.landmark:
        x, y = landmark.x, landmark.y 
        pose_landmarks.append((x,y))
    
    return pose_landmarks

def get_hand_landmarks(hand_landmarker_result):
    
    if not hand_landmarker_result.multi_hand_landmarks:
        return fill_empty_landmarks(42)
    
    landmarks = []        
    if len( hand_landmarker_result.multi_hand_landmarks) != 2:
        landmarks = landmarks + fill_empty_landmarks(21)
        
    for hand_landmarks in hand_landmarker_result.multi_hand_landmarks:
        
        for landmark in hand_landmarks.landmark:
            x, y = landmark.x, landmark.y 
            landmarks.append((x,y))
    return landmarks

def Create_array(detection_result):
    hand_landmarks_list = detection_result.hand_landmarks
    handedness_list = detection_result.handedness

def Fill_Datset(folderName,dataset,labels,class_number):
    # assign directory
    
    # iterate over files in
    # that directory
    
    #while(True):
    '''
        multiarray = []
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        hand_landmarker_result = mp_hands.process(image_rgb)
        #Solutions is how u get multi hands but are they any good 
        
        
        print(hand_landmarker_result.multi_hand_landmarks)
        if hand_landmarker_result.multi_hand_landmarks:
            for hand_landmarks in hand_landmarker_result.multi_hand_landmarks:
                draw_landmarks(image_rgb, hand_landmarks.landmark)
        cv2.imshow("results",image_rgb)
    '''
    for filename in os.listdir(folderName):
        
        path = os.path.join(folderName , filename)
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            continue
        #Test if video exists needs to be out here so if it needs to it can skip to the next one 
        
        flipped = False
        #For each video process it normally then flip it 
        
        for item in range(2):
            cap = cv2.VideoCapture(path)
           
            multiarray = []
            frame_counter = 0
            '''
            for item in range(20):
                ret, frame = cap.read()
                
                # Check if there are frames remaining
                if not ret:
                    print("No more frames available")
                    break
             ''' # This is whetre we skip frames if needed
                           
            
            for item in range(25):   
                
                ret, frame = cap.read()
                
                # Check if there are frames remaining
                if not ret:
                    print("No more frames available")
                    break
                
                if flipped != False:
                    frame = cv2.flip(frame,1)
                    
                    
                #Now we have a indidual frame
                if item % 2 == 0:
                    #get every 5 frames for a overall rate of 5 fps
                                        
                    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    hand_landmarker_result = mp_hands.process(image_rgb)
                    pose_landmarker_result = mp_pose.process(image_rgb)
                    
                    #Solutions is how u get multi hands but are they any good 
                    '''
                    if hand_landmarker_result.multi_hand_landmarks:
                        for hand_landmarks in hand_landmarker_result.multi_hand_landmarks:
                            draw_landmarks(image_rgb, hand_landmarks.landmark)
                        
                    if pose_landmarker_result.pose_landmarks:
                            draw_landmarks(image_rgb, pose_landmarker_result.pose_landmarks.landmark)
                    cv2.imshow("results",image_rgb)
                    
                    cv2.waitKey(0)
                    '''
                    hand_landmarks = get_hand_landmarks(hand_landmarker_result)
                    pose_landmarks = get_pose_landmarks(pose_landmarker_result)
                    multiarray.append(hand_landmarks + pose_landmarks)
                    
            for item in range(13 - len(multiarray)):
                multiarray.append(fill_empty_landmarks(75))
            
            dataset.append(multiarray)
            print(folderName)
            print(folderName.split("\\")[1])
            labels.append(class_number)
            
            flipped = True
            
        
        print(len(dataset))
    
    #print(dataset)
    set = np.array(dataset)
    print("YEEEEEEAHHHHHHHHHHHHHHHHHHHH")

def CreateDictionary():
    action_dictionary = {}
    e = open("Words_Used", "r")
    for line in e:
        line_array = line.split(',')
        action_dictionary[line_array[0]] = line_array[1]
    return action_dictionary
        
     
                    
def CreateDataset(folder_Name):

    entries = os.listdir(folder_Name)
    dataset = []
    labels = []
    class_number = 0
    action_dictionary = CreateDictionary()
    
    e = open("number_to_label.txt", "w")
    e.write("label,number,action")
    for item in entries:
        print(item)
        path = os.path.join(folder_Name,item)
        Fill_Datset(path,dataset,labels,class_number)
        e.write("\n")
        
        e.write(str(class_number) +","+ item+","+ action_dictionary[item])
        
        class_number = class_number + 1
    e.close()
    
    f = open("Dataset_Final.txt", "w")
    f.write("label,data")
    
    for item in range(len(dataset) -1):
        print(str(item) )
        f.write("\n")
        
        f.write(str(labels[item] )+"," +str(dataset[item])+",")
        
    f.close()
     
    
CreateDataset("E:\\Comp208\\VideoFiles\\Frames")
    