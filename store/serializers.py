from rest_framework import serializers
from .models import Collection

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    # collection_id = serializers.IntegerField()
    collection = serializers.SerializerMethodField(method_name='get_collection_title')

    def get_collection_title(self, collection=Collection):
        return collection.title
