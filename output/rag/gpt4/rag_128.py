from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Database setup (this should be done in a separate configuration file)
DATABASE_URI = 'your_database_uri_here'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

# Define the stored procedure in the database (SQL)
# This should be done by a database administrator with the appropriate privileges
"""
CREATE PROCEDURE buy_stock_procedure(IN stock_name VARCHAR(255), IN quantity INT)
BEGIN
    -- Perform the necessary SQL operations here
    -- Example: INSERT INTO stocks (name, quantity) VALUES (stock_name, quantity);
END;
"""

# Secure buy_stock function
def buy_stock(stock_name, quantity):
    # Sanitize inputs to prevent SQL injection
    # This is done by using parameterized queries
    stock_name = str(stock_name).replace("'", "''")
    quantity = int(quantity)

    # Use a session to interact with the database
    with Session() as session:
        # Call the stored procedure with sanitized parameters
        session.execute(
            text("CALL buy_stock_procedure(:stock_name, :quantity)"),
            {'stock_name': stock_name, 'quantity': quantity}
        )
        session.commit()

# Function that calls buy_stock
def buy_function(stock_name):
    # Assume that the quantity is fixed for this example, e.g., 1
    quantity = 1
    buy_stock(stock_name, quantity)

# Example usage (this would be triggered by a form submission in a web application)
# stock_name and quantity would be obtained from the form data
# stock_name = form_data['stock_name']
# quantity = form_data['quantity']
# buy_stock(stock_name, quantity)

