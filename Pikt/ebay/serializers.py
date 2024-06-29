from rest_framework import serializers
from decimal import Decimal

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
    condition = serializers.ChoiceField(choices=["USED_EXCELLENT", "FOR_PARTS_OR_NOT_WORKING"])
    conditionDescription = serializers.CharField(max_length=1000, required=False)
    conditionDescriptors = ConditionDescriptorSerializer(many=True, required=False)
    packageWeightAndSize = PackageWeightAndSizeSerializer(required=False)
    availability = AvailabilitySerializer(required=False)
    product = ProductSerializer()

    def to_representation(self, instance):
        image_urls = []
        for i in range(1, 11):
            image_field = getattr(instance, f"image_{i}", None)
            if image_field:
                image_urls.append(image_field.url)
        return {
            "sku": instance.stock_number,
            "locale": "en_US",
            "condition": "USED_EXCELLENT" if instance.grade == "A" or instance.grade == "B" else "FOR_PARTS_OR_NOT_WORKING",
            "availability": {
                "shipToLocationAvailability": {
                    "quantity": 1
                }
            },
            "packageWeightAndSize": {
                "dimensions": {
                    "unit": "INCH",
                    "height": instance.height,
                    "length": instance.length,
                    "width": instance.width
                },
                "weight": {
                    "unit": "POUND",
                    "value": instance.weight
                }
            },
            "product": {
                "title": instance.type,
                "brand": instance.brand if instance.brand is not None and instance.brand.strip() else instance.vehicle.make,
                "mpn": instance.part_number if instance.part_number else instance.stock_number,
                "description": instance.description if instance.description is not None and instance.description.strip() else f'{instance.type} {instance.stock_number}',
                "imageUrls": image_urls,
                "aspects": {
                    "brand": [instance.brand if instance.brand is not None and instance.brand.strip() else instance.vehicle.make],
                    "MPN": [instance.part_number] if instance.part_number else [instance.stock_number],
                    "UPC": ["Does Not Apply"],
                }
            }
        }

class AmountSerializer(serializers.Serializer):
    currency = serializers.CharField(max_length=3)
    value = serializers.CharField(max_length=50)

class CharitySerializer(serializers.Serializer):
    charityId = serializers.CharField(max_length=50)
    donationPercentage = serializers.CharField(max_length=5)

class ExtendedProducerResponsibilitySerializer(serializers.Serializer):
    ecoParticipationFee = AmountSerializer()
    producerProductId = serializers.CharField(max_length=50, required=False)
    productDocumentationId = serializers.CharField(max_length=50, required=False)
    productPackageId = serializers.CharField(max_length=50, required=False)
    shipmentPackageId = serializers.CharField(max_length=50, required=False)

class BestOfferSerializer(serializers.Serializer):
    autoAcceptPrice = AmountSerializer(required=False)
    autoDeclinePrice = AmountSerializer(required=False)
    bestOfferEnabled = serializers.BooleanField()

class CountryPolicySerializer(serializers.Serializer):
    country = serializers.CharField(max_length=2)
    policyIds = serializers.ListField(child=serializers.CharField(max_length=50))

class RegionalProductCompliancePoliciesSerializer(serializers.Serializer):
    countryPolicies = CountryPolicySerializer(many=True)

class ShippingCostOverrideSerializer(serializers.Serializer):
    additionalShippingCost = AmountSerializer(required=False)
    priority = serializers.IntegerField()
    shippingCost = AmountSerializer(required=False)
    shippingServiceType = serializers.ChoiceField(choices=["DOMESTIC", "INTERNATIONAL"])
    surcharge = AmountSerializer(required=False)

class ListingPoliciesSerializer(serializers.Serializer):
    bestOfferTerms = BestOfferSerializer(required=False)
    eBayPlusIfEligible = serializers.BooleanField(required=False)
    fulfillmentPolicyId = serializers.CharField(max_length=50)
    paymentPolicyId = serializers.CharField(max_length=50)
    productCompliancePolicyIds = serializers.ListField(child=serializers.CharField(max_length=50), required=False)
    regionalProductCompliancePolicies = RegionalProductCompliancePoliciesSerializer(required=False)
    returnPolicyId = serializers.CharField(max_length=50)
    shippingCostOverrides = ShippingCostOverrideSerializer(many=True, required=False)
    takeBackPolicyId = serializers.CharField(max_length=50, required=False)

class PricingSummarySerializer(serializers.Serializer):
    auctionReservePrice = AmountSerializer(required=False)
    auctionStartPrice = AmountSerializer(required=False)
    minimumAdvertisedPrice = AmountSerializer(required=False)
    originallySoldForRetailPriceOn = serializers.ChoiceField(choices=["ON_EBAY", "OFF_EBAY", "ON_AND_OFF_EBAY"], required=False)
    originalRetailPrice = AmountSerializer(required=False)
    price = AmountSerializer(required=False)
    pricingVisibility = serializers.ChoiceField(choices=["NONE", "PRE_CHECKOUT", "DURING_CHECKOUT"], required=False)

class EconomicOperatorSerializer(serializers.Serializer):
    addressLine1 = serializers.CharField(max_length=100)
    addressLine2 = serializers.CharField(max_length=100, required=False)
    city = serializers.CharField(max_length=50)
    companyName = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=2)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(max_length=20, required=False)
    postalCode = serializers.CharField(max_length=20)
    stateOrProvince = serializers.CharField(max_length=50)

class EnergyEfficiencyLabelSerializer(serializers.Serializer):
    imageDescription = serializers.CharField(max_length=100)
    imageURL = serializers.URLField()
    productInformationSheet = serializers.URLField()

