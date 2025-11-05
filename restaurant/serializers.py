from collections import defaultdict

from rest_framework import serializers
from restaurant.models import Restaurant,MenuItem,Menu

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['name','price','description','category','menu']
class MenuSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    class Meta:
        model = Menu
        fields = '__all__'
    def get_categories(self,obj): #"Assembling" JSON file from menu and it dishes
        items=MenuItem.objects.filter(menu=obj.id)
        grouped=defaultdict(list)
        for item in items:
            grouped[item.category].append(MenuItemSerializer(item).data)
        return [{"name": name, "items": items} for name, items in grouped.items()]
    def create(self, validated_data):
        menu = Menu.objects.create(restaurant=validated_data.pop('restaurant'),**validated_data)
        return menu
