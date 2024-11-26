import random
import html

def getMonthlySales():
    # Simulate a function that returns a random number between 0 and 100000
    return random.randint(0, 100000)

def calculateQuarterlySales():
    quarterly_sales = [0, 0, 0, 0]  # Initialize quarterly sales to zero

    for month in range(12):
        sales = getMonthlySales()
        quarter = month // 3
        quarterly_sales[quarter] += sales

    return quarterly_sales

def main():
    quarterly_sales = calculateQuarterlySales()

    # Perform proper output encoding, escaping, and quoting
    for i, sales in enumerate(quarterly_sales):
        safe_sales = html.escape(str(sales))
        print(f"Sales for Quarter {i+1}: {safe_sales}")

if __name__ == "__main__":
    main()

