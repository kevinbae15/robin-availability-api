from django.db import models

class Products(models.Model):
    name = models.CharField(max_length=255, null=False)

class Attributes(models.Model):
    products = models.ForeignKey("Products", null=False, related_name='products_mapping', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)

class Options(models.Model):
    attributes = models.ForeignKey("Attributes", null=False, related_name='attribute_mapping', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=False)