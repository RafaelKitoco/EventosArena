from rest_framework.views import APIView
from rest_framework import exceptions
from .serializer import *
from rest_framework.response import Response
from .authenticate import *
import random, string
from django.core.mail import send_mail

class RegistrarAPIView(APIView):
    def post(self, request):
        dado = request.data

        if dado["palavra_passe"] != dado["palavra_passe_confirm"]:
            raise exceptions.APIException("Palavra passe diferente !")
        
        serializer = UserSerializer(data=dado)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LoginAPiview(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed("Usuario nao encontrado !")
        
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Palavra passe errado")
        

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        UserToken.objects.create(
            id_user = user.id,
            token  = refresh_token,
            expired_at  = datetime.datetime.utcnow() + datetime.timedelta(days=7)
        )

        response = Response()
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

        response.data = {
            "token" : access_token
        }

        return response

class UserAuthenticate(APIView):
    authentication_classes = [JWTAUthenticat]

    def get(self,request):
        return Response(UserSerializer(request.user).data)


class RefreshToken(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        id = decode_refresh_token(refresh_token)

        access_token = create_access_token(id)

        if not UserToken.objects.filter(
            id_user = id,
            token = refresh_token,
            expired_at__gt = datetime.datetime.now(tz=datetime.timezone.utc)
            
        ).exists():
            raise exceptions.AuthenticationFailed("Nao Authenticado !")

        response = Response()

        response.data = {
            "token": access_token
        }

        return response

class LogoutAPIView(APIView):

    def post(self, request):
        
        response = Response()
        response.delete_cookie(key="refresh_token")
        response.data = {
            "message":"Logout feito com sucesso !"
        }

        return response

class ForgoutAPIView(APIView):
    def post(self, request):
        email = request.data["email"]
        token = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))

        ResetPassword.objects.create(
            email = email,
            token = token
        )
        url = "http://localhost:8000/reset" + token

        send_mail(
            subject= "Mudar a sua senha ",

            message="clica <a href='%s'>aqui<\a> para alterar a sua senha"  %url,
            
            from_email="rkitco@gmail.com",
            
            recipient_list=[email]

        )

        response = Response()

        response.data = {
            "message": "feito com sucesso !"
        }

        return response

class ResetPassword_view(APIView):
    def post(self, request):
        dados = request.data

        if dados["password"] != dados["password_confirm"]:
            raise exceptions.APIException("Palavra passe diferente !")
        
        user = ResetPassword.objects.filter(token=dados["token"]).first()

        if not user:
            raise exceptions.AuthenticationFailed("Invalid Link")
        
        new = User.objects.filter(email=user.email).first()

        if new is None:
            raise exceptions.AuthenticationFailed("Usuario Inexistente !")
        
        new.set_password(dados["password"])
        new.save()

        response = Response()

        response.data = {
            "message":"sucess !"
        }

        return response