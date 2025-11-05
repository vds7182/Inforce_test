from django.contrib.admin import action
from django.utils import timezone
from django.shortcuts import render
from rest_framework import generics,viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from restaurant.models import Restaurant,Menu,MenuItem
from restaurant.serializers import MenuSerializer, MenuItemSerializer, RestaurantSerializer


# Create your views here.

class Menulist(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    def get(self, request,pk=None):
        today = timezone.now().date()
        if pk is None:
            menus = Menu.objects.filter(menu_date=today)
            if menus.count() > 1:
                serializer = MenuSerializer(menus, many=True)
            else:
                menus=Menu.objects.get(menu_date=today)
                serializer = MenuSerializer(menus)
        else:
            menus = Menu.objects.get(pk=pk)
            serializer = MenuSerializer(menus)
        return Response(serializer.data)
    def post(self, request):
        serializer = MenuSerializer(data=request.data)
        categories = request.data.pop('categories', [])
        if serializer.is_valid():
            menu=serializer.save()
        else:
            return Response(serializer.errors)
        for category in categories:
            items = category['items']
            for item in items:
                item['menu'] = menu.id
                item_serializer = MenuItemSerializer(data=item)
                if item_serializer.is_valid():
                    item_serializer.save()
                else:
                    return Response(item_serializer.errors, status=400)
        menus = Menu.objects.get(pk=menu.pk)
        serializer = MenuSerializer(menus)
        return Response(serializer.data)
class RestaurantListAPI(APIView):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request,pk=None):
        if pk is None:
            restaurants = Restaurant.objects.all()
            serializer = RestaurantSerializer(restaurants, many=True)
        else:
            restaurants = Restaurant.objects.get(id=pk)
            serializer = RestaurantSerializer(restaurants)
        return Response(serializer.data)
    def post(self, request):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)