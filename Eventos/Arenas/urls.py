from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("registrar", RegistrarAPIView.as_view()),
    path("login", LoginAPiview.as_view()),
    path("user", UserAuthenticate.as_view()),
    path("refresh", RefreshToken.as_view()),
    path("logout", LogoutAPIView.as_view()),
    path("forgout", ForgoutAPIView.as_view()),
    path("reset", ResetPassword_view.as_view())
    
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)