from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

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
        try:
            Customer.objects.create(name=name, code=code, phone=phone)
            messages.success(request, 'Customer added successfully!')
            return redirect('customers')
        except Exception as e:
            messages.error(request, f'Error adding customer: {str(e)}')
            return render(request, 'customer_form.html')

class OrderListView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.all()
        return render(request, 'orders.html', {'orders': orders})

class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        customers = Customer.objects.all()
        return render(request, 'order_form.html', {'customers': customers})

    def post(self, request):
        customer_id = request.POST.get('customer')
        item = request.POST.get('item')
        amount = request.POST.get('amount')
        try:
            customer = Customer.objects.get(id=customer_id)
            Order.objects.create(customer=customer, item=item, amount=amount)
            messages.success(request, 'Order added successfully!')
            return redirect('orders')
        except Exception as e:
            messages.error(request, f'Error adding order: {str(e)}')
            return render(request, 'order_form.html', {'customers': Customer.objects.all()})

# API Viewsets
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]