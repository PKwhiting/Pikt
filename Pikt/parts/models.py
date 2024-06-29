from django.db import models
from dashboards.models import Part

# Create your models here.
class PartEbayCategorySpecification(models.Model):
    part_type = models.CharField(max_length=100, null=True, blank=True)
    ebay_category_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.part_type)