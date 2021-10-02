from django.db import models

class Products(models.Model):
    name = models.CharField(max_length=255, null=False)

class Attributes(models.Model):
    name = models.CharField(max_length=255, null=False)

class Options(models.Model):
    name = models.CharField(max_length=255, null=False)

class AttributesOptionsMapping(models.Model):
    products = models.ForeignKey("Products", null=False, related_name='products_mapping', on_delete=models.CASCADE)
    attributes = models.ForeignKey("Attributes", null=False, related_name='attribute_mapping', on_delete=models.CASCADE)
    options = models.ForeignKey("Options", null=False, related_name='options_mapping', on_delete=models.CASCADE)