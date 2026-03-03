# Cognitive Walkthrough: App Developer — Traditional AI Integration
# Each step is documented as a bullet point below.
#
# AI INTEGRATION STEPS:
#
# - Install the openai package
#   - `pip install openai`
# - Import the os module to access environment variables
# - Import the OpenAI client from the openai package
# - Receive API key from IT/sysadmin or obtain your own
#   (if obtaining your own, see prerequisite steps in cog_traditional.py)
# - Store the API key as an environment variable
#   (e.g. export OPENAI_API_KEY=sk-... in .bashrc or .env file)
# - Create an OpenAI client, passing the API key explicitly
#
# BILLING INTEGRATION STEPS (to pass AI costs to end users):
#
# - Go to stripe.com and create a Stripe account
# - Verify identity and/or business information
# - Create a product representing the AI feature or subscription
# - Define pricing tiers (free trial, monthly, annual, usage-based, etc.)
# - Install the Stripe SDK
#   - `pip install stripe`
# - Import stripe in the application
# - Store Stripe API keys (publishable + secret) in environment variables
# - Build a checkout/payment endpoint in the app
# - Integrate Stripe Checkout or build a custom payment form on the frontend
# - Set up a webhook endpoint to handle Stripe payment events
#   (subscription.created, payment_intent.succeeded, payment_intent.failed, etc.)
# - Implement subscription status checking to gate AI features behind active payment
# - Test the full payment flow in Stripe test mode
# - Switch to Stripe live mode for production
#
# AI integration steps: 6
# Billing integration steps: 13
# Grand total: 19
#
# Compare to app_dev_sat.py: 4 steps, no billing integration needed.
# Saturn eliminates the entire billing stack because AI costs are absorbed
# at the institutional level by the sysadmin.
# The app developer just discovers services on the network and uses them.
#
# NOTE: The billing integration (Stripe) code alone is typically 200-500 lines
# of additional application code, plus frontend payment UI, webhook handlers,
# and database tables for subscription state.
# This walkthrough counts the conceptual steps, not lines of code.

# Step 1: Install the openai package
#   - `pip install openai`

# Step 2: Import the os module to access environment variables
import os

# Step 3: Import the OpenAI client from the openai package
from openai import OpenAI

# Step 4: Read the API key from the environment variable
#   - The developer must have previously set OPENAI_API_KEY in their shell
#     (e.g. `export OPENAI_API_KEY=sk-...` in .bashrc, .zshrc, or a .env file)
api_key = os.environ["OPENAI_API_KEY"]

# Step 5: Create an OpenAI client, passing the API key explicitly
client = OpenAI(api_key=api_key)

# Step 6: Prompt the user for their favorite food
food = input("What is your favorite food? ")

# Use the client to generate a roast
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a brutal food critic. Roast the user for their favorite food choice in 2-3 sentences."},
        {"role": "user", "content": f"My favorite food is {food}"},
    ],
)

print(response.choices[0].message.content)
