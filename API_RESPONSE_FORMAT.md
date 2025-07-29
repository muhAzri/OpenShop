# API Standardized Response Format

This document describes the standardized response format used across all OpenShop API endpoints for consistent frontend integration.

## Response Structure

All API responses follow this consistent structure:

```json
{
  "success": boolean,
  "status_code": integer,
  "message": string,
  "data": object|array|null,
  "errors": object|null
}
```

### Field Descriptions

- **`success`**: Boolean indicating if the request was successful (`true`) or failed (`false`)
- **`status_code`**: HTTP status code (200, 201, 400, 404, 500, etc.)
- **`message`**: Human-readable message describing the result
- **`data`**: Response payload (varies by endpoint, `null` for errors)
- **`errors`**: Validation or error details (`null` for successful requests)

## Response Types

### 1. Success Responses

#### GET /products/ (Success with data)
```json
{
  "success": true,
  "status_code": 200,
  "message": "Retrieved 3 product(s) successfully",
  "data": {
    "products": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Laptop Gaming ASUS",
        "sku": "ASUS-001",
        // ... other product fields
      }
    ]
  },
  "errors": null
}
```

#### GET /products/:id/ (Single product)
```json
{
  "success": true,
  "status_code": 200,
  "message": "Product retrieved successfully",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Laptop Gaming ASUS",
    "sku": "ASUS-001",
    // ... other product fields
  },
  "errors": null
}
```

#### POST /products/ (Creation)
```json
{
  "success": true,
  "status_code": 201,
  "message": "Product created successfully",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "New Product",
    // ... other product fields
  },
  "errors": null
}
```

#### PUT /products/:id/ (Update)
```json
{
  "success": true,
  "status_code": 200,
  "message": "Product updated successfully",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Updated Product Name",
    // ... other updated fields
  },
  "errors": null
}
```

#### DELETE /products/:id/ (Deletion)
```json
{
  "success": true,
  "status_code": 200,
  "message": "Product deleted successfully",
  "data": {
    "deleted_id": "550e8400-e29b-41d4-a716-446655440000"
  },
  "errors": null
}
```

### 2. Empty Data Responses

#### GET /products/ (No products available)
```json
{
  "success": true,
  "status_code": 200,
  "message": "No products available",
  "data": [],
  "errors": null
}
```

#### GET /products/?name=search (No search results)
```json
{
  "success": true,
  "status_code": 200,
  "message": "No products found matching name='search'",
  "data": [],
  "errors": null
}
```

#### GET /products/?name=laptop&location=jakarta (Combined search, no results)
```json
{
  "success": true,
  "status_code": 200,
  "message": "No products found matching name='laptop' and location='jakarta'",
  "data": [],
  "errors": null
}
```

### 3. Error Responses

#### 404 Not Found
```json
{
  "success": false,
  "status_code": 404,
  "message": "Product not found",
  "data": null,
  "errors": null
}
```

#### 400 Validation Error
```json
{
  "success": false,
  "status_code": 400,
  "message": "Product creation failed due to validation errors",
  "data": null,
  "errors": {
    "name": ["This field may not be blank."],
    "price": ["Price must be a positive integer."],
    "sku": ["This field is required."]
  }
}
```

#### 500 Server Error
```json
{
  "success": false,
  "status_code": 500,
  "message": "Internal server error",
  "data": null,
  "errors": null
}
```

## Frontend Integration Benefits

### Easy Status Checking
```javascript
// Check if request was successful
if (response.success) {
  console.log("Success:", response.message);
  handleData(response.data);
} else {
  console.log("Error:", response.message);
  handleErrors(response.errors);
}
```

### Consistent Error Handling
```javascript
function handleApiResponse(response) {
  switch (response.status_code) {
    case 200:
    case 201:
      return { success: true, data: response.data, message: response.message };
    case 400:
      return { success: false, errors: response.errors, message: response.message };
    case 404:
      return { success: false, message: response.message };
    default:
      return { success: false, message: "Unexpected error occurred" };
  }
}
```

### TypeScript Interface
```typescript
interface ApiResponse<T = any> {
  success: boolean;
  status_code: number;
  message: string;
  data: T | null;
  errors: Record<string, string[]> | null;
}

// Usage examples
interface Product {
  id: string;
  name: string;
  sku: string;
  // ... other fields
}

type ProductListResponse = ApiResponse<{ products: Product[] }>;
type ProductDetailResponse = ApiResponse<Product>;
type ProductCreateResponse = ApiResponse<Product>;
```

### React Hook Example
```javascript
const useApiCall = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const apiCall = async (url, options) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(url, options);
      const data = await response.json();
      
      if (!data.success) {
        setError(data.message);
        return { success: false, errors: data.errors };
      }
      
      return { success: true, data: data.data };
    } catch (err) {
      setError("Network error occurred");
      return { success: false };
    } finally {
      setLoading(false);
    }
  };
  
  return { apiCall, loading, error };
};
```

## Status Code Mapping

| Status Code | Success | Description | Data | Errors |
|-------------|---------|-------------|------|---------|
| 200 | `true` | OK - Request successful | Present | `null` |
| 201 | `true` | Created - Resource created | Present | `null` |
| 400 | `false` | Bad Request - Validation failed | `null` | Present |
| 404 | `false` | Not Found - Resource not found | `null` | `null` |
| 500 | `false` | Server Error - Internal error | `null` | `null` |

## Message Patterns

### Success Messages
- `"Retrieved {count} product(s) successfully"`
- `"Product created successfully"`
- `"Product updated successfully"`
- `"Product deleted successfully"`
- `"Product retrieved successfully"`

### Empty Data Messages
- `"No products available"`
- `"No products found matching name='{query}'"`
- `"No products found matching location='{query}'"`
- `"No products found matching name='{name}' and location='{location}'"`

### Error Messages
- `"Product not found"`
- `"Product creation failed due to validation errors"`
- `"Product update failed due to validation errors"`
- `"Internal server error"`

## Advantages for Frontend Development

1. **Predictable Structure**: Every response has the same top-level structure
2. **Easy Error Handling**: Single point to check `success` field
3. **Consistent Messages**: User-friendly messages for all operations
4. **Type Safety**: Clear data types for TypeScript integration
5. **Debugging Friendly**: Status codes and messages for easy troubleshooting
6. **Flexible Data**: `data` field adapts to different response types
7. **Validation Feedback**: Detailed error information in `errors` field