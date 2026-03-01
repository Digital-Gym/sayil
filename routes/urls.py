from django.urls import path
from . import views

app_name = 'routes'

urlpatterns = [
    path('', views.home, name='home'),
    path('routes/', views.route_list, name='list'),
    path('routes/create/', views.route_create, name='create'),
    path('routes/<slug:slug>/', views.route_detail, name='detail'),
    path('routes/<slug:slug>/edit/', views.route_edit, name='edit'),
    path('routes/<slug:slug>/delete/', views.route_delete, name='delete'),
    path('routes/<slug:slug>/review/', views.add_review, name='add_review'),
    path(
        'routes/<slug:slug>/favorite/',
        views.toggle_favorite,
        name='toggle_favorite',
    ),
    path('about/', views.about, name='about'),
]
