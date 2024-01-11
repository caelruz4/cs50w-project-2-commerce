# script.py

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "commerce.settings")  # Reemplaza "tuproyecto" con el nombre de tu proyecto
django.setup()

from auctions.models import Category  # Reemplaza "tuapp" con el nombre de tu aplicación

def create_categories():
    categories = [
        "Art",
        "Electronics",
        "Clothing and Accessories",
        "Jewelry and Watches",
        "Furniture and Home Decor",
        "Books and Media",
        "Sports and Recreation",
        "Cars and Vehicles",
        "Toys and Collectibles",
        "Musical Instruments",
    ]

    for category_name in categories:
        Category.objects.create(name=category_name)
        print(f"Category '{category_name}' created.")

if __name__ == "__main__":
    create_categories()
