from django.urls import path
from . import views  # Import views from the current directory

urlpatterns = [
    path('', views.rootView.as_view(), name='dashboard'),
]