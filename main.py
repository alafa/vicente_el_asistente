from smolagents import CodeAgent, WebSearchTool
from agents.encription_agent.encription_agent import use_encrypt_agent
from agents.expenses_agent.expenses_agent import use_expenses_agent
from utils.load_model import model

super_agent = CodeAgent(
    tools=[WebSearchTool(), use_encrypt_agent, use_expenses_agent],
    model=model,
    stream_outputs=False  # cambia a True si tienes soporte para streaming
)

# 3. Ejecuta
response = super_agent.run(input("What do you need??"))
print(response)