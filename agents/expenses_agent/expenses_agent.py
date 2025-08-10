from smolagents import CodeAgent, tool
from .expenses_tools import (
    fetch_expenses_data_filtered_by_conditions,
    fetch_available_categories_and_subcategories,
    group_data_filtered_by_conditions,
    fetch_available_events
)
from utils.dataframe_tools import (
    get_dataframe_schema,
    get_numeric_column_properties,
)
from utils.load_model import model

agent = CodeAgent(
    tools=[
        fetch_expenses_data_filtered_by_conditions,
        fetch_available_categories_and_subcategories,
        group_data_filtered_by_conditions,
        get_dataframe_schema, get_numeric_column_properties,
        fetch_available_events
    ],
    model=model
)

@tool
def use_expenses_agent(query: str) -> str:
    """Handle user queries about expenses and provide insights.
    
    This function processes questions about expenses and provides detailed answers
    using available data and tools.
    
    Args:
        query (str): The user's question or query about expenses.
            Example: "How much did I spend on groceries last month?"
            
    Returns:
        str: A detailed response to the user's query about expenses.
    """
    return agent.run(f"""
    Use the available tools to answer the user’s query:  
    **{query}**

    Start by using the tools **`fetch_available_categories_and_subcategories`** and **`fetch_available_events`** to get the exact names of categories, subcategories, or events. This is important because these names are case sensitive and may be in Spanish.

    Before applying filters with other tools, always try to narrow down your search by year, category, subcategory, event, or a combination of these. Make sure you know the exact filter values.

    Use both **Categoria** and **Subcategoria** to filter by a certain type of expense, but not both at the same time. For example, if you want to find expenses related to cats, you will see there is a category called **"cats"** and three subcategories: **"cat litter"**, **"cat food"**, and **"veterinary"**. You can either filter by the **cats** category or filter by all three subcategories.

    If the query is unclear or you need more details, feel free to ask the user for clarification.

    When a tool returns a dataframe, it will have these columns:

    - **expected**: Whether the expense has occurred or is expected in the future  
    - **Applied date**: Date the expense was applied if different from the main date  
    - **Name**: Name of the expense  
    - **Precio**: Price of the expense  
    - **Is_compartido**: Indicates if the expense is shared with a partner (if yes, real price is 50%)  
    - **Categoria**: Expense category  
    - **Evento**: Related event, if any  
    - **size_cat**: Category size based on cost  
    - **Price real**: Actual price of the expense  
    - **date**: Date of the expense if 'Applied date' is empty  
    - **Comentarios**: Comments about the expense  
    - **URL**: URL linked to the expense, if any  
    - **Created**: Date the expense was created  
    - **tipo_especial**: Special expense type, if any  
    - **year**: Year of the expense  
    - **year_month**: Year and month of the expense  
    - **Subcategoria**: Subcategory of the expense  
    - **is_cost_of_living**: Indicates if it is a cost of living expense  
    - **Cobee cover 40**: Portion of the expense covered by the company

    Follow these steps to respond:

    1. Identify and confirm the relevant category, subcategory, event, and year using the initial fetch tools.  
    2. Build appropriate filters with confirmed exact names and dates before querying detailed data.  
    3. Use all gathered data to provide a clear, thorough, and well-explained answer to the user’s question.  
    4. Include in your response a detailed explanation of the steps you took to arrive at the final answer.

    """)
