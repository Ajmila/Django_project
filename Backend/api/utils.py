from .models import *
from django.core.mail import send_mail,EmailMessage
from retinaface import RetinaFace as rf
from deepface import DeepFace as df
from bson.binary import Binary
from datetime import datetime
from io import StringIO
import mediapipe as mp
import tempfile
import cv2
import pickle
import shutil
import os
import csv
# import uuid

#................................................................................................
# function to remove similar frames 
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

#....................................................................................................
# functions to remove blurred frames
def calculate_blurriness(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def remove_blurred_frames(frames, threshold=60):
    sharp_frames = []
    count=0
    for i, frame in enumerate(frames):
        sharpness = calculate_blurriness(frame)
        print("frame",count," ",sharpness)
        count+=1
        if sharpness > threshold:
            sharp_frames.append(frame)
            
    return sharp_frames

#......................................................................................................
# functions to detect faces using mediapipe and retinaface

def detect_faces_mediapipe(frames):
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
    output_folder = 'C:\\Users\\wigar\\Desktop\\Django_project\\faces'
    
    for i, face in enumerate(detected_faces):
        face = cv2.cvtColor(face,cv2.COLOR_BGR2RGB)
        cv2.imwrite(os.path.join(output_folder, f'face_{i}.jpg'), face)

    return detected_faces


#.......................................................................................................
# functions to process detected faces

# function to remove small faces from detected faces
     # note:need to find appropriate threshold
def remove_small_faces(detected_faces,frames):
    large_faces = []
    frame_area = frames[0].shape[0] * frames[0].shape[1]

    # Set the threshold as a percentage of the frame area
    threshold_percentage = 0.001 # Adjust this percentage according to your requirements
    min_area_threshold = int(threshold_percentage * frame_area)

    for face in detected_faces:
        # Calculate the area of the face
        area = face.shape[0] * face.shape[1]

        # Check if the area is greater than the minimum threshold
        if area >= min_area_threshold:
            large_faces.append(face)

# function to remove similar faces from detected faces
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

# functions to remove blurred faces from detected faces(note:threshold needs to be adjusted)
def calculate_blurriness(face):
    gray = cv2.cvtColor(face, cv2.COLOR_RGB2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def remove_blurred_faces(detected_faces, threshold=40):
    sharp_faces = []
    count=0
    for i, face in enumerate(detected_faces):
        sharpness = calculate_blurriness(face)
        print("face",count," ",sharpness)#printing sharpness of each face
        count+=1
        if sharpness > threshold:
            sharp_faces.append(face)
    output_folder = 'C:\\Users\\wigar\\Desktop\\Django_project\\sharpfaces'
    
    for i, face in enumerate(sharp_faces):
        face = cv2.cvtColor(face,cv2.COLOR_BGR2RGB)
        cv2.imwrite(os.path.join(output_folder, f'face_{i}.jpg'), face)        
    return sharp_faces

#.............................................................................................................

# functions to recognize faces(note:need modification)

def recognize_faces(detected_faces,class_name):
    # Specify the condition for fetching documents
    condition = {"Class": class_name}

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
        present = []
        for i in range(len(detected_faces)):
            model = df.find(img_path=detected_faces[i],db_path=temp_folder,model_name='Facenet',distance_metric='euclidean',enforce_detection=False,normalization='Facenet',detector_backend='mediapipe')
            models.append(model)
        print()
        #count = 0
        for model in models:
            if len(model) > 0 and len(model[0]) > 0:
                name = model[0]['identity'].values[0].split('\\')[-1].split('/')[-1].split('.')[-2]
                #print(count , "_ ", name)
                if name not in present:
                    present.append(name)
            else:
                #print('Unknown Face detected')
                pass
            #count += 1
        
        # Clean up: Delete the temporary folder and its contents
        shutil.rmtree(temp_folder)
    else:
        print("No document found with class attribute ",class_name," in MongoDB.")
    return present

def get_absent_students(present):
    # Query MongoDB for students not present
    absent_students = list(student_collection.find({'Name': {'$nin': present}}))
    
    return absent_students

def generate_csv(document):
    csv_data = [[ 'Date', 'Time', 'Present Students', 'Absent Students'],
                [document['date'], document['time'], ','.join(document.get('present', [])), ','.join(document.get('absent', []))]]
    # Convert CSV data to string
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerows(csv_data)
    csv_buffer.seek(0)
    csv_string = csv_buffer.getvalue()

    # Save CSV data to a temporary file on the server
        #write code if needed...
    return csv_string

def send_mail_to_absent_students(absent_students):
    
    absent_students = [{'email':'ajmilashada@gmail.com','name':'Ajmila_Shada'}]
    for student_data in absent_students:
        email = student_data['email']  # Assuming 'email' is the field in the data that stores email addresses
        name = student_data['name']  # Assuming 'name' is the field in the data that stores student names

        # Send email to the absent student
        subject = 'Attendance Notification'
        message = f'Dear {name},\nYou were marked as absent in today\'s class. Please ensure your attendance in the upcoming classes.'
        from_email = 'ajmilashada@gmail.com'  # Replace with your email address
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

def send_csv_email(email, csv_data):
    subject = 'CSV File Attachment'
    message = 'Please find the attached CSV file.'

    # Create a CSV attachment
    attachment_filename = 'attendance.csv'
    
    # Create an EmailMessage object
    email_message = EmailMessage(subject, message, to=[email])

    # Attach the CSV file
    email_message.attach(attachment_filename, csv_data, 'text/csv')

    # Send the email
    email_message.send()