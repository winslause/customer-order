from django.contrib import admin
from django.urls import path, include
from core.views import HomeView, CustomerListView, OrderListView, CustomerCreateView, OrderCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),  # API endpoints
    path('oidc/', include('mozilla_django_oidc.urls')),  # OIDC routes
    path('', HomeView.as_view(), name='home'),
    path('customers/', CustomerListView.as_view(), name='customers'),
    path('customers/add/', CustomerCreateView.as_view(), name='customer_add'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('orders/add/', OrderCreateView.as_view(), name='order_add'),
    path('oidc/', include('mozilla_django_oidc.urls')),  
]