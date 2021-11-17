from django.shortcuts import render

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from .models import Account
from .serializers import UserRegisterSerializer
from . import signals

class UserLogin(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data, context={'request': request})
        
        if serializer.is_valid(raise_exception=True):
            user  = serializer.validated_data.get('user')
            
            token, created = Token.objects.get_or_create(user=user)
            
            data = {
                'username': user.username,
                'email': user.email,
                'token': token.key,
            }

        return Response(data)


class UserLogout(APIView):
    permission_class = [permissions.IsAuthenticated,]
    
    def post(self, request):
        user = request.user
        
        token = Token.objects.get(user=user)
        
        token.delete()
        
        return Response({'success': 'you have been logged out!'})


class UserRegister(APIView):
    # permission_class = [permissions.AllowAny, ]

    
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data, context={'request': request})
        data = {}
        
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            
            user = Account()
            user.username = username
            user.email = email
            user.is_active = True
            user.set_password(password)
            user.save()
            
            token = Token.objects.get(user=user)
            data = {
                'username': username,
                'email': email,
                'token': token.key
            }
        else:
            data = serializer.errors
            
        return Response(data)
