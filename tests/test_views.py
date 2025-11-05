import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from restaurant.models import Restaurant, Menu, MenuItem
from users.models import Vote
from django.utils import timezone

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_client(api_client):
    user = User.objects.create_user(username='testuser', password='password123')
    api_client.force_authenticate(user=user)
    return api_client
@pytest.mark.django_db
def test_create_restaurant(auth_client):
    payload = {"name": "Test Restaurant","address":"Kharkiv","description":"desctription"}
    response = auth_client.post("/restaurant/", payload, format="json")

    assert response.status_code == 200 or response.status_code == 201
    assert response.data["name"] == "Test Restaurant"
@pytest.mark.django_db
def test_create_menu_with_items(auth_client):
    restaurant = Restaurant.objects.create(name="Demo Place")

    payload = {
        "menu_date": str(timezone.now().date()),
        "restaurant": restaurant.id,
        "categories": [
            {
                "name": "Italian",
                "items": [
                    {"name": "Pizza", "price": 12000, "description": "Cheese pizza", "category": "Italian"},
                    {"name": "Pasta", "price": 8000, "description": "Tomato pasta", "category": "Italian"},
                ],
            }
        ],
    }

    response = auth_client.post("/menus/", payload, format="json")

    assert response.status_code == 200
    assert response.data["restaurant"] == restaurant.id
    assert "categories" in response.data
@pytest.mark.django_db
def test_get_todays_menu(auth_client):
    restaurant = Restaurant.objects.create(name="Demo Place")
    menu = Menu.objects.create(restaurant=restaurant, menu_date=timezone.now().date())
    response = auth_client.get("/menus/", format="json")
    print(response.status_code, response.data)
    assert response.status_code == 200
    data = response.data
    if isinstance(data, dict):
        data = [data]
    assert isinstance(data, list)
    assert response.data["restaurant"] == restaurant.id
@pytest.mark.django_db
def test_vote_and_get_results(auth_client):
    user = User.objects.create_user(username="bob", password="1234")
    restaurant = Restaurant.objects.create(name="Vote Café")
    menu = Menu.objects.create(restaurant=restaurant, menu_date=timezone.now().date())

    # User votes for menu
    vote_payload = {"user": user.id, "menu": menu.id}
    vote_response = auth_client.post("/vote/", vote_payload, format="json")

    assert vote_response.status_code == 200

    # Get results
    result_response = auth_client.get("/result/")
    assert result_response.status_code == 200
    assert len(result_response.data) >= 1
    assert "votes" in result_response.data[0]


