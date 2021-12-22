from django.conf.urls import url
from django.urls import path, re_path

from . import views

urlpatterns = [
    path('countries', views.countries, name='countries'),
    path('countries/<int:id>', views.countries_id, name='countries'),
    path('cities/country/<int:id_Tara>', views.cities_per_country, name='cities_per_country'),
    path('cities/<int:id>', views.cities_id, name='cities'),
    path('cities', views.cities, name='cities'),
    path('temperatures', views.temperatures, name='temperatures'),
    path('temperatures/<int:id_temp>', views.temperatures_id, name='temperatures_id'),
    path('temperatures/cities/<int:id_oras>', views.temperatures_cities, name='temperatures_cities'),
    path('temperatures/countries/<int:id_tara>', views.temperatures_countries, name='temperatures_countries'),
    path('', views.index, name='index'),

]
