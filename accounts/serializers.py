
from django.contrib.auth.models import User 
from rest_framework import serializers 
from rest_framework_simplejwt.tokens import RefreshToken 

class UserRegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        field = ('id', 'username', 'email')

class MyTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        from django.contrib.auth import authenticate 
        user = authenticate(
            username=attrs['username'],
            password=attrs['password']
        )

        if not user or not user.is_active:
            raise serializers.ValidationError("Invalid credentials.")

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

