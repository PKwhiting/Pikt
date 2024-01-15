from django.urls import path
from . import views  # Import views from the current directory

urlpatterns = [
    path('', views.rootView.as_view()),
    path('parts/', views.defaultDashboardView.as_view()),
    path('add-part/', views.add_part),
    path('delete_message/', views.delete_message.as_view(), name='delete_message'),
    # Each line here represents a route
    # path('route', views.view_name, name='route_name'),

    # Example:
    # path('', views.home, name='home'),
]