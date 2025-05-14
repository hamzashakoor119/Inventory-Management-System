from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any
from exceptions.inventory_exceptions import InsufficientStockError

class Product(ABC):
    """Abstract base class for all products in the inventory system."""
    
    def __init__(self, product_id: str, name: str, price: float, quantity_in_stock: int):
        """
        Initialize a new product.
        
        Args:
            product_id (str): Unique identifier for the product
            name (str): Name of the product
            price (float): Price of the product
            quantity_in_stock (int): Initial quantity in stock
        """
        self._product_id = product_id
        self._name = name
        self._price = price
        self._quantity_in_stock = quantity_in_stock
    
    @property
    def product_id(self) -> str:
        return self._product_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def price(self) -> float:
        return self._price
    
    @property
    def quantity_in_stock(self) -> int:
        return self._quantity_in_stock
    
    def restock(self, amount: int) -> None:
        """
        Add more items to stock.
        
        Args:
            amount (int): Number of items to add
        """
        if amount <= 0:
            raise ValueError("Restock amount must be positive")
        self._quantity_in_stock += amount
    
    def sell(self, quantity: int) -> float:
        """
        Sell items from stock.
        
        Args:
            quantity (int): Number of items to sell
            
        Returns:
            float: Total value of the sale
            
        Raises:
            InsufficientStockError: If trying to sell more than available
        """
        if quantity <= 0:
            raise ValueError("Sale quantity must be positive")
        if quantity > self._quantity_in_stock:
            raise InsufficientStockError(self._product_id, quantity, self._quantity_in_stock)
        
        self._quantity_in_stock -= quantity
        return self._price * quantity
    
    def get_total_value(self) -> float:
        """Calculate total value of current stock."""
        return self._price * self._quantity_in_stock
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert product to dictionary for serialization."""
        return {
            "product_id": self._product_id,
            "name": self._name,
            "price": self._price,
            "quantity_in_stock": self._quantity_in_stock,
            "type": self.__class__.__name__
        }
    
    @abstractmethod
    def __str__(self) -> str:
        """String representation of the product."""
        return f"Product ID: {self._product_id}\nName: {self._name}\nPrice: Rs.{self._price:.2f}\nStock: {self._quantity_in_stock}"


class Electronics(Product):
    """Class representing electronic products."""
    
    def __init__(self, product_id: str, name: str, price: float, quantity_in_stock: int,
                 warranty_years: int, brand: str):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._warranty_years = warranty_years
        self._brand = brand
    
    @property
    def warranty_years(self) -> int:
        return self._warranty_years
    
    @property
    def brand(self) -> str:
        return self._brand
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "warranty_years": self._warranty_years,
            "brand": self._brand
        })
        return data
    
    def __str__(self) -> str:
        base_info = super().__str__()
        return f"{base_info}\nBrand: {self._brand}\nWarranty: {self._warranty_years} years"


class Grocery(Product):
    """Class representing grocery products."""
    
    def __init__(self, product_id: str, name: str, price: float, quantity_in_stock: int,
                 expiry_date: datetime):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._expiry_date = expiry_date
    
    @property
    def expiry_date(self) -> datetime:
        return self._expiry_date
    
    def is_expired(self) -> bool:
        """Check if the product has expired."""
        return datetime.now() > self._expiry_date
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "expiry_date": self._expiry_date.isoformat()
        })
        return data
    
    def __str__(self) -> str:
        base_info = super().__str__()
        expiry_status = "EXPIRED" if self.is_expired() else "Valid"
        return f"{base_info}\nExpiry Date: {self._expiry_date.strftime('%Y-%m-%d')}\nStatus: {expiry_status}"


class Clothing(Product):
    """Class representing clothing products."""
    
    def __init__(self, product_id: str, name: str, price: float, quantity_in_stock: int,
                 size: str, material: str):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._size = size
        self._material = material
    
    @property
    def size(self) -> str:
        return self._size
    
    @property
    def material(self) -> str:
        return self._material
    
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "size": self._size,
            "material": self._material
        })
        return data
    
    def __str__(self) -> str:
        base_info = super().__str__()
        return f"{base_info}\nSize: {self._size}\nMaterial: {self._material}" 