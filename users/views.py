from django.db.models import Count
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from restaurant.models import Menu
from restaurant.serializers import MenuSerializer
from users.models import Vote
from users.serializers import VoteSerializer
from django.utils import timezone

# Create your views here.
class VoteListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VoteSerializer
    def get(self, request,pk=None):
        today = timezone.now().date()
        if not pk:
            votes = Vote.objects.filter(date__date=today)
            return Response(VoteSerializer(votes,many=True).data)
        else:
            votes = Vote.objects.filter(user=pk,date__date=today)
        return Response(VoteSerializer(votes,many=True).data)
    def post(self,request):
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=400)
        return Response(serializer.data)
class ResultListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        today = timezone.now().date()
        votes_today = (
            Vote.objects
            .filter(date__date=today)
            .values('menu')
            .annotate(total_votes=Count('id'))
            .order_by('-total_votes')
        )
        results = []
        for entry in votes_today:
            menu = Menu.objects.get(id=entry['menu'])
            menu_data = MenuSerializer(menu).data
            menu_data['votes'] = entry['total_votes']
            results.append(menu_data)

        return Response(results)