from django.contrib.auth.models import AbstractBaseUser , BaseUserManager ,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        """
        Creates and saves a User with the given email , password and extra fields.
        """
        if not email:
            raise ValueError(_("the email must be set"))
        email = self.normalize_email(email)
        # user = self.model(email=email,**extra_fields)
        user = User(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,password,**extra_fields):
        """
        Creates and saves a superuser with the given email , password and extra fields.
        """
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_verified',True)


        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have staff=True."))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have superuser=True."))
    
        return self.create_user(email,password,**extra_fields)

class User(AbstractBaseUser,PermissionsMixin):
    '''
    Custom User Model for our app
    '''
    email = models.EmailField(max_length=255,unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=10,blank=True,null=True)

    objects = UserManager()
    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=30,null=True,unique=True)
    first_name  = models.CharField(max_length=255)
    last_name  = models.CharField(max_length=255)
    image = models.ImageField(null=True,blank=True)
    description = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

@receiver(post_save,sender=User)
def save_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
