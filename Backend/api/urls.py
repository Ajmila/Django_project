from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register('login', UserLoginViewSet, basename = 'login')
router.register('password_reset', PasswordChangeViewSet, basename = 'password_reset')
router.register('process_video', VideoProcessingViewSet, basename = 'process_video')


urlpatterns = router.urls