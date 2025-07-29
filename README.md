# OpenShop Products API

A RESTful API for product management built with Django REST Framework. This API provides comprehensive CRUD operations for e-commerce product management with features like soft delete, search functionality, and HATEOAS compliance.

## Features

### Core Functionality
- **Product Management**: Complete CRUD operations (Create, Read, Update, Delete)
- **Soft Delete**: Products are marked as deleted rather than permanently removed
- **Search Capabilities**: Search products by name and location with partial matching
- **UUID-based IDs**: Uses UUID4 for product identification
- **Data Validation**: Comprehensive field validation with detailed error messages
- **HATEOAS Support**: Hypermedia links for API discoverability

### Technical Features
- **Django REST Framework**: Built on industry-standard REST framework
- **SQLite Database**: Lightweight database for development and testing
- **Admin Interface**: Django admin panel for product management
- **API Documentation**: Postman collection for comprehensive testing
- **Proper HTTP Status Codes**: Correct status codes for all operations
- **Standardized Responses**: Consistent JSON response format for easy frontend integration
- **Frontend-Friendly**: Unified response structure with success flags and clear error handling

## API Endpoints

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `POST` | `/products/` | Create new product | 201, 400 |
| `GET` | `/products/` | List all products | 200 |
| `GET` | `/products/:id/` | Get product details | 200, 404 |
| `PUT` | `/products/:id/` | Update product | 200, 400, 404 |
| `DELETE` | `/products/:id/` | Soft delete product | 200, 404 |
| `GET` | `/products/?name=search` | Search by name | 200 |
| `GET` | `/products/?location=search` | Search by location | 200 |

## Data Model

### Product Fields
- `id` (UUID): Unique product identifier
- `name` (String): Product name (required)
- `sku` (String): Stock Keeping Unit (required, unique)
- `description` (Text): Product description
- `shop` (String): Shop/store name
- `location` (String): Product location
- `price` (Integer): Price in cents/smallest currency unit
- `discount` (Integer): Discount amount
- `category` (String): Product category
- `stock` (Integer): Available stock quantity
- `is_available` (Boolean): Product availability status
- `picture` (URL): Product image URL
- `is_delete` (Boolean): Soft delete flag
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

## Installation & Setup

