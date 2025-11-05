from django.db import models



# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
class Menu(models.Model):
    menu_date=models.DateField(auto_now_add=True)
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE)

class MenuItem(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    price=models.IntegerField()
    category=models.CharField(max_length=100)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items',blank=True, null=True)