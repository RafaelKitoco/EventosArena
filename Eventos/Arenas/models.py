from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

def uploader_path(instance, filname):
    return "/".join(["curriculo", str(instance.email), filname])

# Create your models here.
class User(AbstractUser):
    nome_usuario = models.CharField(max_length=100)
    email = models.CharField(max_length=255, unique=True)
    idade = models.DateField()
    residencia = models.CharField(max_length=50)
    profissao = models.CharField(max_length=50)
    interes = models.CharField(max_length=50)
    bibliografia = models.CharField(max_length=255)
    curriculo = models.FileField(blank=True, null=True, upload_to=uploader_path) 
    palavra_passe = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

class Multimedia(models.Model):
    id_user = models.IntegerField()
    image = models.ImageField(blank=True, null=True, upload_to= "uploader")

class UserToken(models.Model):
    id_user = models.IntegerField()
    token = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

class ResetPassword(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255, unique=True)
