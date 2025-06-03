from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('customers/', views.CustomerListView.as_view(), name='customers'),
    path('customers/add/', views.CustomerCreateView.as_view(), name='customer_add'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category_add'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/add/', views.OrderCreateView.as_view(), name='order_add'),
    path('api/', include(router.urls)),
    
    path('logout/', views.oidc_logout, name='logout'),
]