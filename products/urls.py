from django.urls import path, re_path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    re_path(r'^products/(?P<product_id>[^/]+)/$', views.product_detail, name='product_detail'),
]