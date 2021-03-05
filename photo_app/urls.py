from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='index'),  # home page
    path('edit/', views.Search.as_view(), name='search'),  # search page
    path('edit/<int:pk>/', views.Edit.as_view(), name='edit'),  # specific element
    path('add', views.Add.as_view(), name='add'),  # add a photo
]