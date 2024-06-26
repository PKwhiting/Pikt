from rest_framework import serializers

class InventoryItemSerializer(serializers.Serializer):
    sku = serializers.CharField(max_length=50)
    locale = serializers.CharField(max_length=10, default='en_US')
    condition = serializers.CharField(max_length=50)
    title = serializers.CharField(max_length=80)
    description = serializers.CharField(max_length=4000)
    quantity = serializers.IntegerField()
    # Add other relevant fields based on eBay API documentation
