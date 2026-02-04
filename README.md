# Sample FastAPI Application

A comprehensive sample FastAPI application demonstrating CRUD operations, data validation, and RESTful API best practices.

## Features

- ✨ **CRUD Operations** for Items and Users
- 🔒 **Data Validation** using Pydantic models
- 📊 **Statistics Endpoint** for application metrics
- 🏥 **Health Check** endpoint
- 📝 **Auto-generated API Documentation** (Swagger UI & ReDoc)
- 🌐 **CORS Support** for frontend integration
- ⚡ **Fast and Async** operations

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /home/lenovo/Pictures/fastapi-application
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Development Mode (with auto-reload)
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:
- **API**: http://localhost:8000
- **Swagger UI Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## API Endpoints

### Root & Health
- `GET /` - Welcome message
- `GET /health` - Health check endpoint

### Items
- `POST /items/` - Create a new item
- `GET /items/` - Get all items (with pagination)
- `GET /items/{item_id}` - Get a specific item
- `PUT /items/{item_id}` - Update an item
- `DELETE /items/{item_id}` - Delete an item

### Users
- `POST /users/` - Create a new user
- `GET /users/` - Get all users (with pagination)
- `GET /users/{user_id}` - Get a specific user by ID
- `GET /users/username/{username}` - Get a user by username

### Statistics
- `GET /stats` - Get application statistics

## Example Usage

### Create an Item
```bash
curl -X POST "http://localhost:8000/items/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 999.99,
    "quantity": 10
  }'
```

### Get All Items
```bash
curl "http://localhost:8000/items/"
```

### Create a User
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "password": "securepassword123"
  }'
```

### Get Statistics
```bash
curl "http://localhost:8000/stats"
```

## Data Models

### Item
- `id`: Integer (auto-generated)
- `name`: String (1-100 characters)
- `description`: Optional String (max 500 characters)
- `price`: Float (must be positive)
- `quantity`: Integer (non-negative)
- `created_at`: DateTime
- `updated_at`: DateTime

### User
- `id`: Integer (auto-generated)
- `username`: String (3-50 characters)
- `email`: String (valid email format)
- `full_name`: Optional String
- `is_active`: Boolean (default: true)
- `created_at`: DateTime

## Project Structure

```
fastapi-application/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Notes

- This application uses in-memory storage for demonstration purposes
- Data will be lost when the application restarts
- For production use, integrate with a proper database (PostgreSQL, MySQL, MongoDB, etc.)
- Password hashing is not implemented in this sample (use libraries like `passlib` for production)

## Next Steps

To extend this application, consider:
- Adding database integration (SQLAlchemy, Tortoise ORM)
- Implementing authentication & authorization (JWT tokens)
- Adding more complex business logic
- Writing unit and integration tests
- Containerizing with Docker
- Setting up CI/CD pipelines

## License

This is a sample project for educational purposes.
