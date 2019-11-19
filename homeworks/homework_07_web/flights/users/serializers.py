from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):

    date_joined = serializers.ReadOnlyField()

    def create(self, validated_data):
        user = User(
            email = validated_data["email"],
            username = validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta(object):
        model = User
        fields = ('id', 'email', 'username',
                  'date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}}
