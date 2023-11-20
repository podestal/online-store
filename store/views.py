from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from store.models import Product
from store.serializers import ProductSerializer

@api_view()
def product_list(request):
    # product = Product.objects.filter(pk=1).first()
    query_set = Product.objects.all()
    serializer = ProductSerializer(query_set, many=True)
    # print(product.title)
    return Response(serializer.data)

@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)