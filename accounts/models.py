from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,null=False,blank=False,on_delete=models.CASCADE)

    phone = models.CharField(max_length=12)


    def __str__(self):
        return self.user.username