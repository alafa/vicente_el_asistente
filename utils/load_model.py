from smolagents import OpenAIServerModel
import os
import time
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Please set the GEMINI_API_KEY in your .env file")

# The base model using Gemini-compatible OpenAI endpoint
base_model = OpenAIServerModel(
    model_id="gemini-2.0-flash",
    api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=GEMINI_API_KEY,
)

# Throttle wrapper
class ThrottledModel:
    def __init__(self, model, delay_seconds=12):
        self.model = model
        self.delay = delay_seconds

    def generate(self, *args, **kwargs):
        time.sleep(self.delay)
        return self.model.generate(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        # Optional: also allow model(prompt) calls with throttling
        time.sleep(self.delay)
        return self.model(*args, **kwargs)

# Export throttled model
model = ThrottledModel(base_model, delay_seconds=4.1)
