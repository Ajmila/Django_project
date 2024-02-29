from django.shortcuts import render
from django.http import HttpResponse
import os
import cv2
import numpy as np
import mediapipe as mp
import uuid
from deepface import DeepFace as df
import tempfile
from django.http import JsonResponse
#from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt
# Create your views here.

def home(request):
    return HttpResponse("this is the homepage")



def process_video(request):
    if request.method == 'POST':
        print(request.FILES.keys())
        video_file = request.FILES['video']
        
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
                # define function ....
            
            # detect faces from frames
            detected_faces=detect_faces(frames)
            if len(detected_faces):
                message3='detected faces successfully'
            return JsonResponse({'message1': message1,'message2': message2,'frames_count': len(frames),'message3' : message3,'detected_faces_count' : len(detected_faces)})
        finally:
            # Clean up: Close and delete the temporary directory
            temp_dir.cleanup()
    else:
        return JsonResponse({'error': 'Video file not found'}, status=400)

def remove_similar_frames(frames):
    non_similar_frames = []
    non_similar_frames.append(frames[0])
    orb = cv2.ORB_create()
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    for i in range(1, len(frames)):
        keypoints1, descriptors1 = orb.detectAndCompute(non_similar_frames[-1], None)
        keypoints2, descriptors2 = orb.detectAndCompute(frames[i], None)
        matches = bf.match(descriptors1, descriptors2)
        if len(matches) < 200:
            non_similar_frames.append(frames[i])
    return non_similar_frames  

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
    
        
    return detected_faces
 

