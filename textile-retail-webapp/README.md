# ASAA Fashion & Beauty House

A luxury fashion and beauty e-commerce website with product management, user authentication, orders, and an admin dashboard.

## Status

**The website is now published and live!** Access it here: **[https://asaa-fashion.onrender.com/](https://asaa-fashion.onrender.com/)**

*Note: If you are looking to run the local development environment or make further changes, refer to the **Developer Setup** section below.*

## Architecture

```
Browser -> https://asaa-fashion.onrender.com/

  FastAPI (backend/main.py)
  serves BOTH the API and the website

  MongoDB Atlas (or local MongoDB)
```

One server, one URL. The backend serves the frontend pages alongside the API.

## Features

| Feature | Description |
|---------|-------------|
| **M&S-style Storefront** | Product browsing with category/filter tabs, dynamic detail modals, responsive grid |
| **Product Catalogue** | Rich models supporting SKU, sale prices, sizes, colours, stock, SEO tags, materials |
| **Image Uploads** | Integrated storage supporting local filesystem, GitHub, Google Drive, and URLs |
| **Authentication** | Separated Admin and Customer roles, JWT cookies, standard library hashing |
| **Orders** | Place orders and view purchase history |
| **Admin Dashboard** | Tabbed admin form with secure key access for full product CRUD operations |
| **Product Categories** | Clothing, Footwear, Accessories, Beauty |
| **Health Check** | API monitoring at `/api/health` |

## Project Structure

```
 backend/
    main.py             # API routes + serves frontend
    database.py         # MongoDB connection
    auth.py             # JWT authentication
    models.py           # Data models
    seed_products.py    # Sample product data
    requirements.txt    # Python dependencies
    .env                # Your config (not committed)
 frontend/
    index.html          # Main storefront
    admin.html          # Admin dashboard
 start.ps1               # Run this to start everything
 DEPLOY.txt              # Production deployment guide
```

## Admin Access

Customer accounts and admin accounts are strictly separated.

1. Navigate to the live website's `/admin.html` page.
2. If setting up for the first time on a new database, click **Set up admin**.
3. Enter your name, email, password, and the server's `SECRET_KEY` (configured in the environment variables) as the setup key.
4. After that, use that admin email/password to sign in to `/admin.html`.

Normal customers can register, sign in, buy products, and view their orders, but they cannot create, edit, or delete products. Product management routes require an authenticated account with `role: "admin"`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/healthz` | Render health check |
| POST | `/api/register` | User registration |
| POST | `/api/login` | User login |
| POST | `/api/logout` | User logout |
| GET | `/api/me` | Current user info |
| GET | `/api/products` | List all products |
| POST | `/api/products` | Create product (admin) |
| GET | `/api/products/{id}` | Get product details |
| PUT | `/api/products/{id}` | Update product (admin) |
| DELETE | `/api/products/{id}` | Delete product (admin) |
| GET | `/api/orders` | User's orders |
| POST | `/api/orders` | Place new order |

## Deployment

See `DEPLOY.txt` for production deployment to Render + MongoDB Atlas. The backend serves the frontend, so this project can deploy as one web service.

## Security

- Passwords hashed with PBKDF2-HMAC-SHA256
- JWT tokens in httpOnly cookies
- Admin actions require secret key
- CORS configured for allowed origins
- Environment variables for all secrets

---

<details>
<summary><strong>Developer Setup (Local)</strong></summary>

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
