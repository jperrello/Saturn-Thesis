"""
Total configuration steps: 4
"""

# Step 1: Install the saturn-ai and openai packages
#   - `pip install saturn-ai openai`

# Step 2: Import discover and select_best_service from saturn
from saturn import discover, select_best_service

# Step 3: Import the OpenAI client from the openai package
from openai import OpenAI

# Step 4: Discover AI services on the local network and pick the best one
#   - No API key needed, no environment variable to set, no .env file to manage
services = discover()
best = select_best_service(services)

# Create the client pointed at the discovered endpoint (api_key is unused)
client = OpenAI(base_url=best.effective_endpoint, api_key="unused")

# Prompt the user for their favorite food
food = input("What is your favorite food? ")

# Use the client to generate a roast
response = client.chat.completions.create(
    model=best.models[0],
    messages=[
        {"role": "system", "content": "You are a brutal food critic. Roast the user for their favorite food choice in 2-3 sentences."},
        {"role": "user", "content": f"My favorite food is {food}"},
    ],
)

print(response.choices[0].message.content)
