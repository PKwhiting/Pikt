from django.db import models

# Create your models here.
class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)
    user = models.ForeignKey('Authentication.User', on_delete=models.CASCADE)
    status = models.CharField(max_length=100, null=True, blank=True)
    html = models.TextField(null=True, blank=True)
    destination = models.ForeignKey('dashboards.Customer', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)