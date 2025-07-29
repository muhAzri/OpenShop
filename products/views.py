from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.exceptions import ValidationError
import uuid
from .models import Product
from .serializers import ProductSerializer, ProductListSerializer


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        name_query = request.GET.get('name', '')
        location_query = request.GET.get('location', '')
        
        products = Product.objects.filter(is_delete=False)
        
        if name_query:
            products = products.filter(name__icontains=name_query)
        
        if location_query:
            products = products.filter(location__icontains=location_query)
        
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response({'products': serializer.data}, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            product = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, product_id):
    # Validate UUID format first
    try:
        uuid.UUID(str(product_id))
    except (ValueError, TypeError):
        return Response({'message': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        product = Product.objects.get(id=product_id, is_delete=False)
    except Product.DoesNotExist:
        return Response({'message': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        product.is_delete = True
        product.save()
        return Response({'message': 'Product deleted successfully.'}, status=status.HTTP_200_OK)
