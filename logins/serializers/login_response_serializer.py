from rest_framework import serializers
from usuarios.serializers.usuario_serializer import UsuarioSerializer


class LoginResponseSerializer(serializers.Serializer):
    usuario = UsuarioSerializer()
    token = serializers.CharField()