from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('bikes/', views.bikes_index, name='index'),
    path('bikes/<int:bike_id>/', views.bikes_detail, name='detail'),
    path('bikes/create/', views.BikeCreate.as_view(), name='bikes_create'),
    path('bikes/<int:pk>/update/', views.BikeUpdate.as_view(), name='bikes_update'),
    path('bikes/<int:pk>/delete/', views.BikeDelete.as_view(), name='bikes_delete'),
    path('bikes/<int:bike_id>/add_order/', views.add_order, name='add_order'),
    path('components/', views.ComponentList.as_view(), name='components_index'),
    path('components/<int:pk>/', views.ComponentDetail.as_view(), name='components_detail'),
    path('components/create/', views.ComponentCreate.as_view(), name='components_create'),
    path('components/<int:pk>/update/', views.ComponentUpdate.as_view(), name='components_update'),
    path('components/<int:pk>/delete/', views.ComponentDelete.as_view(), name='components_delete'),
    path('bikes/<int:bike_id>/assoc_component/<int:component_id>/', views.assoc_component, name='assoc_component'),
    path('bikes/<int:bike_id>/add_photo/', views.add_photo, name='add_photo'),
]