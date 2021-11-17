import json
from django.core.exceptions import ValidationError

from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer
from .models import Account
from .serializers import PasswordResetCompleteSerializer, PasswordResetSerializer, UserRegisterSerializer
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
    permission_class = [permissions.AllowAny, ]

    
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


class PasswordReset(APIView):
    permission_class = [permissions.AllowAny, ]
    
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            user = Account.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            site_domain = get_current_site(request)
            endpoint = f'{site_domain}/accounts/password_reset_confirm/{uid}/{token}/'
            
            context = {
                'username': user.username,
                'endpoint': endpoint,
            }
            message = render_to_string('password_reset_email.html', context)
            
            mail_subject = 'Password reset'
            email_message = EmailMessage(mail_subject, message, to=[email, ])
            email_message.send()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PasswordResetConfirm(APIView):
    
    def post(self, request, uidb64, token):
        data = {}
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Account.objects.get(pk=uid)
        except (Account.DoesNotExist, ValidationError):
            user = None
        
        
        if user is not None and default_token_generator.check_token(user, token):
            data["done"] = True
            data["user_id"] = uid
            request.session['user_id'] = uid
        else:
            data = {'invalid_link': 'The link is not valid!'}
        
        return Response(data)
        

class PasswordResetComplete(APIView):
    
    def post(self, request):
        data = {}
        try:
            user_id = request.session.get('user_id')
            user = Account.objects.get(pk=user_id)
        except (Account.DoesNotExist, ValidationError):
            user = None
        serializer = PasswordResetCompleteSerializer(data=request.data, context={'request': request})
        
        if user is not None:
            if serializer.is_valid(raise_exception=True):
                password = serializer.validated_data.get('password')
                user.set_password(password)
                user.save()
                del request.session['user_id']
                request.session.modified = True
                data = {'done': True}
            else:
                data = serializer.errors
        else:
            data = data = {'invalid_link': 'The link is not valid!'}
        return Response(data)
