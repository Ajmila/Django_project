from django.shortcuts import render
from django.http import HttpResponse
import os
import cv2
import numpy as np
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
            
            # Further processing of frames (optional)
            
            return JsonResponse({'frames_count': len(frames), 'message': 'Frames extracted successfully'})
        finally:
            # Clean up: Close and delete the temporary directory
            temp_dir.cleanup()
    else:
        return JsonResponse({'error': 'Video file not found'}, status=400)

