from django.shortcuts import render
from django.http import HttpResponse
import os
import cv2
import numpy as np
import mediapipe as mp
# import uuid
from deepface import DeepFace as df
import tempfile
from django.http import JsonResponse
from .models import *
import pickle
from bson.binary import Binary
import shutil
from retinaface import RetinaFace as rf
#from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt
# Create your views here.

def home(request):
    return HttpResponse("this is the homepage")

#.........................................................
# process the video obtained from client
def process_video(request):
    if request.method == 'POST':
        
        video_file = request.FILES['video'] # 'video' is the name of key
        
        # Create a temporary directory to store the video file
        temp_dir = tempfile.TemporaryDirectory()
        temp_file_path = os.path.join(temp_dir.name, 'video.mov')
        
        try:
            # Save the video file temporarily
            with open(temp_file_path, 'wb+') as destination:
                for chunk in video_file.chunks():
                    destination.write(chunk)
            
            # Extract frames from the video
            cap = cv2.VideoCapture(temp_file_path)
            frames = []
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                # Convert frame to RGB (assuming BGR format)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame_rgb)
                
            cap.release()
            if len(frames):
                message1='frames extracted successfully'

            # remove similar frames
            non_similar_frames = remove_similar_frames(frames)
            message2='removed similar frames'
            frames[:] = non_similar_frames[:]

            # remove blurred frames
                # note : function not yet defined ....
            
            # detect faces from frames
            detected_faces = detect_faces_retinaface(frames)
            if len(detected_faces):
                message3 ='detected faces successfully'
            
            # remove similar faces from detected_faces
            non_similar_faces = remove_similar_faces(detected_faces)
            detected_faces[:] = non_similar_faces[:]
            if len(detected_faces):
                message4 ='removed similar faces successfully'
            
            #recognize faces and find present students
            present = recognize_faces(detected_faces)
            if len(present):
                message5 = 'recognized faces successfully'
            return JsonResponse({'message1': message1,'message2': message2,'frames_count': len(frames),'message3' : message3,'message4' : message4 ,'detected_faces_count' : len(detected_faces), 'message5' : message5 , 'present_students' : present})

        finally:
            # Clean up: Close and delete the temporary directory
            temp_dir.cleanup()
    else:
        return JsonResponse({'error': 'Video file not found'}, status = 400)



#....................................................................
# function to remove similar frames 
    
def remove_similar_frames(frames):
    non_similar_frames = []
    non_similar_frames.append(frames[0])
    orb = cv2.ORB_create()
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # frame_count=0
    # output_folder="C:\\Users\\wigar\\Desktop\\Django_project\\frames"
    # os.makedirs(output_folder, exist_ok=True)

    for i in range(1, len(frames)):
        keypoints1, descriptors1 = orb.detectAndCompute(non_similar_frames[-1], None)
        keypoints2, descriptors2 = orb.detectAndCompute(frames[i], None)
        matches = bf.match(descriptors1, descriptors2)
        if len(matches) < 200:
            non_similar_frames.append(frames[i])
            # output_file_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
            # frame_count+=1
            # # Save the frame as an image file
            # cv2.imwrite(output_file_path,frames[i])
            #.............................................................................................
            # note : the commented code inside this function is to store the frames in a folder if required
    return non_similar_frames  



#.................................................................
# function to detect faces using mediapipe

