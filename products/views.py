import uuid

from rest_framework.decorators import api_view

from .models import Product
from .response_handler import StandardResponse
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
            search_terms = []
            if name_query:
                search_terms.append(f"name='{name_query}'")
            if location_query:
                search_terms.append(f"location='{location_query}'")

            if search_terms:
                message = f"No products found matching {' and '.join(search_terms)}"
            else:
                message = "No products available"

            return StandardResponse.empty_list(message=message)

        return StandardResponse.success(
            data={"products": serializer.data},
            message=f"Retrieved {len(serializer.data)} product(s) successfully",
        )

    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            product = serializer.save()
            return StandardResponse.created(
                data=serializer.data, message="Product created successfully"
            )
        return StandardResponse.validation_error(
            errors=serializer.errors,
            message="Product creation failed due to validation errors",
        )


@api_view(["GET", "PUT", "DELETE"])
def product_detail(request, product_id):
    # Validate UUID format first
    try:
        uuid.UUID(str(product_id))
    except (ValueError, TypeError):
        return StandardResponse.not_found(message="Product not found")

    try:
        product = Product.objects.get(id=product_id, is_delete=False)
    except Product.DoesNotExist:
        return StandardResponse.not_found(message="Product not found")

    if request.method == "GET":
        serializer = ProductSerializer(product, context={"request": request})
        return StandardResponse.success(
            data=serializer.data, message="Product retrieved successfully"
        )

    elif request.method == "PUT":
        serializer = ProductSerializer(
            product, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return StandardResponse.success(
                data=serializer.data, message="Product updated successfully"
            )
        return StandardResponse.validation_error(
            errors=serializer.errors,
            message="Product update failed due to validation errors",
        )

    elif request.method == "DELETE":
        product.is_delete = True
        product.save()
        return StandardResponse.success(
            data={"deleted_id": str(product.id)}, message="Product deleted successfully"
        )
