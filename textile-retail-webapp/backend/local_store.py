import asyncio
import json
import threading
from datetime import datetime
from pathlib import Path
from uuid import uuid4


DATA_FILE = Path(__file__).resolve().parent / ".local_data.json"
_LOCK = threading.Lock()


DEFAULT_PRODUCTS = [
    {
        "id": "local-product-1",
        "name": "Wool Trench Coat",
        "sku": "COAT-WOO-001",
        "price": 149.99,
        "original_price": None,
        "emoji": "🧥",
        "category": "Clothing",
        "tags": ["new-in", "bestseller"],
        "short_description": "A timeless wool trench coat for all seasons.",
        "description": "Crafted from premium wool blend fabric, this classic trench coat features a double-breasted front, belted waist, and notch lapels. Fully lined for warmth. An enduring wardrobe staple that pairs beautifully with everything from jeans to evening wear.",
        "image_url": "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=600&q=80",
        "image_urls": [],
        "sizes": ["XS", "S", "M", "L", "XL", "XXL"],
        "colours": ["Camel", "Navy", "Black"],
        "material": "70% Wool, 20% Polyamide, 10% Cashmere",
        "care_instructions": "Dry clean only. Do not tumble dry.",
        "stock_count": 24,
        "is_featured": True,
        "is_active": True,
    },
    {
        "id": "local-product-2",
        "name": "Checked Blazer",
        "sku": "BLZ-CHK-002",
        "price": 119.99,
        "original_price": 159.99,
        "emoji": "🕴",
        "category": "Clothing",
        "tags": ["sale"],
        "short_description": "Elegant houndstooth blazer, perfect for formal occasions.",
        "description": "A sharp houndstooth checked blazer with a tailored fit. Features two-button fastening, welt pockets, and a subtle logo lining. Versatile enough for the boardroom or a night out.",
        "image_url": "https://images.unsplash.com/photo-1594938298603-c8148c4b984f?w=600&q=80",
        "image_urls": [],
        "sizes": ["S", "M", "L", "XL"],
        "colours": ["Black/White", "Navy/White"],
        "material": "62% Polyester, 33% Viscose, 5% Elastane",
        "care_instructions": "Machine wash cold. Hang to dry. Do not iron directly.",
        "stock_count": 15,
        "is_featured": False,
        "is_active": True,
    },
    {
        "id": "local-product-3",
        "name": "Leather Ankle Boots",
        "sku": "BOOT-LEA-003",
        "price": 129.99,
        "original_price": None,
        "emoji": "👢",
        "category": "Footwear",
        "tags": ["bestseller"],
        "short_description": "Premium leather ankle boots with a block heel.",
        "description": "These classic ankle boots are crafted from full-grain leather with a cushioned insole and durable rubber outsole. A 5cm block heel provides comfortable height all day. A wardrobe essential.",
        "image_url": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=600&q=80",
        "image_urls": [],
        "sizes": ["36", "37", "38", "39", "40", "41", "42"],
        "colours": ["Black", "Tan", "Burgundy"],
        "material": "Full-grain leather upper, rubber sole",
        "care_instructions": "Wipe clean with a damp cloth. Apply leather conditioner regularly.",
        "stock_count": 32,
        "is_featured": True,
        "is_active": True,
    },
    {
        "id": "local-product-4",
        "name": "Silk Wrap Scarf",
        "sku": "SCRF-SLK-004",
        "price": 29.99,
        "original_price": None,
        "emoji": "🧣",
        "category": "Accessories",
        "tags": ["new-in"],
        "short_description": "Handcrafted silk scarf with a vibrant floral print.",
        "description": "Luxuriously soft 100% pure silk scarf with an exclusive floral design. Can be worn as a head wrap, neck scarf, or tied to a handbag for a pop of colour. Comes presented in a gift box.",
        "image_url": "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=600&q=80",
        "image_urls": [],
        "sizes": ["One Size"],
        "colours": ["Floral Ivory", "Floral Blush", "Floral Navy"],
        "material": "100% Pure Silk",
        "care_instructions": "Hand wash in cold water. Do not wring. Lay flat to dry.",
        "stock_count": 50,
        "is_featured": False,
        "is_active": True,
    },
    {
        "id": "local-product-5",
        "name": "Luxury Eau de Parfum",
        "sku": "PERF-LUX-005",
        "price": 89.99,
        "original_price": None,
        "emoji": "🌸",
        "category": "Beauty",
        "tags": ["bestseller", "new-in"],
        "short_description": "An opulent floral fragrance with warm amber base notes.",
        "description": "A signature fragrance inspired by the finest floral gardens. Top notes of bergamot and rose lead to a heart of jasmine and peony, grounded in warm amber and sandalwood. Eau de Parfum concentration. 50ml.",
        "image_url": "https://images.unsplash.com/photo-1541643600914-78b084683702?w=600&q=80",
        "image_urls": [],
        "sizes": ["30ml", "50ml", "100ml"],
        "colours": [],
        "material": "Eau de Parfum, 50ml",
        "care_instructions": "Keep away from direct sunlight and heat. Store in a cool, dry place.",
        "stock_count": 40,
        "is_featured": True,
        "is_active": True,
    },
    {
        "id": "local-product-6",
        "name": "Strappy Block-Heel Sandals",
        "sku": "HEEL-BLK-006",
        "price": 159.99,
        "original_price": 199.99,
        "emoji": "👠",
        "category": "Footwear",
        "tags": ["sale"],
        "short_description": "Elegant multi-strap sandals with a sturdy block heel.",
        "description": "Turn heads in these stunning strappy sandals. The 8cm block heel gives effortless height while a padded insole ensures all-night comfort. Features an ankle strap with adjustable buckle. Available in metallic gold and silver.",
        "image_url": "https://images.unsplash.com/photo-1596703263926-eb0762ee17e4?w=600&q=80",
        "image_urls": [],
        "sizes": ["36", "37", "38", "39", "40", "41"],
        "colours": ["Gold", "Silver", "Black"],
        "material": "Synthetic upper, padded footbed, rubber sole",
        "care_instructions": "Wipe with a dry cloth. Store in the dust bag provided.",
        "stock_count": 18,
        "is_featured": False,
        "is_active": True,
    },
    {
        "id": "local-product-7",
        "name": "Quilted Chain Shoulder Bag",
        "sku": "BAG-QLD-007",
        "price": 79.99,
        "original_price": None,
        "emoji": "👜",
        "category": "Accessories",
        "tags": ["new-in", "bestseller"],
        "short_description": "Classic quilted bag with a gold chain shoulder strap.",
        "description": "Timeless quilted leather-effect shoulder bag with a distinctive diamond-stitch pattern and gold-tone chain strap. Interior features a zip compartment and two slip pockets. Closes with a flip-lock clasp.",
        "image_url": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=600&q=80",
        "image_urls": [],
        "sizes": ["One Size"],
        "colours": ["Black", "Beige", "Burgundy"],
        "material": "Faux leather exterior, fabric lining",
        "care_instructions": "Wipe clean with a slightly damp cloth. Avoid prolonged sun exposure.",
        "stock_count": 22,
        "is_featured": False,
        "is_active": True,
    },
    {
        "id": "local-product-8",
        "name": "Ribbed Cashmere Rollneck",
        "sku": "KNIT-CSH-008",
        "price": 95.00,
        "original_price": None,
        "emoji": "🧶",
        "category": "Clothing",
        "tags": ["new-in"],
        "short_description": "Cosy ribbed rollneck in pure cashmere.",
        "description": "Indulge in the ultimate luxury knitwear. This fine-knit cashmere rollneck features a ribbed texture throughout for a flattering fit. Incredibly soft against the skin. A timeless investment piece.",
        "image_url": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=600&q=80",
        "image_urls": [],
        "sizes": ["XS", "S", "M", "L", "XL"],
        "colours": ["Oatmeal", "Camel", "Charcoal", "Dusty Rose"],
        "material": "100% Grade-A Cashmere",
        "care_instructions": "Dry clean or hand wash in cold water. Lay flat to dry.",
        "stock_count": 12,
        "is_featured": True,
        "is_active": True,
    },
]