def detect_faces(frames):
    detected_faces = []
    mp_face_detection = mp.solutions.face_detection
    # Initialize MediaPipe face detection module
    face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)
    
    for frame in frames:
        # Convert frame to RGB (MediaPipe requires RGB input)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect faces in the current frame
        results = face_detection.process(frame_rgb)
        print(type(results.detections))
        if results.detections:
            
            for detection in results.detections:
                # Get bounding box coordinates
                box = detection.location_data.relative_bounding_box
                x_start, y_start = int(box.xmin * frames[0].shape[1]), int(box.ymin * frames[0].shape[0])
                x_end, y_end = int((box.xmin + box.width) * frames[0].shape[1]), int((box.ymin + box.height) * frames[0].shape[0])

                if x_start < 0 or y_start < 0:
                    continue

                face = frame[y_start:y_end, x_start:x_end]
                face = cv2.cvtColor(face,cv2.COLOR_BGR2RGB)
                detected_faces.append(face)
    
    # Release resources used by MediaPipe
    face_detection.close()
    #.........................................
    # note : store detected faces in folder
   
    # for i, face in enumerate(detected_faces):
    #     # Generate a unique filename for the face image
    #     filename = f"face_{i}_{uuid.uuid4()}.jpg"
        
    #     # Save the face image to the output folder
    #     output_path = os.path.join("C:\\Users\\wigar\\Desktop\\Django_project\\faces", filename)
    #     cv2.imwrite(output_path, face)
    #.............................................................................................    
    return detected_faces
 



# function to detect faces using retinaface
#..................................................
def detect_faces_retinaface(frames):
    detected_faces = []

    for frame in frames:
        obj = rf.detect_faces(frame)
        if isinstance(obj, dict):
            for key in obj.keys():
                faceid = obj[key]
                area = faceid['facial_area']
                x1,y1,x2,y2=area
                extracted_face=frame[y1:y2,x1:x2]
                extracted_face=cv2.cvtColor(extracted_face,cv2.COLOR_BGR2RGB)
                detected_faces.append(extracted_face)
    return detected_faces



# function to remove similar faces from detected faces
#...........................................................

def remove_similar_faces(detected_faces):
    non_similar_faces = []
    non_similar_faces.append(cv2.convertScaleAbs(detected_faces[0]))
    orb = cv2.ORB_create()
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    for i in range(1, len(detected_faces)):
        img = cv2.convertScaleAbs(detected_faces[i])
        keypoints1, descriptors1 = orb.detectAndCompute(non_similar_faces[-1], None)
        keypoints2, descriptors2 = orb.detectAndCompute(img, None)

        if descriptors2 is None:
            continue
        matches = bf.match(descriptors1, descriptors2)
        if len(matches) < 200:
            non_similar_faces.append(detected_faces[i])
    return non_similar_faces


#.............................................................................................................

# function to recognize faces

def recognize_faces(detected_faces):
    # Specify the condition for fetching documents
    condition = {"class": "2k20"}

    # Retrieve the document from MongoDB based on the condition
    document = classes_collection.find_one(condition)

    if document:
        # Retrieve the binary data from the MongoDB document
        binary_data_from_mongo = document['pkl']

        # Create a temporary folder
        temp_folder = tempfile.mkdtemp()

        # Path to the Pickle file inside the temporary folder
        pickle_file_path = f"{temp_folder}/representations_facenet.pkl"

        # Save the binary data to the temporary folder
        with open(pickle_file_path, 'wb') as file:
            file.write(binary_data_from_mongo)
        

        # Load the Pickle file from mongodb
        with open(pickle_file_path, 'rb') as file:
            loaded_data = pickle.load(file)

        # Perform some processing with the loaded data-face recognition
        models = []
        res = []
        present = []
        for i in range(len(detected_faces)):
            model = df.find(img_path=detected_faces[i],db_path=temp_folder,model_name='Facenet',distance_metric='euclidean',enforce_detection=False,normalization='Facenet',detector_backend='mediapipe')
            models.append(model)
        print()
        count = 0
        for model in models:
            if len(model) > 0 and len(model[0]) > 0:
                name = model[0]['identity'].values[0].split('\\')[-1].split('/')[-1].split('.')[-2]
                print(count , "_ ", name)
                if name not in present:
                    present.append(name)
            else:
                print('Unknown Face detected')
            count += 1
        print(present)
        # Clean up: Delete the temporary folder and its contents
        shutil.rmtree(temp_folder)
    else:
        print("No document found with class attribute '2k20' in MongoDB.")
    return present


