from rest_framework import serializers
from django.contrib.auth import get_user_model
from competition.models import Competition
from competition.serializers import UserCompInlineSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    compCreated = UserCompInlineSerializer(many=True, read_only=True, source='competitions')

    class Meta:
        model = User
        fields = ['id', 'fullName', 'email', 'college',
                  'about', 'createdAt', 'updatedAt', 'compCreated']


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'fullName', 'email', 'college',
                  'about', 'createdAt', 'updatedAt', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True},
        }

    def validate(self, attrs):
        # check if email already exists
        email = attrs['email'].lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "Email already exists."})
        
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        # normalize email with django builtin function
        validated_data['email'] = validated_data['email'].lower()
        user = User.objects.create(
            email=validated_data['email'],
            fullName=validated_data['fullName'],
            college=validated_data['college'],
            about=validated_data['about'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
    

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100, required=True)
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }