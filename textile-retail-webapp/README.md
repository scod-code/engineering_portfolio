# ASAA Fashion & Beauty House

A modern e-commerce platform for fashion and beauty products, built with React + Vite (frontend) and FastAPI (backend), with MongoDB for data persistence.

## 🌐 Live Website

**Access the live application here:** **[https://textile-retail.vercel.app/](https://textile-retail.vercel.app/)**

**Vercel Project:** [https://vercel.com/asaafashion/textile-retail](https://vercel.com/asaafashion/textile-retail)

## Overview

This is a full-stack application combining:
- **Frontend**: React with Vite, Tailwind CSS, and React Router
- **Backend**: FastAPI with MongoDB, JWT authentication, and file storage
- **Database**: MongoDB Atlas (cloud) or local MongoDB
- **Deployment**: Render (backend) + Netlify/Vercel (frontend)

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    React Frontend                        │
│  (Vite + React Router + Tailwind CSS)                   │
│  • Storefront.jsx - Product browsing & purchasing       │
│  • Admin.jsx - Product management                       │
│  • AuthModal.jsx - Login/Register modal                 │
│  • ProductModal.jsx - Product details modal             │
└──────────────────┬──────────────────────────────────────┘
                   │ API Calls (axios)
                   ▼
┌─────────────────────────────────────────────────────────┐
│              FastAPI Backend (main.py)                   │
│  • RESTful API endpoints                                │
│  • JWT authentication with httpOnly cookies             │
│  • Product CRUD operations (admin only)                 │
│  • Order management                                     │
│  • File uploads (local, GitHub, Google Drive)           │
└──────────────────┬──────────────────────────────────────┘
                   │ Database queries (motor)
                   ▼
        ┌─────────────────────────┐
        │   MongoDB Database      │
        │  • Products collection  │
        │  • Customers collection │
        │  • Orders collection    │
        └─────────────────────────┘
```

## Core Features

| Feature | Implementation |
|---------|-----------------|
| **Product Browsing** | Storefront with category filters, search, responsive grid |
| **Product Details** | Modal with images, sizes, colors, pricing, stock info |
| **User Authentication** | Registration, login, role-based access (customer/admin) |
| **Shopping Cart & Orders** | Add to cart, checkout, order history |
| **Admin Dashboard** | CRUD operations for products with image upload support |
| **Image Management** | Upload from local filesystem, GitHub, Google Drive, or URL |
| **Responsive Design** | Mobile, tablet, and desktop support with Tailwind CSS |
| **Security** | JWT tokens in secure cookies, PBKDF2 password hashing, CORS |

## Project Structure

```
.
├── frontend/                    # React + Vite application
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Storefront.jsx  # Main shopping interface
│   │   │   └── Admin.jsx        # Admin product management
│   │   ├── components/
│   │   │   ├── AuthModal.jsx   # Login/Register modal
│   │   │   └── ProductModal.jsx # Product details modal
│   │   ├── App.jsx              # Main app routing
│   │   ├── App.css              # Tailwind styles
│   │   ├── index.css            # Base styles
│   │   └── main.jsx             # React entry point
│   ├── public/                  # Static assets
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── netlify.toml             # Netlify deployment config
│   └── vercel.json              # Vercel deployment config
│
├── backend/                     # FastAPI application
│   ├── main.py                  # API endpoints & middleware
│   ├── models.py                # Pydantic data models
│   ├── database.py              # MongoDB connection
│   ├── auth.py                  # JWT & password utilities
│   ├── config.py                # Configuration loader
│   ├── image_storage.py         # Image storage handlers
│   ├── local_store.py           # Local file storage
│   ├── seed_products.py         # Sample product data
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Configuration (not committed)
│
├── frontend_legacy/             # Legacy HTML/CSS version (archived)
│   ├── index.html
│   └── admin.html
│
├── README.md                    # This file
├── COMPLETION_SUMMARY.md        # Implementation details
├── DEPLOY.txt                   # Production deployment guide
├── start.ps1                    # PowerShell startup script
├── requirements.txt             # Root-level Python deps
└── main.py                      # Root entry point
```

## API Endpoints

### Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| POST | `/api/register` | Register new customer account | ✗ |
| POST | `/api/login` | Login and get JWT token | ✗ |
| POST | `/api/logout` | Logout and clear token | ✓ |
| GET | `/api/me` | Get current user info | ✓ |

### Admin Setup
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| POST | `/api/admin-setup` | Initial admin account setup | ✗ (requires SECRET_KEY) |

### Products
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| GET | `/api/products` | List all products | ✗ |
| GET | `/api/products/{id}` | Get product details | ✗ |
| POST | `/api/products` | Create new product | ✓ Admin |
| PUT | `/api/products/{id}` | Update product | ✓ Admin |
| DELETE | `/api/products/{id}` | Delete product | ✓ Admin |
| POST | `/api/upload-image` | Upload product image | ✓ Admin |

### Orders
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| GET | `/api/orders` | Get user's orders | ✓ |
| POST | `/api/orders` | Create new order | ✓ |

### Health & Info
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|----------------|
| GET | `/api/health` | API health check | ✗ |
| GET | `/healthz` | Render deployment health check | ✗ |

## Data Models

### Product
```javascript
{
  "_id": ObjectId,
  "name": string,
  "description": string,
  "price": float,
  "sale_price": float (optional),
  "category": string,  // "Clothing", "Footwear", "Accessories", "Beauty"
  "sku": string (optional),
  "images": [string],  // URLs
  "sizes": [string] (optional),
  "colours": [string] (optional),
  "stock": int,
  "materials": string (optional),
  "tags": [string] (optional)
}
```

### Customer
```javascript
{
  "_id": ObjectId,
  "name": string,
  "email": string (unique),
  "password": string (hashed),
  "role": "customer" | "admin",
  "joined": datetime
}
```

### Order
```javascript
{
  "_id": ObjectId,
  "customer_id": ObjectId,
  "product_name": string,
  "price": float,
  "size": string (optional),
  "colour": string (optional),
  "quantity": int,
  "created_at": datetime
}
```

## Admin Access

Admin and customer accounts are completely separate.

1. **First Time Setup**:
   - Navigate to `/admin.html`
   - Click "Set up admin"
   - Enter name, email, password, and the server's `SECRET_KEY` (from `.env`)

2. **Regular Admin Login**:
   - Go to `/admin.html`
   - Enter your admin email and password
   - Access full product CRUD operations

**Note**: Regular customers cannot perform admin operations. The API enforces role-based access control.

## Security Features

- **Password Hashing**: PBKDF2-HMAC-SHA256 using Python's standard library
- **Authentication**: JWT tokens stored in secure httpOnly cookies
- **Authorization**: Role-based access control (customer vs admin)
- **Admin Setup**: Requires SECRET_KEY to prevent unauthorized admin creation
- **CORS**: Configured for allowed origins only
- **Environment Variables**: All secrets loaded from `.env` file (not committed)

---

<details>
<summary><strong>Local Development Setup</strong></summary>

If you need to run the project locally for development, you can use the startup scripts:
```powershell
.\start.ps1
```
Or double-click `start.bat`.

Alternatively, set things up manually:

```powershell
# 1. Create virtual environment
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Configure environment
copy .env.example .env
# Edit .env with your MongoDB URL and secret key

# 3. Seed products (optional)
python seed_products.py

# 4. Start the server
uvicorn main:app --reload --host 127.0.0.1 --port 8000

# 5. Open http://127.0.0.1:8000 in your browser
```

</details>
