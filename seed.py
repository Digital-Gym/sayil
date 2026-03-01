"""Seed script to populate the database with sample data."""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sayil.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from routes.models import Category, Route, Review
from accounts.models import UserProfile


def seed():
    # Create superuser
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@sayil.uz',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        print('Created admin user (admin / admin123)')

    # Create test user
    user, created = User.objects.get_or_create(
        username='hiker',
        defaults={'email': 'hiker@sayil.uz'}
    )
    if created:
        user.set_password('hiker123')
        user.save()
        print('Created test user (hiker / hiker123)')

    # Ensure profiles
    UserProfile.objects.get_or_create(user=admin)
    UserProfile.objects.get_or_create(user=user)

    # Categories
    categories_data = [
        ('Mountain', 'mountain', '🏔️', 'High altitude trails with stunning views'),
        ('Forest', 'forest', '🌲', 'Shaded trails through woodlands'),
        ('Canyon', 'canyon', '🏜️', 'Rugged trails through canyons and gorges'),
        ('Lake', 'lake', '🏞️', 'Trails around beautiful lakes'),
        ('Desert', 'desert', '☀️', 'Arid landscape adventures'),
    ]
    cats = {}
    for name, slug, icon, desc in categories_data:
        cat, _ = Category.objects.get_or_create(
            slug=slug,
            defaults={'name': name, 'icon': icon, 'description': desc}
        )
        cats[slug] = cat
    print(f'Categories: {len(cats)}')

    # Routes
    routes_data = [
        {
            'title': 'Chimgan Peak Trail',
            'description': (
                'A classic hiking route to the summit of Greater Chimgan '
                '(3309m). The trail starts from Chimgan village and winds '
                'through alpine meadows, rocky terrain, and offers '
                'breathtaking panoramic views of the Western Tian Shan '
                'mountains. Best visited from June to September.'
            ),
            'difficulty': 'hard',
            'distance_km': 14.5,
            'elevation_gain': 1600,
            'estimated_duration': '6-8 hours',
            'location': 'Chimgan, Tashkent Region',
            'categories': ['mountain'],
        },
        {
            'title': 'Gulkam Gorge Walk',
            'description': (
                'A moderate trail through the scenic Gulkam Gorge '
                'featuring lush vegetation, a flowing river, and '
                'beautiful rock formations. Great for families and '
                'groups looking for a half-day hike.'
            ),
            'difficulty': 'moderate',
            'distance_km': 8.0,
            'elevation_gain': 400,
            'estimated_duration': '3-4 hours',
            'location': 'Bostanlyk District',
            'categories': ['canyon', 'forest'],
        },
        {
            'title': 'Charvak Lake Loop',
            'description': (
                'An easy and relaxing walk around sections of the '
                'stunning Charvak Reservoir. Enjoy views of turquoise '
                'waters surrounded by mountains. Flat terrain makes it '
                'accessible for hikers of all levels.'
            ),
            'difficulty': 'easy',
            'distance_km': 5.2,
            'elevation_gain': 120,
            'estimated_duration': '1.5-2 hours',
            'location': 'Charvak, Tashkent Region',
            'categories': ['lake'],
        },
        {
            'title': 'Beldersay Ridge Trail',
            'description': (
                'A challenging ridge hike in the Ugam-Chatkal National Park. '
                'The trail follows a mountain ridge with exposed sections '
                'offering 360-degree views. Recommended for experienced '
                'hikers only. Bring plenty of water and sun protection.'
            ),
            'difficulty': 'hard',
            'distance_km': 12.0,
            'elevation_gain': 1200,
            'estimated_duration': '5-7 hours',
            'location': 'Beldersay, Tashkent Region',
            'categories': ['mountain'],
        },
        {
            'title': 'Amirsoy Forest Path',
            'description': (
                'A gentle forest walk starting from the Amirsoy resort '
                'area. The trail passes through juniper and walnut forests, '
                'wildflower meadows, and offers peaceful spots for picnic '
                'and rest. Perfect for beginners.'
            ),
            'difficulty': 'easy',
            'distance_km': 4.0,
            'elevation_gain': 200,
            'estimated_duration': '1-2 hours',
            'location': 'Amirsoy Resort',
            'categories': ['forest'],
        },
        {
            'title': 'Pulatkhan Plateau Trek',
            'description': (
                'A multi-day trek option that can also be done as a '
                'challenging day hike. Traverse the Pulatkhan plateau at '
                '2500m altitude through rolling grasslands and rocky paths. '
                'Wildlife spotting opportunities include marmots and eagles.'
            ),
            'difficulty': 'moderate',
            'distance_km': 16.0,
            'elevation_gain': 900,
            'estimated_duration': '7-9 hours',
            'location': 'Ugam-Chatkal NP',
            'categories': ['mountain', 'desert'],
        },
    ]

    for data in routes_data:
        cat_slugs = data.pop('categories')
        route, created = Route.objects.get_or_create(
            title=data['title'],
            defaults={**data, 'created_by': admin}
        )
        if created:
            for slug in cat_slugs:
                route.categories.add(cats[slug])
            print(f'  Created route: {route.title}')

    # Sample reviews
    routes = Route.objects.all()
    reviews_data = [
        (0, user, 5, 'Absolutely incredible views from the summit! Tough but rewarding.'),
        (1, user, 4, 'Beautiful gorge, well-maintained path. A bit crowded on weekends.'),
        (2, user, 5, 'Perfect family outing. The lake is stunning in summer.'),
        (4, user, 4, 'Lovely peaceful walk. Great for unwinding after a busy week.'),
    ]
    for idx, u, rating, comment in reviews_data:
        if idx < routes.count():
            Review.objects.get_or_create(
                route=routes[idx],
                user=u,
                defaults={'rating': rating, 'comment': comment}
            )

    print('\nSeed complete!')
    print('Admin login: admin / admin123')
    print('Test user login: hiker / hiker123')


if __name__ == '__main__':
    seed()
