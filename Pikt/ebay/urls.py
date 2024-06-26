from django.urls import path
from . import views  


urlpatterns = [
    path('bulk_create_or_replace_inventory_item/', views.BulkCreateOrReplaceInventoryItemView.as_view(), name='bulk_create_or_replace_inventory_item'),
]