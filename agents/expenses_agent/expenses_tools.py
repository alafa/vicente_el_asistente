from smolagents import tool
import pandas as pd
import utils.dataframe_tools as df_tools
import utils.notion as notion

@tool
def fetch_expenses_data_filtered_by_conditions(conditions: dict[str, dict[str, int]] = None) -> pd.DataFrame:
    """ 
    Filters the expenses data using the conditions provided.

    Args:
        conditions (dict, optional): Dictionary where keys are column names and values are
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
    data = notion.get_notion_data("expenses")
    if conditions is None:
        return data
    return df_tools.filter_dataframe_comparisons(data, conditions)



@tool
def group_data_filtered_by_conditions(group_fields: list[str], numeric_field: str, agg_func: str, conditions: dict[str, dict[str, int]] = None) -> pd.DataFrame:
    """ 
    Gets data filtered by the provided conditions and returns the data grouped by the provided columns and aggregated by the provided numeric field.

    Args:
        group_fields (list[str]): Columns to group by.
        numeric_field (str): Numeric column to aggregate.
        agg_func (str): Aggregation function: 'sum', 'max', 'min', 'avg' or 'mean'.
        conditions (dict, optional): Dictionary where keys are column names and values are
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
        pd.DataFrame: DataFrame grouped.
    """
    data = notion.get_notion_data("expenses")
    if conditions is None:
        filtered_data = data
    else:
        filtered_data = df_tools.filter_dataframe_comparisons(data, conditions)
    return df_tools.aggregate_data(filtered_data, group_fields, numeric_field, agg_func)



@tool
def fetch_available_categories_and_subcategories() -> dict[str, list[str]]:
    """
    Extracts and returns a dictionary of unique categories and subcategories from the expenses DataFrame.

    Args:
        None

    Returns:
        dict[str, list[str]]: A dictionary of unique category names and their subcategories.
    """

    response = "*Categories:* \n"
    category_options = notion.get_notion_property_options("expenses", "Categoria")
    for option in category_options:
        response += "- " + option['name'] + "\n"
    response += "\n*Subcategories:* \n"
    subcategory_options = notion.get_notion_property_options("expenses", "Subcategoria")
    for option in subcategory_options:
        response += "- " + option['name'] + "\n"
    return response


@tool
def fetch_available_events() -> dict[str, list[str]]:
    """
    Extracts and returns a dictionary of unique events from the expenses DataFrame.

    Args:
        None

    Returns:
        dict[str, list[str]]: A dictionary of unique events.
    """

    response = "*Events:* \n"
    event_options = notion.get_notion_property_options("expenses", "Evento")
    for option in event_options:
        response += "- " + option['name'] + "\n"
    return response