### Prerequisites
- Python 3.9+
- pipenv (for dependency management)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd OpenShop
   ```

2. **Install dependencies**
   ```bash
   pipenv install
   ```

3. **Activate virtual environment**
   ```bash
   pipenv shell
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create admin user (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   # or using make
   make server
   ```

The API will be available at `http://localhost:8000`

## Code Quality & Formatting

### Code Formatting
This project uses Black and isort for consistent code formatting:

```bash
# Format code automatically
make format

# Check formatting without changes
make format-check

# Run all linting checks
make lint
```

### Available Make Commands
```bash
make help              # Show all available commands
make install           # Install dependencies
make server            # Start development server
make migrate           # Apply database migrations
make makemigrations    # Create new migrations
make superuser         # Create admin user
make test              # Run tests
make format            # Format code with black and isort
make format-check      # Check code formatting
make lint              # Run all linting checks
make clean             # Clean Python cache files
make check             # Check for Django issues
```

## Usage Examples

### Create Product
```bash
curl -X POST http://localhost:8000/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop Gaming ASUS",
    "sku": "ASUS-001",
    "description": "High performance gaming laptop",
    "shop": "Tech Store",
    "location": "Jakarta",
    "price": 15000000,
    "discount": 1000000,
    "category": "Electronics",
    "stock": 25,
    "is_available": true,
    "picture": "https://example.com/laptop.jpg"
  }'
```

### Get All Products
```bash
curl http://localhost:8000/products/
```

### Search Products
```bash
# Search by name
curl "http://localhost:8000/products/?name=laptop"

# Search by location
curl "http://localhost:8000/products/?location=jakarta"

# Combined search
curl "http://localhost:8000/products/?name=laptop&location=jakarta"
```

### Update Product
```bash
curl -X PUT http://localhost:8000/products/{product-id}/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Product Name",
    "price": 2000000
  }'
```

### Delete Product (Soft Delete)
```bash
curl -X DELETE http://localhost:8000/products/{product-id}/
```

## Standardized Response Format

All API responses follow a consistent structure for easy frontend integration:

```json
{
  "success": boolean,
  "status_code": integer,
  "message": string,
  "data": object|array|null,
  "errors": object|null
}
```

For detailed response format documentation, see [API_RESPONSE_FORMAT.md](API_RESPONSE_FORMAT.md).

## Response Examples

### Success Response (Product Created)
```json
{
  "success": true,
  "status_code": 201,
  "message": "Product created successfully",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Laptop Gaming ASUS",
    "sku": "ASUS-001",
    "description": "High performance gaming laptop",
    "shop": "Tech Store", 
    "location": "Jakarta",
    "price": 15000000,
    "discount": 1000000,
    "category": "Electronics",
    "stock": 25,
    "is_available": true,
    "picture": "https://example.com/laptop.jpg",
    "is_delete": false,
    "_links": [...]
  },
  "errors": null
}
```

### Products List Response
```json
{
  "success": true,
  "status_code": 200,
  "message": "Retrieved 2 product(s) successfully",
  "data": {
    "products": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Laptop Gaming ASUS",
        "sku": "ASUS-001",
        // ... other product fields
        "_links": [...]
      }
    ]
  },
  "errors": null
}
```

### Error Response (Validation)
```json
{
  "success": false,
  "status_code": 400,
  "message": "Product creation failed due to validation errors",
  "data": null,
  "errors": {
    "name": ["This field is required."],
    "price": ["Price must be a positive integer."]
  }
}
```

### Error Response (Not Found)
```json
{
  "success": false,
  "status_code": 404,
  "message": "Product not found",
  "data": null,
  "errors": null
}
```

### Empty Search Results
```json
{
  "success": true,
  "status_code": 200,
  "message": "No products found matching name='search'",
  "data": [],
  "errors": null
}
```

## Admin Interface

Access the Django admin interface at `http://localhost:8000/admin/`

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`

### Admin Features
- View all products in organized table format
- Search products by name, SKU, description, shop, location
- Filter products by availability, category, shop, location
- Inline editing for stock, price, discount, availability
- Bulk soft delete operations
- Organized fieldsets for better data entry

## Testing

### Postman Collection
Import the provided Postman collection for comprehensive API testing:
- `OpenShop Products API.postman_collection.json`

### Test Coverage
The Postman collection includes tests for:
- ✅ All CRUD operations
- ✅ Data validation scenarios
- ✅ Error handling (400, 404)
- ✅ Search functionality
- ✅ HATEOAS link validation
- ✅ Soft delete verification

### Manual Testing
```bash
# Test server health
curl http://localhost:8000/products/

# Test invalid UUID handling
curl http://localhost:8000/products/invalid-id/

# Test validation errors
curl -X POST http://localhost:8000/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "", "price": -100}'
```

## Project Structure

```
OpenShop/
├── OpenShop/                 # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Main settings
│   ├── urls.py              # URL routing
│   └── wsgi.py
├── products/                 # Products app
│   ├── __init__.py
│   ├── admin.py             # Admin configuration
│   ├── models.py            # Product model
│   ├── serializers.py       # DRF serializers
│   ├── urls.py              # App URL patterns
│   └── views.py             # API views
├── manage.py                 # Django management script
├── Pipfile                   # Dependencies
├── Pipfile.lock             # Locked dependencies
└── README.md                # This file
```

## Dependencies

### Core Dependencies
- `Django 4.2.23`: Web framework
- `djangorestframework`: REST API framework

### Development Dependencies
- `requests`: For API testing scripts
- `black`: Python code formatter
- `isort`: Import statement organizer

## Configuration

### Environment Variables
The application uses Django's default settings. For production deployment, consider configuring:
- `DEBUG = False`
- `ALLOWED_HOSTS` with your domain
- Database configuration (PostgreSQL recommended)
- Secret key management

### Database
Currently configured with SQLite for development. The database file `db.sqlite3` is created automatically when running migrations.

## API Design Principles

### RESTful Design
- Uses appropriate HTTP methods (GET, POST, PUT, DELETE)
- Proper HTTP status codes
- Resource-based URLs
- JSON content type

### HATEOAS Implementation
All product responses include `_links` array with:
- Self-referential links
- Related action links (GET, PUT, DELETE)
- Proper HTTP methods and content types

### Soft Delete Pattern
- Products are never permanently deleted
- `is_delete` flag marks deleted products
- Deleted products are filtered from all GET requests
- Admin interface can restore deleted products

## Limitations & Future Enhancements

### Current Limitations
- Single product model (no categories, variants)
- Basic search (no full-text search, filters)
- No authentication/authorization
- No pagination for large datasets
- No image upload handling
- No inventory tracking beyond stock count

### Potential Enhancements
- User authentication and permissions
- Advanced search with filters
- Image upload and management
- Product categories and tags
- Inventory management system
- Order management integration
- API rate limiting
- Caching for better performance
- Real-time stock updates
- Bulk operations support

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow Django/DRF best practices
- Add tests for new features
- Update API documentation
- Maintain backwards compatibility
- Use semantic commit messages

## License

This project is available for educational and development purposes.

## Support

For questions or issues:
1. Check the Postman collection for API usage examples
2. Review the Django admin interface for data management
3. Examine the code structure for implementation details

---

**Note**: This is a development project focused on demonstrating RESTful API design with Django REST Framework. For production use, additional security, scalability, and monitoring considerations should be implemented.