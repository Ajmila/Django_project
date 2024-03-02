clone the repository (last added branch..checkout the branch with latest date)
cd django_project
cd backend
python -m pip install virtualenv
python -m virtualenv venv
venv/scripts/activate
python -m pip install django
pip install djangorestframework
pip install opencv-python
pip install tensorflow
pip install deepface==0.0.79
pip install retina-face
pip install mediapipe
npm install -g npm (shoud install node from its website before this)

#to run the server
python manage.py runserver

NOTE:
changes in mar_2 branch from previous branches:

FRBAS\settings.py changed(line 82)

api\models.py changed
api\urls.py changed
api\views.py changed

db_connection.py changed

database\models.py,database\urls.py,database\views.py changed..(just comment out the everything in these files)
note: you can also choose to delete the backend\database folder completely