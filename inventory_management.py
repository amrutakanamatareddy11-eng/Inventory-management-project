import os
from datetime import datetime


# Parent class
class ActivityLog:

    # Get current date and time
    def get_time(self):
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    # Save activity in log file
    def log_activity(self, message):
        with open("activity_log.txt", "a") as file:
            file.write(f"[{self.get_time()}] {message}\n")


# Child class
class Inventory(ActivityLog):

    def __init__(self):
        self.products = []
        self.product_id = 1

    # Add Product
    def add_product(self):
        print("\n--- Add Product ---")

        name = input("Enter name of the product: ")
        price = int(input("Enter the price of the product: "))
        quantity = int(input("Quantity: "))

        product = {
            "ID": self.product_id,
            "Name": name,
            "Price": price,
            "Quantity": quantity
        }

        self.products.append(product)

        self.log_activity(
            f"Added product: {name} | "
            f"ID: {self.product_id} | "
            f"Price: ₹{price} | "
            f"Quantity: {quantity}"
        )

        self.product_id = self.product_id + 1

        print("Product added successfully!")

    # View Products
    def view_products(self):
        print("\n--- All Products ---")

        if len(self.products) == 0:
            print("No products available.")
            return

        for product in self.products:
            print(
                "ID:", product["ID"],
                "| Name:", product["Name"],
                "| Price:", product["Price"],
                "| Quantity:", product["Quantity"]
            )

    # Update Stock
    def update_stock(self):
        id = int(input("Enter product ID: "))
        found = False

        for product in self.products:

            if id == product["ID"]:

                quantity = int(input("Enter quantity to add: "))

                product["Quantity"] = product["Quantity"] + quantity

                self.log_activity(
                    f"Updated stock: {product['Name']} | "
                    f"ID: {product['ID']} | "
                    f"Added: {quantity} | "
                    f"New Stock: {product['Quantity']}"
                )

                found = True

                print("Stock is updated")
                break

        if not found:
            print("Invalid ID")

    # Delete Product
    def delete_product(self):
        id = int(input("Enter product ID to delete: "))
        found = False

        for product in self.products:

            if id == product["ID"]:

                self.products.remove(product)

                self.log_activity(
                    f"Deleted product: {product['Name']} | "
                    f"ID: {product['ID']} | "
                    f"Quantity: {product['Quantity']}"
                )

                found = True

                print("Product deleted successfully!")
                break

        if not found:
            print("Invalid ID")

    # Generate Bill
    def generate_bill(self):
        id = int(input("Enter the ID of the product: "))
        quantity = int(input("Enter the quantity of product: "))
        found = False

        for product in self.products:

            if id == product["ID"]:

                found = True

                if quantity <= product["Quantity"]:

                    total_price = quantity * product["Price"]

                    product["Quantity"] = (
                        product["Quantity"] - quantity
                    )

                    print("\n----- BILL -----")
                    print("Date and Time:", self.get_time())
                    print("Product:", product["Name"])
                    print("Price:", product["Price"])
                    print("Quantity:", quantity)
                    print("Total Bill:", total_price)
                    print("----------------")

                    self.log_activity(
                        f"Bill generated: {product['Name']} | "
                        f"ID: {product['ID']} | "
                        f"Quantity: {quantity} | "
                        f"Total: ₹{total_price}"
                    )

                else:
                    print("Not enough stock")

                break

        if not found:
            print("Invalid ID")

    # View Activity Log
    def view_log(self):
        print("\n--- Activity Log ---")

        if not os.path.exists("activity_log.txt"):
            print("No activity recorded yet.")
            return

        with open("activity_log.txt", "r") as file:
            for line in file:
                print(line.strip())

    # Save Inventory
    def save_file(self):

        with open("inventory.txt", "w") as file:

            for product in self.products:

                file.write(
                    f'{product["ID"]},{product["Name"]},'
                    f'{product["Price"]},{product["Quantity"]}\n'
                )

        self.log_activity("Inventory saved successfully")

    # Load Inventory
    def load_file(self):

        if os.path.exists("inventory.txt"):

            with open("inventory.txt", "r") as file:

                for line in file:

                    data = line.strip().split(",")

                    product = {
                        "ID": int(data[0]),
                        "Name": data[1],
                        "Price": int(data[2]),
                        "Quantity": int(data[3])
                    }

                    self.products.append(product)

                    if product["ID"] >= self.product_id:
                        self.product_id = product["ID"] + 1

        else:
            print("No saved products found.")


# Create Inventory object
inventory = Inventory()

# Load previously saved products
inventory.load_file()

choice = "yes"

while choice == "yes":

    option = int(
        input(
            "\nChoose\n"
            "1. Add Product\n"
            "2. View All Products\n"
            "3. Update Stock\n"
            "4. Delete Product\n"
            "5. Generate Bill\n"
            "6. View Activity Log\n"
            "7. Exit\n"
            "Enter your choice: "
        )
    )

    if option == 1:
        inventory.add_product()

    elif option == 2:
        inventory.view_products()

    elif option == 3:
        inventory.update_stock()

    elif option == 4:
        inventory.delete_product()

    elif option == 5:
        inventory.generate_bill()

    elif option == 6:
        inventory.view_log()

    elif option == 7:
        inventory.save_file()
        print("Thank you!")
        break

    else:
        print("Invalid option")

    choice = input(
        "Do you want to continue (yes/no): "
    ).lower()
