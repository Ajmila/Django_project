clone the repository (last added branch..checkout the branch with latest date)
cd django_project
cd Backend
python -m pip install virtualenv
python -m virtualenv venv
venv/scripts/activate
python -m pip install django
pip install djangorestframework
pip install opencv-python
pip install tensorflow==2.14.0
pip install deepface==0.0.79
pip install retina-face
pip install mediapipe
pip install pymongo
pip install django-cors-headers


# to run the server:
cd Backend
venv/scripts/activate
python manage.py runserver
(server runs in localhost:8000)

# to run client:
install node from website
cd Frontend1
npm install -g npm (not sure if this is necessary if you are cloning my code..:)...skip this step and try)
npm start
(client will run in localhost:3000)
