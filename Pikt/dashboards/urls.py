from django.urls import path
from . import views  # Import views from the current directory

urlpatterns = [
    path('', views.rootView.as_view(), name='dashboard'),
    path('success/', views.rootView.as_view(), name='funnel_success'),
    path('parts/', views.defaultDashboardView.as_view(), name='parts'),
    path('vehicles/', views.vehiclesView.as_view(), name='vehicles'),
    path('add-part/', views.add_part),
    path('add-vehicle/', views.add_vehicle, name='add_vehicle'),
    path('delete_message/', views.delete_message.as_view(), name='delete_message'),
    path('single_part/<int:part_id>/', views.single_part.as_view(), name='single_part'),
    path('single_vehicle/<int:vehicle_id>/', views.single_vehicle.as_view(), name='single_vehicle'),
    path('delete_part/<int:part_id>/', views.delete_part, name='delete_part'),
    path('delete_vehicle/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),
    path('edit_part/<int:part_id>/', views.edit_part, name='edit_part'),
    path('edit_vehicle/<int:vehicle_id>/', views.edit_vehicle, name='edit_vehicle'),
    path('ebay_consent/', views.ebayConsent.as_view(), name='ebay_consent'),
    path('ebay_consent/redirect/', views.RedirectView.as_view(), name='redirect'),
    path('orders/', views.orders.as_view(), name='orders'),
    path('yard/', views.yard.as_view(), name='yard'),
    path('cores/', views.cores.as_view(), name='cores'),
    path('upload_inventory', views.uploadInventoryView.as_view(), name='upload_inventory'),
]