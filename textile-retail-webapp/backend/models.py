from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List

# ----- Request bodies (what the frontend SENDS to the server) -----

class CustomerRegister(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr       # Pydantic validates this is a real email format
    password: str = Field(..., min_length=8, max_length=128)

class CustomerLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

class AdminSetup(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    admin_key: str = Field(..., min_length=1)

class OrderCreate(BaseModel):
    product_id: str = Field(...)
    product_name: str = Field(..., min_length=1, max_length=200)
    price: float = Field(..., gt=0)
    size: Optional[str] = Field(None, max_length=20)
    colour: Optional[str] = Field(None, max_length=50)
    quantity: int = Field(1, ge=1, le=99)

# ----- Response shapes (what the server SENDS BACK) -----
# Never include the hashed password in responses

class CustomerOut(BaseModel):
    id: str
    name: str
    email: str
    joined: datetime

class OrderOut(BaseModel):
    order_id: str
    product_name: str
    price: float
    created_at: str
    size: Optional[str] = None
    colour: Optional[str] = None
    quantity: int = 1


# ----- Product models -----
# Designed to be modular: any field can be None for backwards compatibility.
# Image URLs are plain strings — the image storage backend is abstracted in
# backend/image_storage.py and can be swapped without changing these models.

class ProductIn(BaseModel):
    # Core
    name: str = Field(..., min_length=1, max_length=200)
    sku: Optional[str] = Field(None, max_length=100)
    price: float = Field(..., gt=0)
    original_price: Optional[float] = Field(None, gt=0)   # If set, shows sale badge
    category: Optional[str] = Field(None, max_length=50)
    tags: Optional[List[str]] = Field(default_factory=list)  # e.g. ["new-in","sale"]

    # Descriptions
    short_description: Optional[str] = Field(None, max_length=200)  # Shown on cards
    description: Optional[str] = Field(None, max_length=3000)       # Full product page

    # Images (plain URLs — see image_storage.py for how they're generated)
    image_url: Optional[str] = Field(None, max_length=1000)         # Primary / cover
    image_urls: Optional[List[str]] = Field(default_factory=list)   # Gallery (up to 5)

    # Variants
    sizes: Optional[List[str]] = Field(default_factory=list)        # e.g. ["S","M","L"]
    colours: Optional[List[str]] = Field(default_factory=list)      # e.g. ["Black","White"]

    # Details
    material: Optional[str] = Field(None, max_length=200)
    care_instructions: Optional[str] = Field(None, max_length=500)

    # Inventory & visibility
    stock_count: Optional[int] = Field(None, ge=0)  # None = not tracked, 0 = out of stock
    is_featured: bool = Field(False)
    is_active: bool = Field(True)

    # Legacy field kept for backwards compatibility
    emoji: Optional[str] = Field(None, max_length=10)


class ProductOut(BaseModel):
    id: str
    name: str
    sku: Optional[str] = None
    price: float
    original_price: Optional[float] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None

    short_description: Optional[str] = None
    description: Optional[str] = None

    image_url: Optional[str] = None
    image_urls: Optional[List[str]] = None

    sizes: Optional[List[str]] = None
    colours: Optional[List[str]] = None

    material: Optional[str] = None
    care_instructions: Optional[str] = None

    stock_count: Optional[int] = None
    is_featured: bool = False
    is_active: bool = True

    # Legacy
    emoji: Optional[str] = None
