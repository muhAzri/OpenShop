import uuid

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .serializers import ProductListSerializer, ProductSerializer


@api_view(["GET", "POST"])
def product_list(request):
    if request.method == "GET":
        name_query = request.GET.get("name", "")
        location_query = request.GET.get("location", "")

        products = Product.objects.filter(is_delete=False)

        if name_query:
            products = products.filter(name__icontains=name_query)

        if location_query:
            products = products.filter(location__icontains=location_query)

        serializer = ProductListSerializer(
            products, many=True, context={"request": request}
        )

        # Check if products list is empty
        if not serializer.data:
            return Response(
                {"products": []}, 
                status=status.HTTP_200_OK,
                content_type="application/json"
            )

        return Response(
            {"products": serializer.data}, 
            status=status.HTTP_200_OK,
            content_type="application/json"
        )

    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            # Return flattened response structure for Postman test compatibility
            response_data = {
                **serializer.data,  # Flatten product data to root level
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def product_detail(request, product_id):
    # Validate UUID format first
    try:
        uuid.UUID(str(product_id))
    except (ValueError, TypeError):
        return Response(
            {"detail": "Not found."},
            status=status.HTTP_404_NOT_FOUND,
            content_type="application/json"
        )

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {"detail": "Not found."},
            status=status.HTTP_404_NOT_FOUND,
            content_type="application/json"
        )

    if request.method == "GET":
        serializer = ProductSerializer(product, context={"request": request})
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            content_type="application/json"
        )

    elif request.method == "PUT":
        serializer = ProductSerializer(
            product, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
                content_type="application/json"
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == "DELETE":
        product.is_delete = True
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
