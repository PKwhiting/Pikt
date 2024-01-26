from django.urls import path
from . import views  # Import views from the current directory

urlpatterns = [
    path('', views.rootView.as_view(), name='dashboard'),
    path('parts/', views.defaultDashboardView.as_view()),
    path('add-part/', views.add_part),
    path('delete_message/', views.delete_message.as_view(), name='delete_message'),
    path('single_part/<int:part_id>/', views.single_part.as_view(), name='single_part'),
    path('delete_part/<int:part_id>/', views.delete_part, name='delete_part'),
    path('ebay_consent/', views.ebayConsent.as_view(), name='ebay_consent'),
    path('ebay_consent/redirect/', views.RedirectView.as_view(), name='redirect'),
    path('orders/', views.orders.as_view(), name='orders'),
]