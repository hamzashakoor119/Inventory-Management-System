import json
from datetime import datetime
from typing import Dict, List, Optional, Type, Union
from models.product import Product, Electronics, Grocery, Clothing
from exceptions.inventory_exceptions import (
    DuplicateProductError,
    ProductNotFoundError,
    InvalidProductDataError
)

class Inventory:
    """Class to manage a collection of products."""
    
    def __init__(self):
        """Initialize an empty inventory."""
        self._products: Dict[str, Product] = {}
    
    def add_product(self, product: Product) -> None:
        """
        Add a product to the inventory.
        
        Args:
            product (Product): The product to add
            
        Raises:
            DuplicateProductError: If a product with the same ID already exists
        """
        if product.product_id in self._products:
            raise DuplicateProductError(product.product_id)
        self._products[product.product_id] = product
    
    def remove_product(self, product_id: str) -> None:
        """
        Remove a product from the inventory.
        
        Args:
            product_id (str): ID of the product to remove
            
        Raises:
            ProductNotFoundError: If no product exists with the given ID
        """
        if product_id not in self._products:
            raise ProductNotFoundError(product_id)
        del self._products[product_id]
    
    def get_product(self, product_id: str) -> Product:
        """
        Get a product by its ID.
        
        Args:
            product_id (str): ID of the product to get
            
        Returns:
            Product: The requested product
            
        Raises:
            ProductNotFoundError: If no product exists with the given ID
        """
        if product_id not in self._products:
            raise ProductNotFoundError(product_id)
        return self._products[product_id]
    
    def search_by_name(self, name: str) -> List[Product]:
        """
        Search for products by name (case-insensitive partial match).
        
        Args:
            name (str): Name to search for
            
        Returns:
            List[Product]: List of matching products
        """
        name = name.lower()
        return [p for p in self._products.values() if name in p.name.lower()]
    
    def search_by_type(self, product_type: Type[Product]) -> List[Product]:
        """
        Search for products by type.
        
        Args:
            product_type (Type[Product]): Type of product to search for
            
        Returns:
            List[Product]: List of products of the specified type
        """
        return [p for p in self._products.values() if isinstance(p, product_type)]
    
    def list_all_products(self) -> List[Product]:
        """
        Get a list of all products in the inventory.
        
        Returns:
            List[Product]: List of all products
        """
        return list(self._products.values())
    
    def sell_product(self, product_id: str, quantity: int) -> float:
        """
        Sell a specific quantity of a product.
        
        Args:
            product_id (str): ID of the product to sell
            quantity (int): Quantity to sell
            
        Returns:
            float: Total value of the sale
            
        Raises:
            ProductNotFoundError: If no product exists with the given ID
        """
        product = self.get_product(product_id)
        return product.sell(quantity)
    
    def restock_product(self, product_id: str, quantity: int) -> None:
        """
        Restock a product.
        
        Args:
            product_id (str): ID of the product to restock
            quantity (int): Quantity to add
            
        Raises:
            ProductNotFoundError: If no product exists with the given ID
        """
        product = self.get_product(product_id)
        product.restock(quantity)
    
    def total_inventory_value(self) -> float:
        """
        Calculate the total value of all products in inventory.
        
        Returns:
            float: Total value of inventory
        """
        return sum(product.get_total_value() for product in self._products.values())
    
    def remove_expired_products(self) -> List[str]:
        """
        Remove all expired grocery products from inventory.
        
        Returns:
            List[str]: List of IDs of removed products
        """
        expired_ids = []
        for product_id, product in list(self._products.items()):
            if isinstance(product, Grocery) and product.is_expired():
                del self._products[product_id]
                expired_ids.append(product_id)
        return expired_ids
    
    def save_to_file(self, filename: str) -> None:
        """
        Save inventory to a JSON file.
        
        Args:
            filename (str): Name of the file to save to
        """
        data = {
            "products": [product.to_dict() for product in self._products.values()]
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, filename: str) -> None:
        """
        Load inventory from a JSON file.
        
        Args:
            filename (str): Name of the file to load from
            
        Raises:
            InvalidProductDataError: If the file contains invalid product data
        """
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            self._products.clear()
            product_classes = {
                "Electronics": Electronics,
                "Grocery": Grocery,
                "Clothing": Clothing
            }
            
            for product_data in data.get("products", []):
                product_type = product_data.pop("type", None)
                if product_type not in product_classes:
                    raise InvalidProductDataError(f"Unknown product type: {product_type}")
                
                # Convert expiry_date string back to datetime for Grocery products
                if product_type == "Grocery":
                    product_data["expiry_date"] = datetime.fromisoformat(product_data["expiry_date"])
                
                product = product_classes[product_type](**product_data)
                self.add_product(product)
                
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            raise InvalidProductDataError(str(e)) 