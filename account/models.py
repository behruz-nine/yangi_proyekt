from django.db import models
from django.contrib.auth.models import AbstractUser
from base.models import BaseModel
from PROJECT.settings import EMAIL_TIME, PHONE_TIME
from datetime import datetime, timedelta
import uuid
from rest_framework_simplejwt.tokens import RefreshToken
import random

# Create your models here.

NEW, CODE_VERIFY, DONE, PHOTO_DONE = ('new', 'code_verify', 'done', 'photo_done')
VIA_PHONE, VIA_EMAIL = ('via_phone', 'via_email')
SELLER, COSTUMER = ('seller', 'costumer')

class CustomUser(AbstractUser, BaseModel):
    
    AUTH_STATUS =(
        (NEW, NEW),
        (CODE_VERIFY, CODE_VERIFY),
        (DONE, DONE),
        (PHOTO_DONE, PHOTO_DONE)
    )

    AUTH_TYPE =(
        (VIA_PHONE, VIA_PHONE),
        (VIA_EMAIL, VIA_EMAIL)
    )

    AUTH_ROLE =(
        (SELLER, SELLER),
        (COSTUMER, COSTUMER)
    )

    phone_number = models.CharField(max_length=13, unique=True, blank = True, null= True)
    email = models.EmailField(max_length=20, unique=True, blank = True, null= True)
    auth_status = models.CharField(max_length=20, choices=AUTH_STATUS, default=NEW)
    auth_typ = models.CharField(max_length=20, choices=AUTH_TYPE)
    auth_role = models.CharField(max_length=20, choices=AUTH_ROLE)
    image = models.ImageField(upload_to='users/', blank=True, null=True)
    adress = models.CharField(max_length=250, blank=True, null=True)


    def __str__(self):
        return self.username
    
    
    def change_username(self):
        if self.username is None:
            u = str(uuid.uuid4)
            username2 = u[u.rfind('-'):]
            self.username = username2

    def change_password(self):
        if self.password is None:
            u = str(uuid.uuid4)
            password2 = u[u.rfind('-'):]
            self.password = password2

    def heshing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)


    def email_normalize(self):
        email2 = self.email.lower()
        self.email = email2


    def generate_code(self, verify_type):
        code = random.randint(1000, 9999)
        Verify.objects.create(
            verify_type = verify_type,
            code = code,
            user = self
        )
        return code
    
 
    
    def token(self):
        refresh_token = RefreshToken.for_user(self)

        return {
            'refresh_token': str(refresh_token),
            'access_token': str(refresh_token.access_token)
        }
    
    def save(self, *args, **kwargs):
        self.change_username
        self.change_password
        self.heshing_password
        self.email_normalize
        return super().save(*args, **kwargs)





class Verify(BaseModel):
    VERIFY_TYPE = (
        (VIA_PHONE, VIA_PHONE),
        (VIA_EMAIL, VIA_EMAIL)
    )

    verify_type =models.CharField(max_length=20, choices=VERIFY_TYPE)
    used = models.BooleanField(default=False)
    code = models.CharField(max_length=4)
    expired_time = models.DateTimeField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}---{self.code}"
    
    def save(self, *args, **kwargs):
        if self.verify_type == VIA_EMAIL:
            self.expired_time = datetime.now() + timedelta(minutes=EMAIL_TIME)
        else:
            self.expired_time = datetime.now() + timedelta(minutes=PHONE_TIME)
        return super().save(*args, **kwargs)