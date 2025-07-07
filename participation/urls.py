from django.urls import path
from . import views

urlpatterns = [
    path('', views.opportunity_list, name='opportunity_list'),
    path('opportunity/<int:pk>/', views.opportunity_detail, name='opportunity_detail'),
    path('create/', views.create_opportunity, name='create_opportunity'),
    path('opportunity/<int:pk>/edit/', views.opportunity_edit, name='opportunity_edit'),
    path('opportunity/<int:pk>/delete/', views.opportunity_delete, name='opportunity_delete'),
    path('create-tag/', views.create_tag, name='create_tag'),
    path('tag/<int:pk>/edit/', views.tag_edit, name='tag_edit'),
    path('tag/<int:pk>/delete/', views.tag_delete, name='tag_delete'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('subscription_list/', views.subscription_list, name='subscription_list'),
    path('about/', views.about, name='about'),
    path('recommend/', views.recommend, name='recommend'),
]
