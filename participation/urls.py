from django.urls import path
from . import views

urlpatterns = [
    path('', views.opportunity_list, name='opportunity_list'),
    path('opportunity/<int:pk>/', views.opportunity_detail, name='opportunity_detail'),
    path('create/', views.create_opportunity, name='create_opportunity'),
    path('create-tag/', views.create_tag, name='create_tag'),
]
