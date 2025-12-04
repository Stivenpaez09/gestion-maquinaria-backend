from rest_framework import serializers

from logins.models.login import Login


class LoginDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = [
            'id_login',
            'username',
            'rol',
            'is_active',
            'usuario'
        ]
        read_only_fields = fields
