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
    path('single_part/<int:item_id>/', views.single_item.as_view(), name='single_part'),
    path('single_vehicle/<int:item_id>/', views.single_item.as_view(), name='single_vehicle'),
    path('delete_part/<int:item_id>/', views.delete_item, name='delete_part'),
    path('edit_part/<int:item_id>/', views.edit_item.as_view(), name='edit_part'),
    path('delete_vehicle/<int:item_id>/', views.delete_item, name='delete_vehicle'),
    path('edit_vehicle/<int:item_id>/', views.edit_item.as_view(), name='edit_vehicle'),
    path('ebay_consent/', views.ebayConsent.as_view(), name='ebay_consent'),
    path('ebay_consent/redirect/', views.RedirectView.as_view(), name='redirect'),
    path('orders/', views.orders.as_view(), name='orders'),
    path('yard/', views.yard.as_view(), name='yard'),
    path('parts/', views.defaultDashboardView.as_view(), name='parts'),
    # path('upload_inventory', views.parts.as_view(), name='upload_inventory'),
    path('sales/', views.sales.as_view(), name='sales'),
    path('customers/', customer_list, name='customer_list'),
    path('generate-quote/<int:customer_id>/', views.generate_quote, name='generate_quote'),
    path('part-search/', views.part_search, name='part_search'),
    path('send-invoice/<int:customer_id>/', views.send_invoice, name='send_invoice'),
    path('vehicles/', views.VehiclesView.as_view(), name='vehicles'),
    path('inventory-addition-success/', views.inventory_addition_success, name='inventory_addition_success'),
    path('save-part-types/', views.SavePartTypesView.as_view(), name='save_part_types'),
    path('filter-vehicles/', views.FilterVehicles.as_view(), name='filter_vehicles'),
    path('filter-parts/', views.FilterParts.as_view(), name='filter_parts'),
    path('create_parts/', views.create_parts, name='create_parts')
]