def _initial_data():
    return {
        "customers": [],
        "orders": [],
        "products": DEFAULT_PRODUCTS.copy(),
    }


def _read_data():
    with _LOCK:
        if not DATA_FILE.exists():
            data = _initial_data()
            DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
            return data

        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = _initial_data()

        data.setdefault("customers", [])
        data.setdefault("orders", [])
        data.setdefault("products", DEFAULT_PRODUCTS.copy())
        return data


def _write_data(data):
    with _LOCK:
        DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _mutate(mutator):
    with _LOCK:
        if DATA_FILE.exists():
            try:
                data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                data = _initial_data()
        else:
            data = _initial_data()

        data.setdefault("customers", [])
        data.setdefault("orders", [])
        data.setdefault("products", DEFAULT_PRODUCTS.copy())
        result = mutator(data)
        DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
        return result


# ---------------------------------------------------------------------------
# Customer helpers
# ---------------------------------------------------------------------------

async def find_customer_by_email(email: str):
    normalized = email.lower()
    data = await asyncio.to_thread(_read_data)
    return next((c for c in data["customers"] if c["email"].lower() == normalized), None)


async def get_customer(customer_id: str):
    data = await asyncio.to_thread(_read_data)
    return next((c for c in data["customers"] if c["id"] == customer_id), None)


async def insert_customer(customer_doc: dict):
    def mutator(data):
        customer = {
            "id": uuid4().hex,
            "name": customer_doc["name"],
            "email": customer_doc["email"],
            "password": customer_doc["password"],
            "role": customer_doc.get("role", "customer"),
            "joined": customer_doc["joined"].isoformat(),
        }
        data["customers"].append(customer)
        return customer["id"]

    return await asyncio.to_thread(_mutate, mutator)


