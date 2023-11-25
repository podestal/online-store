from django.shortcuts import render
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q, F
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework import status
from rest_framework.views import APIView
from store.models import Product, Collection, OrderItem, Review, Cart, CartItem, Customer
from store.serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, CustomerSerializer
from store.filters import ProductFilter
from store.pagination import DefaultPagination
from store.permissions import IsAdminOrReadOnly
from django.db.models.aggregates import Count
from django.db.models import Value

    # def get(self, request):
    #     query_set = Product.objects.select_related('collection').all()
    #     serializer = ProductSerializer(query_set, many=True, context={'request': request})
    #     return Response(serializer.data)
    
    # def post(self, request):
    #     serializer = ProductSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# class ProductDetail(RetrieveUpdateDestroyAPIView):

#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
    # def get(self, request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data)
    
    # def put(self, request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     serializer = ProductSerializer(product, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)
    
    # def delete(self, request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     if product.orderitems.count() > 0:
    #         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         query_set = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(query_set, many=True, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    


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


# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, id):
#     # product = Product.objects.get(pk=id)
#     product = get_object_or_404(Product, pk=id)
#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if product.orderitems.count() > 0:
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class ProductList(ListCreateAPIView):

#     queryset = Product.objects.select_related('collection').all()
#     serializer_class = ProductSerializer

    # def get_serializer_context(self):
    #     return {'request': self.request}

# class ProductDetail(RetrieveUpdateDestroyAPIView):

#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     # queryset = Collection.objects.all()
#     serializer_class = CollectionSerializer

# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer

# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         # query_set = Collection.objects.annotate(nueva=Value(6)).all()
#         query_set = Collection.objects.annotate(products_count=Count('products')).all()
#         serializer = CollectionSerializer(query_set, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     if request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_detail(request, id):
#     collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=id)
#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data, status=status.HTTP_200_OK)

class ProductViewSet(ModelViewSet):
    # queryset = Product.objects.select_related('collection').all()
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]

    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id = collection_id)
    #     return queryset

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id = kwargs.get('pk')).count() > 0:
            return Response({'error': 'Product cannot be deleted'})
        return super().destroy(request, *args, **kwargs)
        # product = get_object_or_404(Product, pk=id)
        # if product.orderitems.count() > 0:
        #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        # product.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id = kwargs.get('pk')).count() > 0:
            return Response({'error': 'Product cannot be deleted'})
        return super().destroy(request, *args, **kwargs)
    
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    
class CartViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['carts_pk']}

    def get_queryset(self):
        return CartItem.objects \
            .filter(cart_id=self.kwargs['carts_pk']) \
            .select_related('product')

class CustomerViewSet(ModelViewSet):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [DjangoModelPermissions]

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        # (customer, created) = Customer.objects.get_or_create(user_id=request.user.id)
        customer = Customer.objects.get(user_id=3)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
