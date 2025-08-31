class Customer:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 1 <= len(value) <= 15:
            self._name = value

    def orders(self):
        """Return all orders belonging to this customer."""
        from classes.many_to_many import Order  
        return [order for order in Order.all if order.customer == self]

    def coffees(self):
        """Return all unique coffees ordered by this customer."""
        return list({order.coffee for order in self.orders()})
    
    def create_order(self, coffee, price):
        """Create a new order for this customer."""
        from classes.many_to_many import Order
        return Order(self, coffee, price)



class Coffee:
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if len(name) <= 2:
            raise ValueError("Name must be longer than 2 characters")
        self._name = name

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        pass
    def orders(self):
        """Return all orders for this coffee"""
        from classes.many_to_many import Order  
        return [order for order in Order.all if order.coffee is self]



    def customers(self):
        """Return all unique customers who ordered this coffee"""
        return list({order.customer for order in self.orders()})
    
    def num_orders(self):
        """Return the total number of orders for this coffee"""
        return len(self.orders())
    
    def average_price(self):
        """Return the average price of all orders for this coffee"""
        orders = self.orders()
        if not orders:  
            return 0
        total = sum(order.price for order in orders)
        return total / len(orders)




class Order:
    all = []

    def __init__(self, customer, coffee, price):
        from classes.many_to_many import Customer, Coffee  # avoid circular import issues
        if not isinstance(customer, Customer):
            raise TypeError("customer must be a Customer instance")
        if not isinstance(coffee, Coffee):
            raise TypeError("coffee must be a Coffee instance")
        if not (isinstance(price, (int, float)) and 1.0 <= price <= 10.0):
            raise ValueError("price must be a number between 1.0 and 10.0")

        self._customer = customer
        self._coffee = coffee
        self._price = price
        Order.all.append(self)

    @property
    def customer(self):
        return self._customer

    @property
    def coffee(self):
        return self._coffee

    @property
    def price(self):
        return self._price

    def __repr__(self):
        return f"<Order: {self.customer.name} ordered {self.coffee.name} for ${self.price}>"
