from rest_framework import generics
from rest_framework import status
from api.serializers import *
from api.models import *
from django.db import transaction
import json
from rest_framework.views import Response

import logging

logger = logging.getLogger("ten.server")

class products(generics.ListCreateAPIView):
    serializer_class = Products

    def get(self, request, *arg, **kwargs):
        querySet = Products.objects.all()
        serializedData = ProductsSerializer(querySet, many=True).data
    
        return Response({"status": "success", "data": serializedData}, status=200)

    def post(self, request, *args, **kwargs):
        dataObject = json.loads(request.body.decode("utf-8"))

        try:
            with transaction.atomic():
                productObject = self.insertProduct(dataObject)
        except ValueError as error:
            return Response({"status": "failure", "errorMessage": str(error)}, status=400)
        except Exception as error:
            logger.info(repr(error))
            return Response({"status": "error", "errorMessage": "Something went wrong"}, status=500)

        return Response({"status": "success", "data": []}, status=200)

    '''
        Params: 
            - product with valid "name"
            - product with list of attributes is optional
    '''
    def insertProduct(self, product):
        if not 'name' in product or not product['name']:
            raise ValueError("Product name cannot be empty")

        if len(product['name']) > 255:
            raise ValueError("Product name must be less than 255 characters")

        productObject = Products(name = product['name'])
        productObject.save()

        if 'attributes' in product:
            self.insertAttributes(product['attributes'], productObject)

        return productObject

    '''
        Params: 
            - attributes with valid "name"
            - attributes with list of options
            - valid Products object
    '''
    def insertAttributes(self, attributes, productObject):
        if not productObject:
            raise TypeError("insertAttributes: productObject is not valid")

        attributeSet = set()

        for attribute in attributes:
            if not 'name' in attribute or not attribute['name']:
                raise ValueError("Attribute name cannot be empty")

            if attribute['name'] in attributeSet:
                raise ValueError("Cannot have duplicate attributes for a single product")

            if not 'options' in attribute:
                raise ValueError("Options are required to assign to attribute")

            if len(attribute['name']) > 255:
                raise ValueError("Attribute name must be less than 255 characters")

            attributeObject = Attributes(name = attribute['name'], products = productObject)
            attributeObject.save()
            attributeSet.add(attribute['name'])

            self.insertOptions(attribute['options'], attributeObject)

    '''
        Params: 
            - options with valid "name"
            - valid Attributes object
    '''
    def insertOptions(self, options, attributeObject):
        if not attributeObject:
            raise TypeError("insertAttributes: attributeObject is not valid")

        if len(options) == 0:
            raise ValueError("Cannot have empty list of options for an attribute")

        optionSet = set()

        for option in options:
            if not "name" in option or not option['name']:
                raise ValueError("Option name cannot be empty")

            if option['name'] in optionSet:
                raise ValueError("Cannot have duplicate options for a single attribute")

            if len(option['name']) > 255:
                raise ValueError("Option name must be less than 255 characters")

            optionObj = Options(name = option['name'], attributes = attributeObject)
            optionObj.save()
            optionSet.add(option['name'])
