from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from datetime import datetime
from .models import *
from .serializers import *
from .utils import *
import os
import cv2
import tempfile
import shutil

#from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt
# Create your views here.

def home(request):
    return HttpResponse("this is the homepage")



class PasswordChangeViewSet(ViewSet):
    serializer_class = PasswordChangeSerializer
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            
            # Authenticate user
            user = authenticate(username=username, password=old_password)
            if user:
                # Change password
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginViewSet(ViewSet):
    
    serializer_class = UserSerializer

    def create(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']
            # Authenticate the user
            user = authenticate(username = username, password = password, email = email)
        
            if user is not None:
                # User is authenticated, proceed with login process
                request.session['email'] = email
                return Response({'message': 'Login successful'}, status = status.HTTP_200_OK)
            else:
                # Authentication failed
                return Response({'error': 'Invalid credentials'}, status = status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class VideoProcessingViewSet(ViewSet):
    
    def create(self, request):
        serializer = VideoUploadSerializer(data = request.data)
        
        if serializer.is_valid():
            class_name = serializer.validated_data['class_name']
            period = serializer.validated_data['period']
            video_file = serializer.validated_data['video']
            temp_dir = tempfile.TemporaryDirectory()
            temp_file_path = os.path.join(temp_dir.name, 'video.mov')

            
            print('class_name=',class_name)
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
                    print('frames extracted successfully')

                
                # remove similar frames
                non_similar_frames = remove_similar_frames(frames)
                print('removed similar frames')
                frames[:] = non_similar_frames[:]

                # remove blurred frames
                sharp_frames = remove_blurred_frames(frames)
                if sharp_frames:
                    print('removed blurred frames')
                
                # detect faces from frames
                detected_faces = detect_faces_retinaface(sharp_frames)
                if len(detected_faces):
                    print('detected faces successfully')
                    
                # remove small faces
                    # write code..
                # remove similar faces from detected_faces
                non_similar_faces = remove_similar_faces(detected_faces)
                detected_faces[:] = non_similar_faces[:]
                if len(detected_faces):
                    print('removed similar faces successfully')
                
                # remove blurred faces
                sharp_faces = remove_blurred_faces(detected_faces)
                if sharp_faces:
                    print('removed blurred faces successfully')
                    detected_faces[:] = sharp_faces[:]

                #recognize faces and find present students
                present = recognize_faces(detected_faces,class_name)
                if len(present):
                    print('recognized faces successfully')
                    print('present:',present)

                #get absent students
                absent_students = get_absent_students(present)
               

                # Extract student names only
                absent_names = [student['Name'] for student in absent_students]
                print('absent:',absent_names)

                # mark attendance in database and generate csv file 
                date = datetime.now().strftime('%Y-%m-%d')
                time = datetime.now().strftime('%H:%M:%S')
                inserted_document = {"date": date, "time": time, "class":class_name, "period":period, "present": present, "absent": absent_names}
                attendance_collection.insert_one(inserted_document)
                csv_data = generate_csv(inserted_document)
                print('csv file generated')

                # send mail to absent students(note:do not run this function since database dont have full data)
                #send_mail_to_absent_students(absent_students) 

                # mail csv file to teacher
                email = request.session.get('email')
                send_csv_email(email,csv_data)

            finally:
                # Clean up: Close and delete the temporary directory
                temp_dir.cleanup()
                if os.path.exists(temp_dir.name):
                    shutil.rmtree(temp_dir.name)

            return Response({'message': 'Video processed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ViewClassViewSet(ViewSet):
    serializer_class = ViewClassSerializer
    def list(self, request):
        # Get the class_name from the request query parameters
        class_name = request.query_params.get('class_name')
      
        # Fetch documents from MongoDB based on class_name
        documents = student_collection.find({"Class": class_name})
        
        # Convert MongoDB documents to dictionaries
        document_dicts = [doc for doc in documents]
        
        print("Retrieved documents:", document_dicts)  # Debugging
        
        # Serialize the fetched documents
        serializer = self.serializer_class(document_dicts, many = True)
        
        print("Serialized data:", serializer.data)  # Debugging
        
        # Return the serialized data with a 200 OK response
        return Response({"data": serializer.data}, status = status.HTTP_200_OK)

