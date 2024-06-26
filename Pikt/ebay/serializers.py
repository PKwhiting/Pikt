from rest_framework import serializers

class DimensionSerializer(serializers.Serializer):
    height = serializers.FloatField()
    length = serializers.FloatField()
    width = serializers.FloatField()
    unit = serializers.ChoiceField(choices=["INCH", "FEET", "CENTIMETER", "METER"])

class WeightSerializer(serializers.Serializer):
    value = serializers.FloatField()
    unit = serializers.ChoiceField(choices=["POUND", "KILOGRAM", "OUNCE", "GRAM"])

class PackageWeightAndSizeSerializer(serializers.Serializer):
    dimensions = DimensionSerializer()
    packageType = serializers.ChoiceField(choices=["LETTER", "BULKY_GOODS", "CARAVAN", "LARGE_PACKAGE"])
    shippingIrregular = serializers.BooleanField()
    weight = WeightSerializer()

class AvailabilityDistributionSerializer(serializers.Serializer):
    fulfillmentTime = serializers.IntegerField()
    unit = serializers.ChoiceField(choices=["YEAR", "MONTH", "DAY", "BUSINESS_DAY"])
    merchantLocationKey = serializers.CharField(max_length=36)
    quantity = serializers.IntegerField()

class ShipToLocationAvailabilitySerializer(serializers.Serializer):
    availabilityDistributions = AvailabilityDistributionSerializer(many=True)
    quantity = serializers.IntegerField()

class PickupAtLocationAvailabilitySerializer(serializers.Serializer):
    availabilityType = serializers.ChoiceField(choices=["IN_STOCK", "OUT_OF_STOCK", "SHIP_TO_STORE"])
    fulfillmentTime = serializers.IntegerField()
    unit = serializers.ChoiceField(choices=["YEAR", "MONTH", "DAY", "BUSINESS_DAY"])
    merchantLocationKey = serializers.CharField(max_length=36)
    quantity = serializers.IntegerField()

class AvailabilitySerializer(serializers.Serializer):
    pickupAtLocationAvailability = PickupAtLocationAvailabilitySerializer(many=True, required=False)
    shipToLocationAvailability = ShipToLocationAvailabilitySerializer(required=False)

class ConditionDescriptorSerializer(serializers.Serializer):
    additionalInfo = serializers.CharField(max_length=30, required=False)
    name = serializers.CharField(max_length=50)
    values = serializers.ListField(child=serializers.CharField(max_length=50))

class ProductSerializer(serializers.Serializer):
    aspects = serializers.JSONField(required=False)
    brand = serializers.CharField(max_length=65, required=False)
    description = serializers.CharField(max_length=4000, required=False)
    ean = serializers.ListField(child=serializers.CharField(max_length=50), required=False)
    epid = serializers.CharField(max_length=50, required=False)
    imageUrls = serializers.ListField(child=serializers.URLField(), required=False)
    isbn = serializers.ListField(child=serializers.CharField(max_length=50), required=False)
    mpn = serializers.CharField(max_length=65, required=False)
    subtitle = serializers.CharField(max_length=55, required=False)
    title = serializers.CharField(max_length=80)
    upc = serializers.ListField(child=serializers.CharField(max_length=50), required=False)
    videoIds = serializers.ListField(child=serializers.CharField(max_length=50), required=False)

class InventoryItemSerializer(serializers.Serializer):
    sku = serializers.CharField(max_length=50)
    locale = serializers.ChoiceField(choices=["en_US", "en_CA", "fr_CA", "en_AU", "en_GB", "de_DE"])
    condition = serializers.ChoiceField(choices=["NEW", "LIKE_NEW", "NEW_OTHER", "USED_VERY_GOOD", "USED_GOOD", "USED_ACCEPTABLE", "CERTIFIED_REFURBISHED"])
    conditionDescription = serializers.CharField(max_length=1000, required=False)
    conditionDescriptors = ConditionDescriptorSerializer(many=True, required=False)
    packageWeightAndSize = PackageWeightAndSizeSerializer(required=False)
    availability = AvailabilitySerializer(required=False)
    product = ProductSerializer()