async def upsert_admin(admin_doc: dict):
    """Insert or promote an existing user to admin role."""
    def mutator(data):
        email = admin_doc["email"].lower()
        existing = next((c for c in data["customers"] if c["email"].lower() == email), None)
        if existing:
            existing["name"] = admin_doc["name"]
            existing["password"] = admin_doc["password"]
            existing["role"] = "admin"
            return existing["id"]
        admin = {
            "id": uuid4().hex,
            "name": admin_doc["name"],
            "email": admin_doc["email"],
            "password": admin_doc["password"],
            "role": "admin",
            "joined": admin_doc["joined"].isoformat(),
        }
        data["customers"].append(admin)
        return admin["id"]

    return await asyncio.to_thread(_mutate, mutator)


# ---------------------------------------------------------------------------
# Product helpers
# ---------------------------------------------------------------------------

# All new product fields that we persist
_PRODUCT_FIELDS = [
    "name", "sku", "price", "original_price", "emoji", "category", "tags",
    "short_description", "description", "image_url", "image_urls",
    "sizes", "colours", "material", "care_instructions",
    "stock_count", "is_featured", "is_active",
]


async def list_products(
    category: str | None = None,
    tag: str | None = None,
    search: str | None = None,
    featured_only: bool = False,
    active_only: bool = True,
) -> list:
    data = await asyncio.to_thread(_read_data)
    products = data["products"]

    if active_only:
        products = [p for p in products if p.get("is_active", True)]
    if featured_only:
        products = [p for p in products if p.get("is_featured", False)]
    if category:
        products = [p for p in products if (p.get("category") or "").lower() == category.lower()]
    if tag:
        products = [p for p in products if tag.lower() in [t.lower() for t in (p.get("tags") or [])]]
    if search:
        q = search.lower()
        products = [
            p for p in products
            if q in (p.get("name") or "").lower()
            or q in (p.get("short_description") or "").lower()
            or q in (p.get("description") or "").lower()
        ]

    return sorted(products, key=lambda p: (not p.get("is_featured", False), p.get("name", "")))


async def get_product(product_id: str):
    data = await asyncio.to_thread(_read_data)
    return next((p for p in data["products"] if p["id"] == product_id), None)


async def create_product(product_doc: dict):
    def mutator(data):
        product = {"id": uuid4().hex}
        for field in _PRODUCT_FIELDS:
            if field in product_doc:
                product[field] = product_doc[field]
        # Defaults for new fields
        product.setdefault("tags", [])
        product.setdefault("image_urls", [])
        product.setdefault("sizes", [])
        product.setdefault("colours", [])
        product.setdefault("is_featured", False)
        product.setdefault("is_active", True)
        data["products"].append(product)
        return product["id"]

    return await asyncio.to_thread(_mutate, mutator)


async def update_product(product_id: str, product_doc: dict):
    def mutator(data):
        for product in data["products"]:
            if product["id"] == product_id:
                for field in _PRODUCT_FIELDS:
                    if field in product_doc:
                        product[field] = product_doc[field]
                return True
        return False

    return await asyncio.to_thread(_mutate, mutator)


async def update_product_image(product_id: str, image_url: str, add_to_gallery: bool = True):
    """Set or add an image URL to a product."""
    def mutator(data):
        for product in data["products"]:
            if product["id"] == product_id:
                product["image_url"] = image_url
                if add_to_gallery:
                    gallery = product.get("image_urls") or []
                    if image_url not in gallery:
                        gallery.append(image_url)
                    product["image_urls"] = gallery[:5]  # max 5 gallery images
                return True
        return False

    return await asyncio.to_thread(_mutate, mutator)


async def delete_product(product_id: str):
    def mutator(data):
        before = len(data["products"])
        data["products"] = [p for p in data["products"] if p["id"] != product_id]
        return len(data["products"]) != before

    return await asyncio.to_thread(_mutate, mutator)


# ---------------------------------------------------------------------------
# Order helpers
# ---------------------------------------------------------------------------

async def insert_order(order_doc: dict):
    def mutator(data):
        order = {
            "order_id": uuid4().hex,
            "customer_id": order_doc["customer_id"],
            "product_id": order_doc["product_id"],
            "product_name": order_doc["product_name"],
            "price": order_doc["price"],
            "size": order_doc.get("size"),
            "colour": order_doc.get("colour"),
            "quantity": order_doc.get("quantity", 1),
            "created_at": order_doc["created_at"].isoformat(),
        }
        data["orders"].append(order)
        return order["order_id"]

    return await asyncio.to_thread(_mutate, mutator)


async def list_orders(customer_id: str):
    data = await asyncio.to_thread(_read_data)
    orders = [o for o in data["orders"] if o["customer_id"] == customer_id]
    return sorted(orders, key=lambda order: order["created_at"], reverse=True)
