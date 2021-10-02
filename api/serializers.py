from rest_framework import serializers
from .models import *

class AttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attributes
        fields = ['name']

class OptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Options
        fields = ['name']


class AttributesOptionsMappingSerializer(serializers.ModelSerializer):
    attributes = AttributesSerializer()
    options = OptionsSerializer()

    class Meta:
        model = AttributesOptionsMapping
        fields = ['attributes', 'options']

class ProductsSerializer(serializers.ModelSerializer):
    attributes = AttributesOptionsMappingSerializer(source='products_mapping', many=True)

    class Meta:
        model = Products
        fields = ['name', 'attributes']
