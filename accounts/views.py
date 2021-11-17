from django.shortcuts import render

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

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
    permission_class = [IsAuthenticated,]
    
    def post(self, request):
        user = request.user
        
        token = Token.objects.get(user=user)
        
        token.delete()
        
        return Response({'success': 'you have been logged out!'})
