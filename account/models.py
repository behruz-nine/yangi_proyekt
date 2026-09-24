from django.db import models
from django.contrib.auth.models import AbstractUser
from base.models import BaseModel

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