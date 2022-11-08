from django.urls import path, include
from . import views

urlpatterns = [
        path('', views.bear_list, name='bear_list'),
        path('females', views.females, name='females'),
        path('bear/<int:id>/', views.bear_detail, name= 'bear_detail'),
        path('bear_new/', views.bear_new, name='bear_new'),
        path('bear/<int:id>/edit/', views.bear_edit, name='bear_edit'),
        path('bear/<int:id>/delete/', views.bear_delete, name='bear_delete'),
        ]