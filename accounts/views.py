import json

from django.core.exceptions import ValidationError
from django.contrib import auth

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
from rest_framework import permissions, serializers, status

from utils.carts import get_cart_id
from .models import Account
from .serializers import(
    PasswordResetCompleteSerializer, 
    PasswordResetSerializer, 
    UserRegisterSerializer,
    PasswordChangeSerializer
    )
from carts.models import Cartitem, ItemVariation
from store.models import Product
from . import signals

class UserLogin(ObtainAuthToken):
    permission_class = [permissions.AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        cart = None
        if serializer.is_valid(raise_exception=True):
            user  = serializer.validated_data.get('user')
            
            cart_items = json.loads(request.data.get('cartItems'))
            
            if cart_items:
                for item in cart_items:
                    product = Product.objects.get(id=item.get('product')['id'])
                    color = item['variation']['color']
                    size = item['variation']['size']
                    brand = item['variation']['brand']
                    quantity = item['quantity']
                    variation_id = f'{product.id}{color}{size}{brand}'

                    existing_item = Cartitem.objects.filter(
                        product=product, variation__variation_id=variation_id, user=user).exists()

                    if existing_item:
                        cart_item = Cartitem.objects.get(
                            product=product, variation__variation_id=variation_id, user=user)
                        cart_item.quantity += quantity
                        cart_item.save()
                    else:
                        variarion = ItemVariation.objects.create(
                            variation_id=variation_id,
                            color=color,
                            size=size,
                            brand=brand
                        )

                        # variarion.save()
                        cart_item = Cartitem()
                        cart_item.user = user
                        cart_item.product = product
                        cart_item.variation = variarion
                        cart_item.quantity = quantity
                        cart_item.save()
                        
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
        
        if not request.user.is_anonymous:
            user = request.user
            
            token = Token.objects.get(user=user)
            
            token.delete()
                        
            return Response({'success': True})
        else:
            return Response({'success': False}, status=status.HTTP_403_FORBIDDEN)
            


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
            site_domain = request.META.get('HTTP_ORIGIN')
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
        except (Account.DoesNotExist, ValidationError, UnicodeEncodeError):
            user = None
        
        
        if user is not None and default_token_generator.check_token(user, token):
            data["done"] = True
            status_res = status.HTTP_200_OK
            data["user_id"] = uid
            request.session['user_id'] = uid
        else:
            status_res = status.HTTP_404_NOT_FOUND
            data = {'invalid_link': 'The link is not valid!'}
        
        return Response(data, status=status_res)
        

class PasswordResetComplete(APIView):

    def post(self, request):
        data = {}
        res_status = status.HTTP_200_OK
        try:
            user_id = request.session.get('user_id') or request.data.get("user_id") # the last is from react frontend: refere to the note at the bottom
            
            user = Account.objects.get(pk=user_id)
        except (Account.DoesNotExist, ValidationError, TypeError):
            user = None
        serializer = PasswordResetCompleteSerializer(data=request.data, context={'request': request})
        
        if user is not None:
            if serializer.is_valid(raise_exception=True):
                password = serializer.validated_data.get('password')
                user.set_password(password)
                user.save()
                try:  # check if user id was saved in session storage
                    del request.session['user_id']
                    request.session.modified = True
                except KeyError:
                    pass
                data = {'done': True}
            else:
                data = serializer.errors
                res_status = status.HTTP_400_BAD_REQUEST
        else:
            data = data = {'invalid_link': 'The link is not valid!'}
            res_status = status.HTTP_400_BAD_REQUEST
        return Response(data, status=res_status)


class PasswordChange(APIView):
    permission_class = [permissions.IsAuthenticated,]
    
    def put(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid(raise_exception=True):
            user = request.user
            if not user.is_authenticated:
                raise serializers.ValidationError(
                    {'not_authenticated': 'Please login to perform password change!'})
            
            old_password = serializer.validated_data.get("password")
            new_password = serializer.validated_data.get("new_password")
            
            if not user.check_password(old_password):
                raise serializers.ValidationError({'current_password': 'Your current password is not correct!'})
            else:
                user.set_password(new_password)
                user.save()
                return Response({'done': True, 'msg': 'Password changed successfully!'})
        else:
            return Response(serializer.errors)


        """[summary]
        Note:
            line-155. Request from react frontend can't save and access from session storage, 
                so i added extra data on serializer field named user_id from react frontend which can be used
                to identify the request id for the password reset
        """
