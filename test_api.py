#!/usr/bin/env python3
import json
import requests

BASE_URL = "http://localhost:8001"

def test_create_product():
    """Test POST /products"""
    print("Testing POST /products...")
    
    data = {
        "name": "Kelas Belajar Python",
        "sku": "DCD01",
        "description": "This is a sample description of the product.",
        "shop": "Dicoding",
        "location": "Bandung",
        "price": 1500000,
        "discount": 0,
        "category": "Course",
        "stock": 1000,
        "is_available": True,
        "picture": "https://www.shutterstock.com/image-vector/sample-red-square-grunge-stamp-260nw-338250266.jpg"
    }
    
    response = requests.post(f"{BASE_URL}/products/", json=data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 201:
        result = response.json()
        print("✅ Product created successfully")
        print(json.dumps(result, indent=2))
        return result['id']
    else:
        print("❌ Failed to create product")
        print(response.text)
        return None

def test_get_products():
    """Test GET /products"""
    print("\nTesting GET /products...")
    
    response = requests.get(f"{BASE_URL}/products/")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Products retrieved successfully")
        print(json.dumps(result, indent=2))
        return result.get('products', [])
    else:
        print("❌ Failed to get products")
        print(response.text)
        return []

def test_get_product_detail(product_id):
    """Test GET /products/{id}"""
    print(f"\nTesting GET /products/{product_id}/...")
    
    response = requests.get(f"{BASE_URL}/products/{product_id}/")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Product detail retrieved successfully")
        print(json.dumps(result, indent=2))
        return result
    else:
        print("❌ Failed to get product detail")
        print(response.text)
        return None

def test_update_product(product_id):
    """Test PUT /products/{id}"""
    print(f"\nTesting PUT /products/{product_id}/...")
    
    data = {
        "name": "Kelas Belajar Python Dasar",
        "sku": "DCD02",
        "description": "This is a updated sample description of the product.",
        "shop": "Dicoding Academy",
        "location": "Indonesia",
        "price": 1200000,
        "discount": 300000,
        "category": "Bootcamp",
        "stock": 500,
        "is_available": True,
        "picture": "https://www.shutterstock.com/image-vector/sample-red-square-grunge-stamp-260nw-338250266.jpg"
    }
    
    response = requests.put(f"{BASE_URL}/products/{product_id}/", json=data)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Product updated successfully")
        print(json.dumps(result, indent=2))
        return result
    else:
        print("❌ Failed to update product")
        print(response.text)
        return None

def test_search_products():
    """Test GET /products?name=Python"""
    print("\nTesting GET /products?name=Python...")
    
    response = requests.get(f"{BASE_URL}/products/?name=Python")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Product search successful")
        print(json.dumps(result, indent=2))
        return result
    else:
        print("❌ Failed to search products")
        print(response.text)
        return None

def test_delete_product(product_id):
    """Test DELETE /products/{id}"""
    print(f"\nTesting DELETE /products/{product_id}/...")
    
    response = requests.delete(f"{BASE_URL}/products/{product_id}/")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 204:
        print("✅ Product deleted successfully (soft delete)")
        return True
    else:
        print("❌ Failed to delete product")
        print(response.text)
        return False

def test_404_error():
    """Test 404 error for non-existent product"""
    print("\nTesting 404 error...")
    
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = requests.get(f"{BASE_URL}/products/{fake_id}/")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 404:
        result = response.json()
        print("✅ 404 error handled correctly")
        print(json.dumps(result, indent=2))
        return True
    else:
        print("❌ 404 error not handled correctly")
        print(response.text)
        return False

def main():
    print("🚀 Starting API Tests...\n")
    
    # Test create product
    product_id = test_create_product()
    if not product_id:
        print("Cannot continue tests without a product ID")
        return
    
    # Test get all products
    test_get_products()
    
    # Test get product detail
    test_get_product_detail(product_id)
    
    # Test update product
    test_update_product(product_id)
    
    # Test search products
    test_search_products()
    
    # Test 404 error
    test_404_error()
    
    # Test delete product (soft delete)
    test_delete_product(product_id)
    
    # Verify product is soft deleted
    print(f"\nVerifying product {product_id} is soft deleted...")
    response = requests.get(f"{BASE_URL}/products/{product_id}/")
    if response.status_code == 404:
        print("✅ Soft delete working correctly - product no longer accessible")
    else:
        print("❌ Soft delete not working - product still accessible")
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    main()