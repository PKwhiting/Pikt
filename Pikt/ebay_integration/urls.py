from django.contrib import admin
from django.urls import include, path
from ebay_integration import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [ 
    path('create_listing/<int:part_id>', views.create_ebay_listing, name='create_ebay_listing'),
]