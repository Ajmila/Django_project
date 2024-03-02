from django.db import models
from db_connection import mongodb
# Create your models here.
student_collection = mongodb['stud_details']
classes_collection = mongodb['classes']
known_faces_collection = mongodb['known_faces']
attendance_collection = mongodb['attendance']

