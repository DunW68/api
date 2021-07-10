from django.db import models
from django.contrib.auth.models import User

# Create your models here. 


class Items(models.Model):
    
    name = models.CharField(max_length=155)
    description = models.TextField(max_length=299)
    price = models.IntegerField()
    
    def __str__(self):
        return self.name


class Cart(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(Items)

    def __str__(self):
        return f"'{self.user.username}' cart"