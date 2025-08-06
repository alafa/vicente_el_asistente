from smolagents import CodeAgent, tool
from .tools import fetch_data, fetch_available_categories_and_subcategories, get_expenses_of_all_categories_and_subcategories_per_year
from utils.load_model import model

agent = CodeAgent(
    tools=[fetch_data, fetch_available_categories_and_subcategories, get_expenses_of_all_categories_and_subcategories_per_year],
    model=model
)

@tool
def use_expenses_agent(query: str) -> str:
    """
    Uses the expenses agent to answer questions and give expenses insights using the data available.

    Args:
        query: The query to be answered

    Returns:
        str: The answer to the query
    """

    return agent.run(f"""
    Use the available tools to answer the user query.
    The query is: {query}
    You probably need first to get the data from the data folder using the fetch_data tool.

    The file has these columns:
    expected - if the expense has happened or it is expected ihe future
    Applied date - Date of the expense if different from date
    Name - Name of the expense
    Precio - Price of the expense
    Is_compartido - If the expense is shared with partner. Is so, real price is 50%.
    Categoria - Category of the expense
    Evento - Event of the expense if any
    size_cat - Size of the category based on its cost
    Price real - Real price of the expense
    date - Date of the expense if 'Applied date' is empty
    Comentarios - Comments about the expense
    URL - URL of the expense if any
    Created - Date when the expense was created
    tipo_especial - Special type of expense if any
    year - Year of the expense
    year_monrh - Year and month of the expense
    Subcategoria - Subcategory of the expense
    is_cost_of_living - If the expense is a cost of living
    Cobee cover 40 - How many of the expense is covered by the company. Real price is affected by this as its subracts this amount from the price. Example: Is price is 50€ and 'Cobee cover 40' is 30, then the real price is 50 - 30 = 20€.

    Take the necesary steps to answer the user query. If the user asks about a specific category or subcategory, look into the available names and pick the ones that could match.
    Keep in mind the categories and subcategories are case sensitive and they could be written in spanish.
    Give a clear and detailed answer.
    """
    )

