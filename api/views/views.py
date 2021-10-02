from rest_framework import generics
from rest_framework import status
from api.serializers import *
from api.models import *
import json
import copy
import datetime as datetimemod
from rest_framework.views import Response

import logging

logger = logging.getLogger("ten.server")


class products(generics.ListCreateAPIView):
    serializer_class = Products

    def get(self, request, *arg, **kwargs):
        querySet = Products.objects.all()
        data = self.formatProductObject(ProductsSerializer(querySet, many=True).data)
    
        return Response({"status": "success", "data": data}, status=200)

    def formatProductObject(self, data):
        for product in data:
            attributeDictionary = {}
            for attribute in product['attributes']:
                attributeName = attribute['attributes']['name']
                optionName = attribute['options']['name']
                if attributeName in attributeDictionary:
                    attributeDictionary[attributeName]['options'].append(optionName)
                else:
                    attributeDictionary[attributeName] = {
                        "name": attributeName,
                        "options": [optionName]
                    }

            product['attributes'] = []
            for attribute in attributeDictionary:
                 product['attributes'].append(attributeDictionary[attribute])

        return data

    def post(self, request, *args, **kwargs):
        dataObject = json.loads(request.body.decode("utf-8"))

        productObject = self.insertProduct(dataObject['name'])
        self.insertAttributesOptions(dataObject['attributes'], productObject)

        return Response({"status": "success", "data": []}, status=200)

    def insertProduct(self, name):
        productObject = Products(name = name)
        productObject.save()

        return productObject

    def insertAttributesOptions(self, attributes, productObject):
        for attribute in attributes:
            logger.info("attribute name: {} options: {}".format(attribute['name'], attribute['options']))
            attributeObject = Attributes(name = attribute['name'])
            attributeObject.save()

            for option in attribute['options']:
                optionObj = Options(name = option)
                optionObj.save()

                attributesOptionsMappingObject = AttributesOptionsMapping(
                    products = productObject,
                    attributes = attributeObject,
                    options = optionObj
                )

                attributesOptionsMappingObject.save()
