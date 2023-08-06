from rest_framework import serializers
from lionclaw.orders.models import Order, OrderItem
from lionclaw.products.serializers import ProductVariantSerializer
from lionclaw.shipping.serializers import AddressSerializer

class OrderItemSerializer(serializers.ModelSerializer):

    product = ProductVariantSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True)
    shipping_address = AddressSerializer()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_total(self, obj):
        return obj.total
