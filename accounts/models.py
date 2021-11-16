import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class AccountManager(BaseUserManager):
    
    def create_user(self, username, email, password=None):
        
        if not username:
            raise ValueError('Please provide a username')
        
        if not email:
            raise ValueError('Please provide an email address')
        
        user = self.model(
            username = username,
            email=self.normalize_email(email)
        )
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user
        
    def create_superuser(self, username, email, password):
        
        user = self.create_user(
            username=username,
            email=email,
            password=password
        )
        
        user.is_staff = True
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        
        return user


class Account(AbstractBaseUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]
    
    onjects = AccountManager()
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
    
    def __str__(self):
        return self.username
    