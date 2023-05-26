from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        
        fields = ["id","nome_usuario", "idade", "email", "residencia", "interes", "curriculo","bibliografia", "palavra_passe"]

        extra_kwargs = {
            "palavra_passe":{
                "write_only":True
            }
        }

    def create(self, validated_data):
        password = validated_data.pop("palavra_passe", None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        
        instance.save()

        return instance

class MultimediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Multimedia
        fields = ["curriculo", "image"]

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)

        instance.save()

        return instance