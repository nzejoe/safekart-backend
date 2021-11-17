from os import write
from rest_framework import serializers

from .models import Account


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Account
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate(self, data):
        password = data['password']
        password2 = data['password2']
       
        if password != password2:
            raise serializers.ValidationError('The two password did not match!')
        
        return super(UserRegisterSerializer, self).validate(data)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    
    def validate_email(self, email):
        
        if not Account.objects.filter(email=email).exists():
            raise serializers.ValidationError(f'{email} is not associated with any account!')
        
        return super(PasswordResetSerializer, self).validate(email)
    
    
class PasswordResetCompleteSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    
    def validate(self, data):
        password = data['password']
        password2 = data['password2']
        
        if password != password2:
            raise serializers.ValidationError('The two password did not match')
        
        return super().validate(data)