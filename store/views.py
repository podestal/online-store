from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q, F
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from store.models import Product
from store.serializers import ProductSerializer

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        query_set = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(query_set, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    # product = Product.objects.filter(pk=1).first()
    # query_set = Product.objects.all()
    # lookup values
    # query_set = Product.objects.filter(unit_price__gt=70)
    # query_set = Product.objects.filter(unit_price__lte=70)
    # query_set = Product.objects.filter(unit_price__lte=70)
    # query_set = Product.objects.filter(unit_price__range=(60, 70))
    # query_set = Product.objects.filter(title__icontains='coffee')
    # query_set = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
    # | OR, & AND ... ~ before Q object, it negates the expression
    # query_set = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
    # Products where inventory = unit_price
    # query_set = Product.objects.filter(inventory = F('unit_price'))
    # query_set = Product.objects.order_by('unit_price', '-title')
    # query_set = Product.objects.filter(collection_id = 3)
    # query_set = Product.objects.annotate(new_id=56)
    # query_set = Product.objects.values('id', 'title')
    # serializer = ProductSerializer(query_set, many=True)
    # print(product.title)
    # return Response(serializer.data)
    # Select related is going to load all products with their collections to prevent making unnecesary queries

    # query_set = Product.objects.all()


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    # product = Product.objects.get(pk=id)
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if product.orderitems.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view()
def collection_detail(request, id):
    return Response('ok')