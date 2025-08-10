from agents.expenses_agent.expenses_tools import fetch_expenses_data_filtered_by_conditions


conditions = {'year': {'eq': 2024}, 'Categoria': {'eq': 'Viajes'}}

print(fetch_expenses_data_filtered_by_conditions(conditions))