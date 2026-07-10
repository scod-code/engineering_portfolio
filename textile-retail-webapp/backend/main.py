from fastapi import FastAPI, Response, Depends, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from bson import ObjectId
from datetime import datetime
from pathlib import Path
from pymongo.errors import PyMongoError
import os
import asyncio
from typing import Optional

from .database import customers_collection, orders_collection, products_collection
from .models import AdminSetup, CustomerRegister, CustomerLogin, OrderCreate, ProductIn, ProductOut
from .auth import hash_password, verify_password, create_access_token, get_current_user
from . import local_store
from .config import load_app_env
from .image_storage import get_image_storage, convert_gdrive_url

load_app_env()

app = FastAPI(title="ASAA Fashion & Beauty House API", version="2.0.0")


def _csv_env(name: str, default: str = "") -> list[str]:
    """Read a comma-separated environment variable into a clean list."""
    return [value.strip().rstrip("/") for value in os.getenv(name, default).split(",") if value.strip()]


FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5500").rstrip("/")
ALLOWED_ORIGINS = list(dict.fromkeys([
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    FRONTEND_URL,
    *_csv_env("ALLOWED_ORIGINS"),
]))

COOKIE_SECURE = os.getenv("COOKIE_SECURE", "").lower() in {"1", "true", "yes"} or FRONTEND_URL.startswith("https://")
COOKIE_SAMESITE = os.getenv("COOKIE_SAMESITE", "none" if COOKIE_SECURE else "lax").lower()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===================================================================
# ADMIN ROLE GUARD
# ===================================================================

async def require_admin(user: dict = Depends(get_current_user)) -> dict:
    if _is_local_user(user):
        customer = await local_store.get_customer(_local_id(user))
        if not customer:
            raise HTTPException(status_code=401, detail="Admin session not found. Please sign in again.")
        if customer.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Admin access required")
        return {"id": customer["id"], "name": customer["name"], "email": customer["email"], "role": "admin"}

    if not ObjectId.is_valid(user["sub"]):
        raise HTTPException(status_code=401, detail="Session invalid. Please log in again.")

    try:
        customer = await _db_wait(customers_collection.find_one({"_id": ObjectId(user["sub"])}))
    except (asyncio.TimeoutError, PyMongoError, OSError) as exc:
        _raise_database_unavailable(exc)

    if not customer:
        raise HTTPException(status_code=401, detail="Admin session not found. Please sign in again.")
    if customer.get("role", "customer") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return {"id": str(customer["_id"]), "name": customer["name"], "email": customer["email"], "role": "admin"}


# ===================================================================
# AUTH ROUTES
# ===================================================================

