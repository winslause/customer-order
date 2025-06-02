from rest_framework import serializers
from .models import Customer, Category, Product, Order, OrderItem

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'code', 'phone', 'email']

    def validate_code(self, value):
        if not value:
            raise serializers.ValidationError("Code is required.")
        return value

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name is required.")
        return value

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'description']

    def validate(self, data):
        if not data.get('name') or not data.get('price'):
            raise serializers.ValidationError("Name and price are required.")
        return data

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'total_amount', 'time', 'order_items']

    def validate(self, data):
        # Ensure order_items is not empty
        if not data.get('order_items'):
            raise serializers.ValidationError("At least one order item is required.")
        # Calculate total_amount from order_items
        total_amount = sum(item['quantity'] * item['price'] for item in data.get('order_items', []))
        if total_amount < 0:
            raise serializers.ValidationError("Total amount cannot be negative.")
        data['total_amount'] = total_amount
        return data

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        # Create order with calculated total_amount
        order = Order.objects.create(**validated_data)
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order