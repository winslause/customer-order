from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Customer, Category, Product, Order, OrderItem
from .serializers import CustomerSerializer, CategorySerializer, ProductSerializer, OrderSerializer
from django.db.models import Avg
from django.contrib.auth import logout
from django.conf import settings
import urllib.parse

def oidc_logout(request):
    """Custom OIDC logout function to clear session and redirect to Auth0 logout."""
    logout(request)
    logout_url = settings.OIDC_OP_LOGOUT_URL
    return_to = urllib.parse.quote(settings.LOGOUT_REDIRECT_URL)
    full_logout_url = f"{logout_url}?client_id={settings.OIDC_RP_CLIENT_ID}&returnTo={return_to}"
    return redirect(full_logout_url)

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')

class CustomerListView(LoginRequiredMixin, View):
    def get(self, request):
        customers = Customer.objects.all()
        return render(request, 'customers.html', {'customers': customers})

class CustomerCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'customer_form.html')

    def post(self, request):
        name = request.POST.get('name')
        code = request.POST.get('code')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        try:
            if not name or not code:
                raise ValueError("Name and code are required.")
            Customer.objects.create(name=name, code=code, phone=phone, email=email)
            messages.success(request, 'Customer added successfully!')
            return redirect('customers')
        except Exception as e:
            messages.error(request, f'Error adding customer: {str(e)}')
            return render(request, 'customer_form.html')

class CategoryListView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'categories.html', {'categories': categories})

class CategoryCreateView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'category_form.html', {'categories': categories})

    def post(self, request):
        name = request.POST.get('name')
        parent_id = request.POST.get('parent')
        try:
            if not name:
                raise ValueError("Name is required.")
            parent = Category.objects.get(id=parent_id) if parent_id else None
            Category.objects.create(name=name, parent=parent)
            messages.success(request, 'Category added successfully!')
            return redirect('categories')
        except Exception as e:
            messages.error(request, f'Error adding category: {str(e)}')
            return render(request, 'category_form.html', {'categories': Category.objects.all()})

class ProductListView(LoginRequiredMixin, View):
    def get(self, request):
        products = Product.objects.all()
        return render(request, 'products.html', {'products': products})

class ProductCreateView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'product_form.html', {'categories': categories})

    def post(self, request):
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        description = request.POST.get('description')
        try:
            if not name or not category_id or not price:
                raise ValueError("Name, category, and price are required.")
            category = Category.objects.get(id=category_id)
            Product.objects.create(name=name, category=category, price=price, description=description)
            messages.success(request, 'Product added successfully!')
            return redirect('products')
        except Exception as e:
            messages.error(request, f'Error adding product: {str(e)}')
            return render(request, 'product_form.html', {'categories': Category.objects.all()})

class OrderListView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.all()
        return render(request, 'orders.html', {'orders': orders})

class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        customers = Customer.objects.all()
        products = Product.objects.all()
        return render(request, 'order_form.html', {'customers': customers, 'products': products})

    def post(self, request):
        customer_id = request.POST.get('customer')
        product_ids = request.POST.getlist('products')
        try:
            if not customer_id or not product_ids:
                raise ValueError("Customer and products are required.")
            customer = Customer.objects.get(id=customer_id)
            order = Order.objects.create(customer=customer)
            total_amount = 0
            for product_id in product_ids:
                product = Product.objects.get(id=product_id)
                quantity_key = f'quantity_{product_id}'
                quantity = int(request.POST.get(quantity_key, 1))
                if quantity <= 0:
                    raise ValueError("Quantity must be positive.")
                price = product.price
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
                total_amount += quantity * price
            order.total_amount = total_amount
            order.save()
            messages.success(request, 'Order added successfully!')
            return redirect('orders')
        except Exception as e:
            messages.error(request, f'Error adding order: {str(e)}')
            return render(request, 'order_form.html', {
                'customers': Customer.objects.all(),
                'products': Product.objects.all(),
                'error': str(e)
            })

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    def perform_create(self, serializer):
        order = serializer.save()
        total_amount = sum(item.quantity * item.price for item in order.order_items.all())
        order.total_amount = total_amount
        order.save()

    @action(detail=False, methods=['get'], url_path='category-average-price/(?P<category_id>\d+)')
    def category_average_price(self, request, category_id=None):
        try:
            category = Category.objects.get(id=category_id)
            descendants = category.get_descendants(include_self=True)
            avg_price = Product.objects.filter(category__in=descendants).aggregate(Avg('price'))['price__avg']
            return Response({'category': category.name, 'average_price': avg_price or 0})
        except Category.DoesNotExist:
            return Response({'error': 'Category not found'}, status=404)