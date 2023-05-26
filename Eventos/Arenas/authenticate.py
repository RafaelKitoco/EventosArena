import jwt, datetime
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from .models import *

class JWTAUthenticat(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2:
            refresh_token = auth[1].decode("utf-8")

            id = decode_access_token(refresh_token)

            user = User.objects.get(pk=id)

            return (user, None)
        
        raise exceptions.AuthenticationFailed("Nao autenticado !")

def create_access_token(id):
    return jwt.encode({
        "user_id" : id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
    }, "access_secret", algorithm="HS256")

def decode_access_token(token):
    try:
        payloder = jwt.decode(token, "access_secret", algorithms="HS256")

        return payloder["user_id"]

    except:
        raise exceptions.AuthenticationFailed("Autentificacao falhou !")

def decode_refresh_token(token):
    try:
        payloder = jwt.decode(token, "refresh_secret", algorithms="HS256")

        return payloder["user_id"]

    except:
        raise exceptions.AuthenticationFailed("Autentificacao falhou !")

def create_refresh_token(id):
    return jwt.encode({
        "user_id" : id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }, "refresh_secret", algorithm="HS256")