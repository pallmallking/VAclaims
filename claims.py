import pandas as pd
import pip

# Check if pandasql is installed, if not, install it
try:
    import pandasql
except ImportError:
    print("pandasql is not installed. Installing it now...")
    pip.main(['install', 'pandasql'])
    # If pip is not available, you can use subprocess to install
    import subprocess
    subprocess.check_call(['pip', 'install', 'pandasql'])                   
# If you want to run SQL queries on a DataFrame using pandasql,
try:
    from pandasql import sqldf
except ImportError:
    raise ImportError("Please install 'pandasql' to use SQL queries with Pandas DataFrames.")

def main():
    """
    This script loads a CSV dataset into Pandas and demonstrates
    basic SQL-style analysis using pandasql.
    Update 'file_path' to point to your target CSV file.
    """
    # Path to your CSV file
    file_path = "VA_claims(2020 vs 2024) (2) - VA_claims(2020 vs 2024) (2).csv"

    # Read the CSV into a DataFrame
    df = pd.read_csv(file_path, encoding='utf-8', engine='python')

    # Rename columns to ensure they're SQL-friendly (remove spaces, parentheses, etc.)
    df.columns = [
        col.replace(" ", "_").replace("-", "_").replace("(", "_").replace(")", "_")
        for col in df.columns
    ]

    print("DataFrame info:")
    print(df.info())
    print("\nFirst 5 rows of the dataset:")
    print(df.head(), "\n")

    # Example query 1: Show 10 records with columns: Row_Labels, 2020, 2024, sum, and Ratio
    query_1 = """
        SELECT Row_Labels,
               2020 AS Year2020,
               2024 AS Year2024,
               sum,
               Ratio
        FROM df
        LIMIT 10
    """
    print("SQL Query 1: First 10 rows")
    print(sqldf(query_1, locals()), "\n")

    # Convert potential numeric columns to numeric for consistent analysis
    numeric_cols = ["2020", "2024", "sum", "Ratio"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Example query 2: Find the top 5 rows by highest Ratio
    query_2 = """
        SELECT Row_Labels,
               2020 AS Year2020,
               2024 AS Year2024,
               sum,
               Ratio
        FROM df
        ORDER BY Ratio DESC
        LIMIT 5
    """
    print("SQL Query 2: Top 5 rows by Ratio")
    print(sqldf(query_2, locals()), "\n")

    # Example query 3: Calculate the average Ratio
    query_3 = """
        SELECT AVG(Ratio) AS average_ratio
        FROM df
        WHERE Ratio IS NOT NULL
    """
    print("SQL Query 3: Average Ratio")
    print(sqldf(query_3, locals()), "\n")

if __name__ == "__main__":
    main()
