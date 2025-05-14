"""Exceptions package for the inventory management system."""

from .inventory_exceptions import (
    InventoryError,
    InsufficientStockError,
    DuplicateProductError,
    ProductNotFoundError,
    InvalidProductDataError
)

__all__ = [
    'InventoryError',
    'InsufficientStockError',
    'DuplicateProductError',
    'ProductNotFoundError',
    'InvalidProductDataError'
] 