from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    _links = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "sku",
            "description",
            "shop",
            "location",
            "price",
            "discount",
            "category",
            "stock",
            "is_available",
            "picture",
            "is_delete",
            "_links",
        ]
        read_only_fields = ["id", "is_delete", "_links"]

    def get__links(self, obj):
        request = self.context.get("request")
        if not request:
            base_url = "http://localhost:8000"
        else:
            base_url = f"{request.scheme}://{request.get_host()}"

        return [
            {
                "rel": "self",
                "href": f"{base_url}/products",
                "action": "POST",
                "types": ["application/json"],
            },
            {
                "rel": "self",
                "href": f"{base_url}/products/{obj.id}/",
                "action": "GET",
                "types": ["application/json"],
            },
            {
                "rel": "self",
                "href": f"{base_url}/products/{obj.id}/",
                "action": "PUT",
                "types": ["application/json"],
            },
            {
                "rel": "self",
                "href": f"{base_url}/products/{obj.id}/",
                "action": "DELETE",
                "types": ["application/json"],
            },
        ]

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be a positive integer.")
        return value

    def validate_discount(self, value):
        if value < 0:
            raise serializers.ValidationError("Discount must be a positive integer.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock must be a positive integer.")
        return value

    def validate_sku(self, value):
        if not value.strip():
            raise serializers.ValidationError("SKU cannot be blank.")
        return value

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be blank.")
        return value


class ProductListSerializer(serializers.ModelSerializer):
    _links = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "sku",
            "description",
            "shop",
            "location",
            "price",
            "discount",
            "category",
            "stock",
            "is_available",
            "picture",
            "is_delete",
            "_links",
        ]

    def get__links(self, obj):
        request = self.context.get("request")
        if not request:
            base_url = "http://localhost:8000"
        else:
            base_url = f"{request.scheme}://{request.get_host()}"

        return [
            {
                "rel": "self",
                "href": f"{base_url}/products",
                "action": "POST",
                "types": ["application/json"],
            },
            {
                "rel": "self",
                "href": f"{base_url}/products/{obj.id}/",
                "action": "GET",
                "types": ["application/json"],
            },
            {
                "rel": "self",
                "href": f"{base_url}/products/{obj.id}/",
                "action": "PUT",
                "types": ["application/json"],
            },
            {
                "rel": "self",
                "href": f"{base_url}/products/{obj.id}/",
                "action": "DELETE",
                "types": ["application/json"],
            },
        ]
