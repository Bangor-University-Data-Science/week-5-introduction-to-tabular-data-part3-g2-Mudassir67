import pandas as pd
import chardet

# Helper function to detect file encoding
def get_encoding(file_path):
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read(10000))
        print(f"Detected encoding: {result['encoding']} - Confidence: {result['confidence']}")
        return result['encoding']

# Import the dataset into a DataFrame
def import_data(filename: str) -> pd.DataFrame:
    print(f"Trying to import data from {filename}")
    file_encoding = get_encoding(filename)
    try:
        df = pd.read_excel(filename)
        print("Read file as Excel.")
    except ValueError:
        df = pd.read_csv(filename, encoding=file_encoding)
        print("Read file as CSV.")
    print("Columns in the DataFrame:", df.columns)
    if 'Quantity' in df.columns and 'UnitPrice' in df.columns:
        df['Total_Revenue'] = df['Quantity'] * df['UnitPrice']
    return df

# Filter the data to remove inappropriate rows
def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df['CustomerID'].notna()]
    numeric_cols = df.select_dtypes(include=['number']).columns
    df = df[(df[numeric_cols] >= 0).all(axis=1)]
    return df

# Identify loyal customers
def loyal_customers(df: pd.DataFrame, min_purchases: int) -> pd.DataFrame:
    counts = df.groupby('CustomerID').size()
    return counts[counts >= min_purchases]

# Calculate the total revenue per quarter
def quarterly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Quarter'] = df['InvoiceDate'].dt.to_period('Q')
    return df.groupby('Quarter')['Total_Revenue'].sum().reset_index()

# Identify the top products by total quantity sold
def high_demand_products(df: pd.DataFrame, top_n: int) -> pd.DataFrame:
    product_quantities = df.groupby('StockCode')['Quantity'].sum().nlargest(top_n)
    return product_quantities

# Create a summary showing average quantity and unit price for each product
def product_summary(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby('StockCode').agg(avg_quantity=('Quantity', 'mean'),
                                       avg_unit_price=('UnitPrice', 'mean'))

# Run all tasks
def main():
    filename = "Customer_Behavior.xlsx"
    df = import_data(filename)
    df = filter_data(df)
    print(loyal_customers(df, 5))
    print(quarterly_revenue(df))
    print(high_demand_products(df, 5))
    print(product_summary(df))

if __name__ == "__main__":
    main()

def answer_conceptual_questions() -> dict:
    ans = {
        'Q1': 'A',
        'Q2': 'B',
        'Q3': 'C',
        'Q4': 'A',
        'Q5': 'A'
    }
    return ans

ans = answer_conceptual_questions()
print(ans)
