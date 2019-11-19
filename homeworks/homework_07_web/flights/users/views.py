from django.contrib.auth.hashers import make_password

from rest_framework import views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework_jwt.settings import api_settings

from .models import User
from .serializers import UserSerializer


class CreateUserAPIView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ObtainTokenAPIView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if (user and user.check_password(password)):
                try:
                    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                    payload = jwt_payload_handler(user)
                    token = jwt_encode_handler(payload)
                    user_details = {}
                    user_details['username'] = user.username
                    user_details['token'] = token
                    return Response(user_details, status=status.HTTP_200_OK)

                except Exception as e:
                    raise e
            else:
                res = {
                    'error': 'can not authenticate with the given credentials or the account has been deactivated'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            res = {'error': 'please provide a email and a password'}
            return Response(res)
