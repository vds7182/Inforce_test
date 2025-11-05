from django.contrib.auth.models import User
from django.db import models
from restaurant.models import Menu
# Create your models here.
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
