from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, status
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView as TOPView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from django.shortcuts import get_object_or_404

from . import serializers
from .models import UserSelector

User = get_user_model()

# Create your views here.


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.RegisterSerializer

    def post(self, request, *args, **kwargs):
        user = self.create(request, *args, **kwargs)
        return Response({
            "success": True,
            "message": "User Created Successfully",
            "user": user.data,
        }, status=status.HTTP_201_CREATED)


class LoginView(TOPView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        email = request.data.get('email')
        user = User.objects.get(email=email)
        user = serializers.UserSerializer(user).data

        return Response({
            "success": True,
            "message": "Login Successful",
            "token": serializer.validated_data,
            "user": user,
        }, status=status.HTTP_200_OK)


class RetrieveUserView(generics.RetrieveAPIView):
    serializer_class = serializers.UserProfileSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):

        data = super().retrieve(request, *args, **kwargs)
        if data:
            return Response({
                "success": True,
                "user": data.data,
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "message": "User not found."
        }, status=status.HTTP_404_NOT_FOUND)


class RetrieveMyUserProfile(generics.RetrieveAPIView):
    serializer_class = serializers.UserSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def retrieve(self, request, *args, **kwargs):
        data = super().retrieve(request, *args, **kwargs)
        if data:
            return Response({
                "success": True,
                "user": data.data,
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "message": "User not found."
        }, status=status.HTTP_404_NOT_FOUND)