class HazmatSerializer(serializers.Serializer):
    component = serializers.CharField(max_length=120, required=False)
    pictograms = serializers.ListField(child=serializers.CharField(max_length=50), required=False)
    signalWord = serializers.CharField(max_length=50, required=False)
    statements = serializers.ListField(child=serializers.CharField(max_length=50), required=False)

class RegulatorySerializer(serializers.Serializer):
    economicOperator = EconomicOperatorSerializer(required=False)
    energyEfficiencyLabel = EnergyEfficiencyLabelSerializer(required=False)
    hazmat = HazmatSerializer(required=False)
    repairScore = serializers.FloatField(required=False)

class EbayOfferDetailsWithKeysSerializer(serializers.Serializer):
    availableQuantity = serializers.IntegerField()
    categoryId = serializers.CharField(max_length=50)
    charity = CharitySerializer(required=False)
    extendedProducerResponsibility = ExtendedProducerResponsibilitySerializer(required=False)
    format = serializers.ChoiceField(choices=["AUCTION", "FIXED_PRICE"])
    hideBuyerDetails = serializers.BooleanField(required=False)
    includeCatalogProductDetails = serializers.BooleanField(required=False, default=True)
    listingDescription = serializers.CharField(max_length=500000, required=False)
    listingDuration = serializers.ChoiceField(choices=["DAYS_1", "DAYS_3", "DAYS_5", "DAYS_7", "DAYS_10"], required=False)
    listingPolicies = ListingPoliciesSerializer()
    listingStartDate = serializers.DateTimeField(required=False)
    lotSize = serializers.IntegerField(required=False)
    marketplaceId = serializers.ChoiceField(choices=["EBAY_US", "EBAY_MOTORS", "EBAY_CA"])
    merchantLocationKey = serializers.CharField(max_length=36, required=False)
    pricingSummary = PricingSummarySerializer(required=False)
    quantityLimitPerBuyer = serializers.IntegerField(required=False)
    regulatory = RegulatorySerializer(required=False)
    secondaryCategoryId = serializers.CharField(max_length=50, required=False)
    sku = serializers.CharField(max_length=50)
    storeCategoryNames = serializers.ListField(child=serializers.CharField(max_length=100), required=False)
    tax = serializers.JSONField(required=False)

    def to_representation(self, instance):
        image_urls = [img.image.url for img in instance.part_images.all()]
        return {
            "sku": instance.stock_number,
            "availableQuantity": 1,
            "categoryId": instance.ebay_category_id,
            # "charity": {},
            # "extendedProducerResponsibility": {},
            "format": "FIXED_PRICE",
            # "hideBuyerDetails": "",
            # "includeCatalogProductDetails": "",
            # "listingDescription": "",
            "listingDuration": "GTC",
            "listingPolicies": {
            #     "bestOfferTerms": {},
            #     "eBayPlusIfEligible": "",
                "fulfillmentPolicyId": instance.company.ebay_credentials.fulfillment_policy.policy_id,
                "paymentPolicyId": instance.company.ebay_credentials.payment_policy.policy_id,
            #     "productCompliancePolicyIds": [],
            #     "regionalProductCompliancePolicies": {},
                "returnPolicyId": instance.company.ebay_credentials.return_policy.policy_id,
            #     "shippingCostOverrides": [],
            #     "takeBackPolicyId": ""
            },
            # "listingStartDate": "",
            # "lotSize": "",
            "marketplaceId": "EBAY_MOTORS",
            "merchantLocationKey": instance.company.ebay_merchant_location_key,
            "pricingSummary": {
            #     "auctionReservePrice": "",
            #     "auctionStartPrice": "",
            #     "minimumAdvertisedPrice": "",
            #     "originallySoldForRetailPriceOn": "",
            #     "originalRetailPrice": "",
                "price": {
                    "currency": "USD",
                    "value": float(instance.price) if instance.price > Decimal('1.00') else "1000.00"
                },
            #     "pricingVisibility": ""
            },
            # "quantityLimitPerBuyer": "",
            # "regulatory": {
            #     "economicOperator": "",
            #     "energyEfficiencyLabel": "",
            #     "hazmat": "",
            #     "repairScore": ""
            # },
            # "secondaryCategoryId": "",
            # "storeCategoryNames": "",
            # "tax": "",
            # "product": {
            #     "title": "",
            #     "description": "",
            #     "imageUrls": ""
            # }
        }


class BulkEbayOfferDetailsWithKeysSerializer(serializers.Serializer):
    requests = EbayOfferDetailsWithKeysSerializer(many=True)

    def to_representation(self, queryset):
        return {
            "requests": [EbayOfferDetailsWithKeysSerializer(instance).data for instance in queryset]
        }

    def create(self, validated_data):
        # Additional processing if needed
        return validated_data

class BulkInventoryItemSerializer(serializers.Serializer):
    requests = InventoryItemSerializer(many=True)

    def to_representation(self, queryset):
        return {
            "requests": [InventoryItemSerializer(instance).data for instance in queryset]
        }

    def create(self, validated_data):
        # Additional processing if needed
        return validated_data
    
class BulkOfferSerializer(serializers.Serializer):
    offerId = serializers.CharField(max_length=100)

class BulkPublishOfferRequestSerializer(serializers.Serializer):
    requests = BulkOfferSerializer(many=True)

    def to_representation(self, queryset):
        requests = [{"offerId": instance.ebay_offer_id} for instance in queryset]
        return {
            "requests": requests
        }