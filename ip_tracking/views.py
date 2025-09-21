from django.shortcuts import render
from django.http import JsonResponse
from django_ip_geolocation.decorators import with_ip_geolocation
from rest_framework.views import APIView, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics, filters
from django.contrib.auth import get_user_model, logout
from .serializers import RegisterSerializer, LoginSerializer,  LogoutSerializer
from django.contrib.auth import authenticate
from .models import RequestLog
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.authentication import SessionAuthentication
from rest_framework.validators import ValidationError
from django.contrib.auth.models import User
from django_ratelimit.decorators import ratelimit
# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    if request.method == "POST":
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # Get the data from serializer
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            email = serializer.validated_data.get('email')
            # Create the user
            user = User.objects.create(username=username,first_name=first_name,
                                        last_name=last_name, email=email)
            user.set_password(password)
            user.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ratelimit(key='user', rate='5/m', block=True)
@ratelimit(key='ip', rate='10/m', block=True)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            # Validate the login credentials
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # check if user is active
                if not user.is_active:
                    raise AuthenticationFailed("User is not active")
                
                # Create a jwt token manually here for both refresh and access tokens
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token

                # Add custom data to the access token
                access_token['id'] = str(user.id) 
                access_token['username'] = user.username
               

                return Response({"token":{
                    "access_token": str(access_token),
                    "refresh_token":str(refresh),
                },"message":"login successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"message":"Invalid Credentials!!! user "}, status=status.HTTP_401_UNAUTHORIZED)