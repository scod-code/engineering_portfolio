import asyncio
import os
from config import load_app_env

load_app_env()

from database import products_collection

SAMPLE_PRODUCTS = [
    # Fashion Clothing
    {"name": "Wool Trench Coat", "price": 149.99, "emoji": "Coat", "category": "Clothing", "description": "Classic wool trench coat for all seasons"},
    {"name": "Checked Blazer", "price": 119.99, "emoji": "Blazer", "category": "Clothing", "description": "Elegant checked blazer for formal occasions"},
    {"name": "Silk Evening Dress", "price": 189.99, "emoji": "Dress", "category": "Clothing", "description": "Luxurious silk evening gown"},
    {"name": "Denim Jacket", "price": 79.99, "emoji": "Jacket", "category": "Clothing", "description": "Classic denim jacket with modern fit"},
    {"name": "Cashmere Sweater", "price": 129.99, "emoji": "Sweater", "category": "Clothing", "description": "Soft cashmere sweater for winter"},
    
    # Footwear
    {"name": "Leather Boots", "price": 129.99, "emoji": "Boots", "category": "Footwear", "description": "Premium leather ankle boots"},
    {"name": "Designer Heels", "price": 159.99, "emoji": "Heels", "category": "Footwear", "description": "Elegant designer high heels"},
    {"name": "Sneakers", "price": 89.99, "emoji": "Sneakers", "category": "Footwear", "description": "Comfortable casual sneakers"},
    
    # Accessories
    {"name": "Silk Scarf", "price": 29.99, "emoji": "Scarf", "category": "Accessories", "description": "Handmade silk scarf"},
    {"name": "Leather Handbag", "price": 199.99, "emoji": "Bag", "category": "Accessories", "description": "Italian leather handbag"},
    {"name": "Sunglasses", "price": 49.99, "emoji": "Shades", "category": "Accessories", "description": "UV protection sunglasses"},
    {"name": "Silver Necklace", "price": 79.99, "emoji": "Jewelry", "category": "Accessories", "description": "Sterling silver necklace"},
    
    # Beauty Products
    {"name": "Luxury Perfume", "price": 89.99, "emoji": "Perfume", "category": "Beauty", "description": "Exclusive fragrance collection"},
    {"name": "Skincare Set", "price": 129.99, "emoji": "Skincare", "category": "Beauty", "description": "Complete skincare routine set"},
    {"name": "Makeup Palette", "price": 59.99, "emoji": "Makeup", "category": "Beauty", "description": "Professional makeup palette"},
    {"name": "Hair Care Kit", "price": 69.99, "emoji": "Haircare", "category": "Beauty", "description": "Premium hair care products"},
]


async def seed():
    count = await products_collection.count_documents({})
    if count > 0:
        print(f"Products collection already has {count} documents - skipping seed.")
        return
    result = await products_collection.insert_many(SAMPLE_PRODUCTS)
    print(f"Inserted {len(result.inserted_ids)} sample fashion and beauty products.")
    print("Categories: Clothing, Footwear, Accessories, Beauty")


if __name__ == "__main__":
    asyncio.run(seed())