@app.post("/api/register")
async def register(data: CustomerRegister, response: Response):
    customer_doc = {
        "name": data.name,
        "email": data.email,
        "password": hash_password(data.password),
        "role": "customer",
        "joined": datetime.utcnow(),
    }

    try:
        existing = await _db_wait(customers_collection.find_one({"email": data.email}))
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        result = await _db_wait(customers_collection.insert_one(customer_doc))
        customer_id = str(result.inserted_id)
    except HTTPException:
        raise
    except (asyncio.TimeoutError, PyMongoError, OSError) as exc:
        print(f"Database unavailable, using local account store: {exc}")
        existing = await local_store.find_customer_by_email(data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        customer_id = f"local:{await local_store.insert_customer(customer_doc)}"

    token = create_access_token({"sub": customer_id, "email": data.email})
    _set_auth_cookie(response, token)
    return {"message": "Account created", "name": data.name, "role": "customer", "is_admin": False}


@app.post("/api/login")
async def login(data: CustomerLogin, response: Response):
    try:
        customer = await _db_wait(customers_collection.find_one({"email": data.email}))
        customer_id = str(customer["_id"]) if customer else None
    except (asyncio.TimeoutError, PyMongoError, OSError) as exc:
        print(f"Database unavailable, using local account store: {exc}")
        customer = await local_store.find_customer_by_email(data.email)
        customer_id = f"local:{customer['id']}" if customer else None

    if not customer or not verify_password(data.password, customer["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": customer_id, "email": data.email})
    _set_auth_cookie(response, token)

    role = customer.get("role", "customer")
    return {
        "message": "Logged in",
        "name": customer["name"],
        "email": customer["email"],
        "role": role,
        "is_admin": role == "admin",
    }


@app.post("/api/admin/setup")
async def setup_admin(data: AdminSetup, response: Response):
    if data.admin_key != os.getenv("SECRET_KEY"):
        raise HTTPException(status_code=401, detail="Invalid admin setup key")

    admin_doc = {
        "name": data.name,
        "email": data.email,
        "password": hash_password(data.password),
        "role": "admin",
        "joined": datetime.utcnow(),
    }

    try:
        existing = await _db_wait(customers_collection.find_one({"email": data.email}))
        if existing:
            await _db_wait(customers_collection.update_one(
                {"_id": existing["_id"]},
                {"$set": {"name": data.name, "password": admin_doc["password"], "role": "admin"}},
            ))
            admin_id = str(existing["_id"])
        else:
            result = await _db_wait(customers_collection.insert_one(admin_doc))
            admin_id = str(result.inserted_id)
    except (asyncio.TimeoutError, PyMongoError, OSError) as exc:
        print(f"Database unavailable, using local admin store: {exc}")
        admin_id = f"local:{await local_store.upsert_admin(admin_doc)}"

    token = create_access_token({"sub": admin_id, "email": data.email})
    _set_auth_cookie(response, token)
    return {"message": "Admin account ready", "name": data.name, "email": data.email, "role": "admin", "is_admin": True}


@app.get("/api/admin/me")
async def get_admin_me(admin: dict = Depends(require_admin)):
    return {"id": admin["id"], "name": admin["name"], "email": admin["email"], "role": "admin", "is_admin": True}


@app.post("/api/logout")
async def logout(response: Response):
    response.delete_cookie("access_token", path="/", secure=COOKIE_SECURE, samesite=COOKIE_SAMESITE)
    return {"message": "Logged out"}


@app.get("/api/me")
async def get_me(user: dict = Depends(get_current_user)):
    if _is_local_user(user):
        customer = await local_store.get_customer(_local_id(user))
        if not customer:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "id": customer["id"],
            "name": customer["name"],
            "email": customer["email"],
            "role": customer.get("role", "customer"),
            "is_admin": customer.get("role") == "admin",
            "joined": customer["joined"],
        }

    if not ObjectId.is_valid(user["sub"]):
        raise HTTPException(status_code=401, detail="Session invalid. Please log in again.")

    try:
        customer = await _db_wait(customers_collection.find_one({"_id": ObjectId(user["sub"])}))
    except (asyncio.TimeoutError, PyMongoError, OSError) as exc:
        _raise_database_unavailable(exc)
    if not customer:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": str(customer["_id"]),
        "name": customer["name"],
        "email": customer["email"],
        "role": customer.get("role", "customer"),
        "is_admin": customer.get("role") == "admin",
        "joined": customer["joined"].isoformat(),
    }


# ===================================================================
# ORDERS ROUTES
# ===================================================================

@app.post("/api/orders")
async def place_order(data: OrderCreate, user: dict = Depends(get_current_user)):
    order_doc = {
        "customer_id": _local_id(user) if _is_local_user(user) else user["sub"],
        "product_id": data.product_id,
        "product_name": data.product_name,
        "price": data.price,
        "size": data.size,
        "colour": data.colour,
        "quantity": data.quantity,
        "created_at": datetime.utcnow(),
    }
    if _is_local_user(user):
        order_id = await local_store.insert_order(order_doc)
        return {"order_id": order_id, "message": "Order placed successfully"}

    try:
        result = await _db_wait(orders_collection.insert_one(order_doc))
    except (asyncio.TimeoutError, PyMongoError, OSError) as exc:
        _raise_database_unavailable(exc)
    return {"order_id": str(result.inserted_id), "message": "Order placed successfully"}


@app.get("/api/orders")
async def get_my_orders(user: dict = Depends(get_current_user)):
    if _is_local_user(user):
        return await local_store.list_orders(_local_id(user))

    cursor = orders_collection.find({"customer_id": user["sub"]}).sort("created_at", -1)
    orders = []
    try:
        async for order in cursor:
            orders.append({
                "order_id": str(order["_id"]),
                "product_name": order["product_name"],
                "price": order["price"],
                "size": order.get("size"),
                "colour": order.get("colour"),
                "quantity": order.get("quantity", 1),
                "created_at": order["created_at"].isoformat(),
            })
    except (asyncio.TimeoutError, PyMongoError, OSError) as exc:
        _raise_database_unavailable(exc)
    return orders


