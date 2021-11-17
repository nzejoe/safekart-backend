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