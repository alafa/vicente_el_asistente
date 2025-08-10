import pandas as pd
import numpy as np

from smolagents import tool


@tool
def aggregate_data(df: pd.DataFrame, group_fields: list[str], numeric_field: str, agg_func: str = "sum") -> pd.DataFrame:
    """
    Aggregates data in a flat DataFrame (from Notion or similar).

    Args:
        df (pd.DataFrame): DataFrame with data to aggregate.
        group_fields (list[str]): Columns to group by.
        numeric_field (str): Numeric column to aggregate.
        agg_func (str): Aggregation function: 'sum', 'max', 'min', 'avg' or 'mean'.

    Returns:
        pd.DataFrame: DataFrame with aggregated results.
    """
    agg_map = {
        "sum": "sum",
        "max": "max",
        "min": "min",
        "avg": "mean",
        "mean": "mean"
    }

    if agg_func not in agg_map:
        raise ValueError(f"Aggregation function not supported: {agg_func}")

    result = (
        df.groupby(group_fields, dropna=False)[numeric_field]
        .agg(agg_map[agg_func])
        .reset_index()
    )

    return result

@tool
def get_dataframe_schema(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns the schema of a pandas DataFrame:
    columns, data types and count of non-null values.

    Args:
        df (pd.DataFrame): DataFrame to inspect.

    Returns:
        pd.DataFrame: DataFrame with columns: name, dtype, non_null_count.
    """
    schema_data = []
    for col in df.columns:
        schema_data.append({
            "column": col,
            "dtype": str(df[col].dtype),
            "non_null_count": df[col].notnull().sum()
        })

    return pd.DataFrame(schema_data)


@tool
def get_numeric_column_properties(df: pd.DataFrame, numeric_column_name: str) -> dict:
    """
    Returns detailed information about a numeric column.
    
    Args:
        df (pd.DataFrame): DataFrame with the data.
        numeric_column_name (str): Name of the column to analyze.
    
    Returns:
        dict: Descriptive information.
    """
    if numeric_column_name not in df.columns:
        raise ValueError(f"Column '{numeric_column_name}' not found in DataFrame.")

    col = df[numeric_column_name]

    if pd.api.types.is_numeric_dtype(col):
        # If numeric → statistics
        return {
            "type": str(col.dtype),
            "count": col.count(),
            "min": col.min(),
            "max": col.max(),
            "mean": col.mean(),
            "median": col.median(),
            "variance": col.var(),
            "std_dev": col.std()
        }
    else:

        return {"error": "Column is not numeric"}


@tool
def filter_dataframe_comparisons(df: pd.DataFrame, conditions: dict[str, dict[str, int]]) -> pd.DataFrame:
    """
    Filters a DataFrame according to comparison conditions for each column.
    
    Args:
        df (pd.DataFrame): DataFrame to filter.
        conditions (dict): Dictionary where keys are column names and values are
                           dictionaries with operators and values.
                           Supported operators:
                            - 'eq'  : equal
                            - 'neq' : not equal
                            - 'gt'  : greater than
                            - 'gte' : greater than or equal to
                            - 'lt'  : less than
                            - 'lte' : less than or equal to

                            Example: conditions = {
                                "Price": {"gte": 100, "lt": 500},
                                "year": {"eq": 2023}
                            }

    Returns:
        pd.DataFrame: DataFrame filtered.
    """
    filtered_df = df.copy()
    
    ops = {
        "eq": lambda col, val: col == val,
        "neq": lambda col, val: col != val,
        "gt": lambda col, val: col > val,
        "gte": lambda col, val: col >= val,
        "lt": lambda col, val: col < val,
        "lte": lambda col, val: col <= val,
    }
    
    for col, cond in conditions.items():
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in DataFrame.")
        for op, val in cond.items():
            if op not in ops:
                raise ValueError(f"Operator '{op}' not supported.")
            filtered_df = filtered_df[ops[op](filtered_df[col], val)]
            
    return filtered_df
