from django.urls import reverse
from django.contrib.auth.models import User
import pytest
from routes.models import Category, Route, Review

# Use transactional db since we're creating instances
pytestmark = pytest.mark.django_db

def test_home_page(client):
    url = reverse('routes:home')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Discover trails' in response.content.decode('utf-8')

def test_routes_list_page(client):
    url = reverse('routes:list')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Hiking Routes' in response.content.decode('utf-8')

def test_login_page_renders(client):
    url = reverse('accounts:login')
    response = client.get(url)
    assert response.status_code == 200
    assert 'Please log in' in response.content.decode('utf-8') or 'Login' in response.content.decode('utf-8')

def test_create_category_and_route():
    # Test model creation and logic
    user = User.objects.create_user(username='testuser', password='password123')
    category = Category.objects.create(name='Test Category', slug='test-cat', icon='🌲')
    route = Route.objects.create(
        title='Test Route',
        description='Test description for a route.',
        difficulty='easy',
        distance_km=5.0,
        elevation_gain=200,
        estimated_duration='2 hours',
        location='Tashkent',
        created_by=user
    )
    route.categories.add(category)
    
    assert route.slug == 'test-route'
    assert route.categories.count() == 1
    assert route.average_rating() == 0

def test_review_creation_and_average():
    # Test review averages calculation
    user1 = User.objects.create_user(username='user1', password='password')
    user2 = User.objects.create_user(username='user2', password='password')
    route = Route.objects.create(
        title='Review Route',
        description='Test',
        difficulty='moderate',
        distance_km=10.0,
        elevation_gain=500,
        estimated_duration='4 hours',
        location='Uzbekistan',
        created_by=user1
    )
    Review.objects.create(route=route, user=user1, rating=4, comment='Good')
    Review.objects.create(route=route, user=user2, rating=5, comment='Great')
    
    assert round(route.average_rating(), 1) == 4.5
    assert route.reviews.count() == 2

def test_user_profile_creation_signal():
    # Test that signal automatically creates a UserProfile
    user = User.objects.create_user(username='signaluser', password='password')
    # Because of auto-creation we can re-query the db to ensure userprofile exists
    from accounts.models import UserProfile
    profile_exists = UserProfile.objects.filter(user=user).exists()
    assert profile_exists

