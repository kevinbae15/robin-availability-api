from rest_framework import serializers
from .models import *

class OptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Options
        fields = ['name']

class AttributesSerializer(serializers.ModelSerializer):
    options = OptionsSerializer(source='attribute_mapping', many=True)
    class Meta:
        model = Attributes
        fields = ['name', 'options']

class ProductsSerializer(serializers.ModelSerializer):
    attributes = AttributesSerializer(source='products_mapping', many=True)

    class Meta:
        model = Products
        fields = ['name', 'attributes']