# ===================================================================
# HEALTH CHECK
# ===================================================================

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "ASAA Fashion Beauty House API", "timestamp": datetime.utcnow().isoformat()}


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


# ===================================================================
# PRODUCTS ROUTES
# ===================================================================

def _serialize_product(p: dict) -> dict:
    """Convert a MongoDB or local-store product document to a JSON-safe dict."""
    return {
        "id": str(p.get("_id") or p.get("id")),
        "name": p.get("name"),
        "sku": p.get("sku"),
        "price": p.get("price"),
        "original_price": p.get("original_price"),
        "category": p.get("category", ""),
        "tags": p.get("tags") or [],
        "short_description": p.get("short_description", ""),
        "description": p.get("description", ""),
        "image_url": p.get("image_url", ""),
        "image_urls": p.get("image_urls") or [],
        "sizes": p.get("sizes") or [],
        "colours": p.get("colours") or [],
        "material": p.get("material", ""),
        "care_instructions": p.get("care_instructions", ""),
        "stock_count": p.get("stock_count"),
        "is_featured": p.get("is_featured", False),
        "is_active": p.get("is_active", True),
        # Legacy
        "emoji": p.get("emoji", ""),
    }


@app.get("/api/products")
async def list_products(
    category: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    featured: Optional[bool] = Query(None),
    active_only: bool = Query(True),
):
    async def load_from_database():
        query: dict = {}
        if active_only:
            query["is_active"] = {"$ne": False}
        if featured is True:
            query["is_featured"] = True
        if category:
            query["category"] = {"$regex": f"^{category}$", "$options": "i"}
        if tag:
            query["tags"] = tag.lower()
        if search:
            query["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"short_description": {"$regex": search, "$options": "i"}},
                {"description": {"$regex": search, "$options": "i"}},
            ]
        cursor = products_collection.find(query).sort([("is_featured", -1), ("name", 1)])
        items = []
        async for p in cursor:
            items.append(_serialize_product(p))
        return items

    try:
        items = await asyncio.wait_for(load_from_database(), timeout=4)
    except Exception as e:
        print(f"Database unavailable, using local product store: {e}")
        items = await local_store.list_products(
            category=category, tag=tag, search=search,
            featured_only=featured is True, active_only=active_only,
        )
    return items


@app.get("/api/products/{product_id}")
async def get_product(product_id: str):
    product = None
    try:
        if ObjectId.is_valid(product_id):
            product = await _db_wait(products_collection.find_one({"_id": ObjectId(product_id)}))
        if not product:
            product = await _db_wait(products_collection.find_one({"id": product_id}))
    except (asyncio.TimeoutError, PyMongoError, OSError) as exc:
        print(f"Database unavailable, using local product store: {exc}")
        product = await local_store.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return _serialize_product(product)


def _product_doc_from_data(data: ProductIn) -> dict:
    """Convert a ProductIn to a MongoDB document dict."""
    return {
        "name": data.name,
        "sku": data.sku,
        "price": data.price,
        "original_price": data.original_price,
        "category": data.category,
        "tags": [t.lower().strip() for t in (data.tags or [])],
        "short_description": data.short_description,
        "description": data.description,
        "image_url": data.image_url,
        "image_urls": data.image_urls or [],
        "sizes": data.sizes or [],
        "colours": data.colours or [],
        "material": data.material,
        "care_instructions": data.care_instructions,
        "stock_count": data.stock_count,
        "is_featured": data.is_featured,
        "is_active": data.is_active,
        "emoji": data.emoji,
    }


@app.post("/api/products")
async def create_product(data: ProductIn, admin: dict = Depends(require_admin)):
    """Create a new product. Requires an authenticated admin user."""
    doc = _product_doc_from_data(data)
    try:
        result = await _db_wait(products_collection.insert_one(doc))
        product_id = str(result.inserted_id)
    except (asyncio.TimeoutError, PyMongoError, OSError) as exc:
        print(f"Database unavailable, using local product store: {exc}")
        product_id = await local_store.create_product(doc)
    return {"id": product_id, "message": "Product created"}


