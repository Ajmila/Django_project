from django.shortcuts import render
from .models import students_collection
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse('app is running..')
def add_stud(request):
    records={
        "first_name":"ajmila",
        "last_name":"shada"
    }
    students_collection.insert_one(records)
    return HttpResponse("new student added")

def get_all_student(request):
    students=students_collection.find()
    return HttpResponse(students)