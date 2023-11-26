from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import Collection, Product, Review, Cart, CartItem, Customer, Order, OrderItem

class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']
        # fields = ['id', 'title']

    products_count = serializers.IntegerField(read_only = True)

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return round(product.unit_price * Decimal(1.1), 2)
    

    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    # price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # # collection = serializers.PrimaryKeyRelatedField(
    # #     queryset=Collection.objects.all()
    # # )
    # # collection = serializers.StringRelatedField()
    # # collection = CollectionSerializer()
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection_detail'
    # )

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id = product_id,**validated_data)

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']
    
class CartItemSerializer(serializers.ModelSerializer):

    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField('get_total_price')

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'quantity', 'product', 'total_price']

    def get_total_price(self, cart_item: CartItem):
        return cart_item.product.unit_price * cart_item.quantity

    
class CartSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only = True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']

    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

class AddCartItemSerializer(serializers.ModelSerializer):

    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product found')
        return value


    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart_id = cart_id, product_id = product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id = cart_id, **self.validated_data)
        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

class UpdateCartItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CartItem
        fields = ['quantity']

class CustomerSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']

class OrderItemSerializer(serializers.ModelSerializer):

    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'unit_price', 'product']

class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'placed_at', 'payment_status', 'customer_id', 'items']

class CreateOrderSerializer(serializers.Serializer):

    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart with the given ID exists')
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validate_cart_id(self.validated_data['cart_id'])
            user_id = self.context['user_id']
            (customer, created) = Customer.objects.get_or_create(user_id=user_id)
            order = Order.objects.create(customer = customer)

            order_items = [OrderItem(
                order = order,
                product = item.product,
                quantity = item.quantity,
                unit_price = item.product.unit_price
            ) for item in CartItem.objects.filter(cart=cart_id)]

            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(pk=cart_id).delete()

            return order