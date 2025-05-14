import sys
from datetime import datetime
from typing import Optional, Tuple
from models.inventory import Inventory
from models.product import Electronics, Grocery, Clothing
from exceptions.inventory_exceptions import (
    InventoryError,
    InsufficientStockError,
    DuplicateProductError,
    ProductNotFoundError,
    InvalidProductDataError
)

class InventoryCLI:
    """Command-line interface for the inventory management system."""
    
    def __init__(self):
        """Initialize the CLI with an empty inventory."""
        self.inventory = Inventory()
    
    def display_menu(self) -> None:
        """Display the main menu options."""
        print("\n=== Inventory Management System By Code With Hamza ===")
        print("1. Add Product")
        print("2. Remove Product")
        print("3. Search Products")
        print("4. List All Products")
        print("5. Sell Product")
        print("6. Restock Product")
        print("7. Remove Expired Products")
        print("8. Save Inventory")
        print("9. Load Inventory")
        print("10. Show Total Inventory Value")
        print("0. Exit")
        print("================================")
    
    def get_product_type(self) -> Tuple[str, type]:
        """Get product type from user input."""
        print("\nSelect product type:")
        print("1. Electronics")
        print("2. Grocery")
        print("3. Clothing")
        
        while True:
            try:
                choice = int(input("Enter choice (1-3): "))
                if choice == 1:
                    return "Electronics", Electronics
                elif choice == 2:
                    return "Grocery", Grocery
                elif choice == 3:
                    return "Clothing", Clothing
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")
    
    def get_product_details(self, product_type: str) -> dict:
        """Get common product details from user input."""
        details = {}
        details["product_id"] = input("Enter product ID: ").strip()
        details["name"] = input("Enter product name: ").strip()
        
        while True:
            try:
                details["price"] = float(input("Enter price: "))
                if details["price"] <= 0:
                    raise ValueError("Price must be positive")
                break
            except ValueError as e:
                print(f"Invalid price: {e}")
        
        while True:
            try:
                details["quantity_in_stock"] = int(input("Enter quantity in stock: "))
                if details["quantity_in_stock"] < 0:
                    raise ValueError("Quantity cannot be negative")
                break
            except ValueError as e:
                print(f"Invalid quantity: {e}")
        
        return details
    
    def get_electronics_details(self) -> dict:
        """Get electronics-specific details from user input."""
        details = self.get_product_details("Electronics")
        
        while True:
            try:
                details["warranty_years"] = int(input("Enter warranty years: "))
                if details["warranty_years"] < 0:
                    raise ValueError("Warranty years cannot be negative")
                break
            except ValueError as e:
                print(f"Invalid warranty years: {e}")
        
        details["brand"] = input("Enter brand: ").strip()
        return details
    
    def get_grocery_details(self) -> dict:
        """Get grocery-specific details from user input."""
        details = self.get_product_details("Grocery")
        
        while True:
            try:
                date_str = input("Enter expiry date (YYYY-MM-DD): ")
                details["expiry_date"] = datetime.strptime(date_str, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD")
        
        return details
    
    def get_clothing_details(self) -> dict:
        """Get clothing-specific details from user input."""
        details = self.get_product_details("Clothing")
        details["size"] = input("Enter size: ").strip()
        details["material"] = input("Enter material: ").strip()
        return details
    
    def add_product(self) -> None:
        """Add a new product to inventory."""
        try:
            product_type, product_class = self.get_product_type()
            
            if product_type == "Electronics":
                details = self.get_electronics_details()
                product = Electronics(**details)
            elif product_type == "Grocery":
                details = self.get_grocery_details()
                product = Grocery(**details)
            else:  # Clothing
                details = self.get_clothing_details()
                product = Clothing(**details)
            
            self.inventory.add_product(product)
            print(f"\nSuccessfully added {product_type} product: {product.name}")
            
        except DuplicateProductError as e:
            print(f"\nError: {e}")
        except Exception as e:
            print(f"\nError adding product: {e}")
    
    def remove_product(self) -> None:
        """Remove a product from inventory."""
        try:
            product_id = input("\nEnter product ID to remove: ").strip()
            self.inventory.remove_product(product_id)
            print(f"\nSuccessfully removed product {product_id}")
        except ProductNotFoundError as e:
            print(f"\nError: {e}")
    
    def search_products(self) -> None:
        """Search for products by name or type."""
        print("\nSearch by:")
        print("1. Name")
        print("2. Type")
        
        try:
            choice = int(input("Enter choice (1-2): "))
            if choice == 1:
                name = input("Enter product name to search: ").strip()
                products = self.inventory.search_by_name(name)
            elif choice == 2:
                product_type, _ = self.get_product_type()
                if product_type == "Electronics":
                    products = self.inventory.search_by_type(Electronics)
                elif product_type == "Grocery":
                    products = self.inventory.search_by_type(Grocery)
                else:
                    products = self.inventory.search_by_type(Clothing)
            else:
                print("Invalid choice")
                return
            
            if not products:
                print("\nNo products found")
            else:
                print(f"\nFound {len(products)} products:")
                for product in products:
                    print("\n" + str(product))
                    
        except ValueError:
            print("Invalid input")
    
    def list_products(self) -> None:
        """List all products in inventory."""
        products = self.inventory.list_all_products()
        if not products:
            print("\nNo products in inventory")
        else:
            print(f"\nFound {len(products)} products:")
            for product in products:
                print("\n" + str(product))
    
    def sell_product(self) -> None:
        """Sell a product."""
        try:
            product_id = input("\nEnter product ID: ").strip()
            quantity = int(input("Enter quantity to sell: "))
            
            total = self.inventory.sell_product(product_id, quantity)
            print(f"\nSuccessfully sold {quantity} items")
            print(f"Total sale value: Rs.{total:.2f}")
            
        except (ValueError, ProductNotFoundError, InsufficientStockError) as e:
            print(f"\nError: {e}")
    
    def restock_product(self) -> None:
        """Restock a product."""
        try:
            product_id = input("\nEnter product ID: ").strip()
            quantity = int(input("Enter quantity to add: "))
            
            self.inventory.restock_product(product_id, quantity)
            print(f"\nSuccessfully restocked {quantity} items")
            
        except (ValueError, ProductNotFoundError) as e:
            print(f"\nError: {e}")
    
    def remove_expired(self) -> None:
        """Remove expired grocery products."""
        expired_ids = self.inventory.remove_expired_products()
        if not expired_ids:
            print("\nNo expired products found")
        else:
            print(f"\nRemoved {len(expired_ids)} expired products:")
            for product_id in expired_ids:
                print(f"- {product_id}")
    
    def save_inventory(self) -> None:
        """Save inventory to file."""
        try:
            filename = input("\nEnter filename to save to: ").strip()
            self.inventory.save_to_file(filename)
            print(f"\nSuccessfully saved inventory to {filename}")
        except Exception as e:
            print(f"\nError saving inventory: {e}")
    
    def load_inventory(self) -> None:
        """Load inventory from file."""
        try:
            filename = input("\nEnter filename to load from: ").strip()
            self.inventory.load_from_file(filename)
            print(f"\nSuccessfully loaded inventory from {filename}")
        except InvalidProductDataError as e:
            print(f"\nError loading inventory: {e}")
        except Exception as e:
            print(f"\nError loading inventory: {e}")
    
    def show_total_value(self) -> None:
        """Show total inventory value."""
        total = self.inventory.total_inventory_value()
        print(f"\nTotal inventory value: Rs.{total:.2f}")
    
    def run(self) -> None:
        """Run the main CLI loop."""
        while True:
            self.display_menu()
            try:
                choice = int(input("\nEnter your choice (0-10): "))
                
                if choice == 0:
                    print("\nGoodbye!")
                    break
                elif choice == 1:
                    self.add_product()
                elif choice == 2:
                    self.remove_product()
                elif choice == 3:
                    self.search_products()
                elif choice == 4:
                    self.list_products()
                elif choice == 5:
                    self.sell_product()
                elif choice == 6:
                    self.restock_product()
                elif choice == 7:
                    self.remove_expired()
                elif choice == 8:
                    self.save_inventory()
                elif choice == 9:
                    self.load_inventory()
                elif choice == 10:
                    self.show_total_value()
                else:
                    print("\nInvalid choice. Please try again.")
                    
            except ValueError:
                print("\nPlease enter a number")
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nAn error occurred: {e}")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    cli = InventoryCLI()
    cli.run() 