from smolagents import TOOL_MAPPING, tool
import pandas as pd

@tool
def fetch_data() -> pd.DataFrame:
    """
    Reads the .csv file in /data/Expenses.csv and returns a pandas DataFrame.
    """

    return pd.read_csv("data/Expenses.csv")

@tool
def fetch_available_categories_and_subcategories(df: pd.DataFrame) -> dict[str, list[str]]:
    """
    Extracts and returns a dictionary of unique categories and subcategories from the expenses DataFrame.

    Args:
        df (pd.DataFrame): The pandas DataFrame containing expenses data with a 'Categoria' column.

    Returns:
        dict[str, list[str]]: A dictionary of unique category names and their subcategories.
    """
    categories = df["Categoria"].unique().tolist()
    categories_json = {}
    for category in categories:
        subcategories = df[df["Categoria"] == category]["Subcategoria"].unique().tolist()
        categories_json[category] = subcategories
    return categories_json
    
@tool
def fetch_sum_expenses_by_category_subcategory_and_year(df: pd.DataFrame, category: str, subcategory: str, year: int) -> tuple[float, float]:
    """
    Extracts and returns a tuple of the sum of expenses and the sum of real expenses for a specific category, subcategory, and year.
    The expenses (column 'Precio') are the expenses that have happened.
    The real expenses (column 'Price real') are the expenses that have happened but the price has been affected by the company cover (column 'Cobee cover 40') or because it ahs been shared with the partner.

    Args:
        df (pd.DataFrame): The pandas DataFrame containing expenses data.
        category (str): The category to filter by in the 'Categoria' column.
        subcategory (str): The subcategory to filter by in the 'Subcategoria' column.
        year (int): The year to filter by in the 'year' column.

    Returns:
        tuple[float, float]: A tuple of the sum of expenses and the sum of real expenses for the specified category, subcategory, and year.
    """

    if category not in df["Categoria"].unique().tolist():
        return "Category not found"
    if subcategory not in df[df["Categoria"] == category]["Subcategoria"].unique().tolist():
        return "Subcategory not found"
    if year not in df["year"].unique().tolist():
        return "Year not found"

    filtered_df = df[(df["Categoria"] == category) & (df["Subcategoria"] == subcategory) & (df["year"] == year)]
    sum_price = filtered_df["Precio"].sum()
    sum_real_price = filtered_df["Price real"].sum()
    return sum_price, sum_real_price

@tool
def get_expenses_of_all_categories_and_subcategories_per_year(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a pandas DataFrame with the expenses of all categories and subcategories per year.

    Args:
        df (pd.DataFrame): The pandas DataFrame containing expenses data.

    Returns:
        pd.DataFrame: A pandas DataFrame with the expenses of all categories and subcategories.
    """
    return df.groupby(["Categoria", "Subcategoria", "year"]).sum().reset_index()