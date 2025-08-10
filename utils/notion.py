import os
from notion_client import Client
from dotenv import load_dotenv
import pandas as pd
import numpy as np


load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")

DATABASE_IDS = {
    "expenses": os.getenv("NOTION_EXPENSES_DATABASE_ID")
}

def extract_notion_values(prop):
    prop_type = prop.get("type")
    if prop_type == "title":
        return "".join([t["plain_text"] for t in prop["title"]])
    elif prop_type == "rich_text":
        return "".join([t["plain_text"] for t in prop["rich_text"]])
    elif prop_type == "select":
        return prop["select"]["name"] if prop["select"] else None
    elif prop_type == "multi_select":
        return [s["name"] for s in prop["multi_select"]]
    elif prop_type == "checkbox":
        return prop["checkbox"]
    elif prop_type == "number":
        return prop["number"]
    elif prop_type == "date":
        return prop["date"]["start"] if prop["date"] else None
    elif prop_type == "formula":
        formula_type = prop["formula"]["type"]
        return prop["formula"][formula_type]
    elif prop_type in ("created_time", "last_edited_time"):
        return prop[prop_type]
    elif prop_type == "url":
        return prop["url"]
    else:
        return None


def get_notion_data(database_id: str) -> pd.DataFrame:
    """
    Returns a pandas DataFrame with the expenses of all categories and subcategories per year.

    Returns:
        pd.DataFrame: A pandas DataFrame with the expenses of all categories and subcategories.
    """
    notion = Client(auth=NOTION_TOKEN)
    database_id = DATABASE_IDS[database_id]

    all_results = []
    has_more = True
    start_cursor = None

    while has_more:
        kwargs = {"database_id": database_id}
        if start_cursor:
            kwargs["start_cursor"] = start_cursor

        response = notion.databases.query(**kwargs)
        all_results.extend(response["results"])

        has_more = response.get("has_more", False)
    start_cursor = response.get("next_cursor", None)

    flat_rows = []
    for page in all_results:  # results = client.databases.query(...)
        props = page["properties"]
        flat_row = {name: extract_notion_values(value) for name, value in props.items()}
        flat_rows.append(flat_row)

    df = pd.DataFrame(flat_rows)

    return df


def get_notion_property_options(database_id: str, property_name: str) -> list[str]:
    notion = Client(auth=NOTION_TOKEN)
    database_id = DATABASE_IDS[database_id]

    database = notion.databases.retrieve(database_id=database_id)

    property_info = database['properties'][property_name]


    if property_info['type'] == 'select':
        options = property_info['select']['options']
    elif property_info['type'] == 'multi_select':
        options = property_info['multi_select']['options']
    else:
        options = None

    return options