from django.urls import path
from . import views  # Import views from the current directory
from .views import customer_list

urlpatterns = [
    path('', views.rootView.as_view(), name='dashboard'),
    path('success/', views.rootView.as_view(), name='funnel_success'),
    path('yard/', views.yardView.as_view(), name='yard'),
    path('add-part/', views.add_part),
    path('add-vehicle/', views.add_vehicle, name='add_vehicle'),
    path('delete_message/', views.delete_message.as_view(), name='delete_message'),
    path('single_part/<int:part_id>/', views.single_part.as_view(), name='single_part'),
    path('single_vehicle/', views.single_vehicle.as_view(), name='single_vehicle'),
    path('delete_part/<int:part_id>/', views.delete_part, name='delete_part'),
    path('delete_vehicle/<int:vehicle_id>/', views.delete_vehicle, name='delete_vehicle'),
    path('edit_part/<int:part_id>/', views.edit_part, name='edit_part'),
    path('edit_vehicle/', views.edit_vehicle, name='edit_vehicle'),
    path('ebay_consent/', views.ebayConsent.as_view(), name='ebay_consent'),
    path('ebay_consent/redirect/', views.RedirectView.as_view(), name='redirect'),
    path('orders/', views.orders.as_view(), name='orders'),
    path('yard/', views.yard.as_view(), name='yard'),
    path('parts/', views.parts.as_view(), name='parts'),
    path('upload_inventory', views.parts.as_view(), name='upload_inventory'),
    path('sales/', views.sales.as_view(), name='sales'),
    path('customers/', customer_list, name='customer_list'),
    path('generate-quote/<int:customer_id>/', views.generate_quote, name='generate_quote'),
    path('part-search/', views.part_search, name='part_search'),
    path('send-invoice/<int:customer_id>/', views.send_invoice, name='send_invoice'),
    path('vehicles/', views.vehicles.as_view(), name='vehicles'),
    path('inventory-addition-success/', views.inventory_addition_success, name='inventory_addition_success'),
]