@app.put("/api/products/{product_id}")
async def update_product(product_id: str, data: ProductIn, admin: dict = Depends(require_admin)):
    """Update an existing product by ObjectId or string `id` field."""
    query = {"_id": ObjectId(product_id)} if ObjectId.is_valid(product_id) else {"id": product_id}
    update_doc = _product_doc_from_data(data)
    try:
        result = await _db_wait(products_collection.update_one(query, {"$set": update_doc}))
        matched = result.matched_count > 0
    except (asyncio.TimeoutError, PyMongoError, OSError) as exc:
        print(f"Database unavailable, using local product store: {exc}")
        matched = await local_store.update_product(product_id, update_doc)
    if not matched:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product updated"}


@app.delete("/api/products/{product_id}")
async def delete_product(product_id: str, admin: dict = Depends(require_admin)):
    """Delete a product by ObjectId or string `id` field."""
    query = {"_id": ObjectId(product_id)} if ObjectId.is_valid(product_id) else {"id": product_id}
    try:
        result = await _db_wait(products_collection.delete_one(query))
        deleted = result.deleted_count > 0
    except (asyncio.TimeoutError, PyMongoError, OSError) as exc:
        print(f"Database unavailable, using local product store: {exc}")
        deleted = await local_store.delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}


# ===================================================================
# IMAGE UPLOAD ROUTE
# ===================================================================

@app.post("/api/products/{product_id}/images")
async def upload_product_image(
    product_id: str,
    file: UploadFile = File(None),
    url: Optional[str] = Query(None),
    admin: dict = Depends(require_admin),
):
    """
    Upload an image for a product.
    - If `file` is provided: uploads via the configured IMAGE_STORAGE backend (GitHub by default).
    - If `url` is provided: uses the URL directly (Google Drive links are auto-converted).
    - Returns { image_url: "..." } and updates the product record.
    """
    image_url: Optional[str] = None

    if url:
        # Auto-convert Google Drive share links
        converted = convert_gdrive_url(url)
        image_url = converted if converted else url

    elif file:
        allowed = {"image/jpeg", "image/png", "image/webp", "image/gif"}
        if file.content_type not in allowed:
            raise HTTPException(status_code=400, detail=f"Unsupported image type: {file.content_type}")
        if file.size and file.size > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Image must be under 10 MB")

        content = await file.read()
        storage = get_image_storage()
        try:
            image_url = await storage.upload(file.filename or "product.jpg", content, file.content_type)
        except RuntimeError as exc:
            raise HTTPException(status_code=500, detail=str(exc))

    else:
        raise HTTPException(status_code=400, detail="Provide either a file upload or a url query parameter.")

    # Update the product record in DB / local store
    query = {"_id": ObjectId(product_id)} if ObjectId.is_valid(product_id) else {"id": product_id}
    try:
        await _db_wait(products_collection.update_one(
            query,
            {"$set": {"image_url": image_url}, "$addToSet": {"image_urls": image_url}},
        ))
    except (asyncio.TimeoutError, PyMongoError, OSError):
        await local_store.update_product_image(product_id, image_url)

    return {"image_url": image_url, "message": "Image updated"}


# ===================================================================
# HELPER
# ===================================================================

def _set_auth_cookie(response: Response, token: str):
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE,
        max_age=60 * 60 * 24 * 7,
        path="/",
    )


async def _db_wait(operation, timeout: int = 5):
    return await asyncio.wait_for(operation, timeout=timeout)


def _is_local_user(user: dict) -> bool:
    return str(user.get("sub", "")).startswith("local:")


def _local_id(user: dict) -> str:
    return str(user["sub"]).split("local:", 1)[1]


def _raise_database_unavailable(exc: Exception):
    print(f"Database unavailable: {exc}")
    raise HTTPException(
        status_code=503,
        detail=(
            "Database is unavailable. Check that MongoDB is running, or resume your "
            "MongoDB Atlas cluster and confirm MONGO_URL in backend/.env."
        ),
    )


FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
