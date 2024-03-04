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
pip install pymongo
npm install -g npm (shoud install node from its website before this)

#to run the server
python manage.py runserver

mar_5:
created new file api/utils.py and api/serializers.py
FRBAS/settings.py changed (added variables required for sending email, modified the REST_FRAMEWORK variable also...check for other changes as well:) )
api/views.py changed
api/urls.py changed
note:function remove_small_faces needs to be modified..