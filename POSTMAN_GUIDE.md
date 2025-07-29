# OpenShop API - Postman Collection Guide

This guide explains how to use the Postman collection to test all the OpenShop Products API endpoints.

## 📋 Collection Overview

The Postman collection includes comprehensive testing for:

### 🔧 Core CRUD Operations
- ✅ **CREATE** - POST /products/
- ✅ **READ** - GET /products/ and GET /products/:id/
- ✅ **UPDATE** - PUT /products/:id/
- ✅ **DELETE** - DELETE /products/:id/ (soft delete)

### 🔍 Search Functionality  
- ✅ Search by product name
- ✅ Search by location
- ✅ Combined name + location search
- ✅ Empty results handling

### ⚠️ Error Handling
- ✅ Validation errors (400)
- ✅ Not found errors (404)
- ✅ Success status codes (200, 201, 204)

## 🚀 Quick Start

### 1. Import Collection & Environment

1. **Import Collection**: Import `OpenShop_API.postman_collection.json`
2. **Import Environment**: Import `OpenShop_Environment.postman_environment.json`
3. **Select Environment**: Choose "OpenShop Development" environment

### 2. Start Django Server

```bash
# Using pipenv
export PATH="$PATH:$(python3 -m site --user-base)/bin"
pipenv run python manage.py runserver 8000

# Or if pipenv is in PATH
pipenv run python manage.py runserver 8000
```

### 3. Update Base URL (if needed)

If using a different port, update the `base_url` environment variable:
- Default: `http://localhost:8000`
- Alternative: `http://localhost:8001`

## 📝 Testing Workflow

### Recommended Test Sequence:

1. **🏗️ Setup Test Data**
   - Run requests in "Test Data Setup" folder
   - Creates 3 sample products for testing

2. **✨ Test CRUD Operations**
   - Create Product (Success) → Note the returned `id`
   - Update environment variable `product_id` with the returned UUID
   - Get All Products
   - Get Product Detail 
   - Update Product (Success)
   - Delete Product (Soft Delete)

3. **🔍 Test Search Functionality**
   - Search by Name: `?name=Python`
   - Search by Location: `?location=Jakarta`
   - Combined Search: `?name=Python&location=Bandung`
   - No Results: `?name=NonExistentProduct`

4. **⚠️ Test Error Scenarios**
   - Validation Errors (400)
   - Not Found Errors (404)

## 📊 Expected Response Formats

### Success Response (201 Created):
```json
{
  "id": "uuid-here",
  "name": "Product Name",
  "sku": "SKU123",
  "description": "Product description",
  "shop": "Shop Name",
  "location": "Location",
  "price": 1500000,
  "discount": 0,
  "category": "Category",
  "stock": 100,
  "is_available": true,
  "picture": "https://example.com/image.jpg",
  "is_delete": false,
  "_links": [
    {
      "rel": "self",
      "href": "http://localhost:8000/products",
      "action": "POST",
      "types": ["application/json"]
    },
    // ... more HATEOAS links
  ]
}
```

### Products List Response (200 OK):
```json
{
  "products": [
    // Array of product objects with HATEOAS links
  ]
}
```

### Error Response (400 Bad Request):
```json
{
  "name": ["This field may not be blank."],
  "price": ["Price must be a positive integer."]
}
```

### Error Response (404 Not Found):
```json
{
  "detail": "Not found."
}
```

## 🔧 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `base_url` | API base URL | `http://localhost:8000` |
| `product_id` | UUID for specific product tests | `uuid-string` |

## 💡 Tips for Testing

1. **🔄 Dynamic Product ID**: After creating a product, copy the returned `id` and paste it into the `product_id` environment variable

2. **🧪 Test Order**: Run validation error tests before success tests to avoid data conflicts

3. **🔍 Search Testing**: Create products with different names/locations first, then test search functionality

4. **🗑️ Soft Delete**: After deleting a product, verify it's no longer accessible via GET requests

5. **📊 HATEOAS Verification**: Check that all responses include proper `_links` arrays

## 🐛 Troubleshooting

### Common Issues:

1. **Connection Refused**: Make sure Django server is running on correct port
2. **404 on All Requests**: Check base_url in environment
3. **Validation Errors**: Review request body format and required fields
4. **Product Not Found**: Ensure product_id environment variable is set correctly

### Server Logs:
Monitor Django server logs for detailed error information:
```bash
# Server will show request logs
[29/Jul/2025 07:00:37] "POST /products/ HTTP/1.1" 201 919
[29/Jul/2025 07:00:37] "GET /products/ HTTP/1.1" 200 934
```

## 📁 Collection Structure

```
OpenShop Products API/
├── Products/
│   ├── Create Product (Success)
│   ├── Create Product (Validation Error)
│   ├── Get All Products
│   ├── Get Product Detail
│   ├── Get Product Detail (Not Found)
│   ├── Update Product (Success)
│   ├── Update Product (Validation Error)
│   ├── Update Product (Not Found)
│   ├── Delete Product (Soft Delete)
│   └── Delete Product (Not Found)
├── Search/
│   ├── Search Products by Name
│   ├── Search Products by Location
│   ├── Search Products by Name and Location
│   └── Search Products (No Results)
└── Test Data Setup/
    ├── Create Test Product 1
    ├── Create Test Product 2
    └── Create Test Product 3
```

## ✅ Validation Checklist

Use this checklist to ensure all features are working:

- [ ] ✅ POST /products/ returns 201 with UUID and HATEOAS links
- [ ] ✅ POST /products/ returns 400 for invalid data
- [ ] ✅ GET /products/ returns products array with HATEOAS
- [ ] ✅ GET /products/:id/ returns single product with HATEOAS
- [ ] ✅ GET /products/:id/ returns 404 for non-existent product
- [ ] ✅ PUT /products/:id/ returns 200 with updated data
- [ ] ✅ PUT /products/:id/ returns 400 for invalid data
- [ ] ✅ PUT /products/:id/ returns 404 for non-existent product
- [ ] ✅ DELETE /products/:id/ returns 204 (no content)
- [ ] ✅ DELETE /products/:id/ returns 404 for non-existent product
- [ ] ✅ Soft delete: deleted products no longer accessible via GET
- [ ] ✅ Search by name works with partial matches
- [ ] ✅ Search by location works with partial matches
- [ ] ✅ Combined search works correctly
- [ ] ✅ Empty search results return {"products": []}
- [ ] ✅ All responses include proper HATEOAS links

Happy Testing! 🎉