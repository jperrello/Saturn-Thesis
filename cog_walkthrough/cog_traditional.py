# Cognitive Walkthrough: Traditional AI Setup (Sysadmin/IT)
# Each step is documented as a bullet point below.
#
# PREREQUISITE STEPS (shared with Saturn):
#
# - Go to openrouter.ai (or any other API key provisioner)
# - Create an account and sign in
# - Go to settings
# - Click API keys
# - Create a new key
# - Copy key and store it somewhere safe
# - Create a .env file
# - Place key in file as OPENROUTER_API_KEY
#
# --- Saturn and traditional methods diverge here ---
#
# TRADITIONAL DISTRIBUTION STEPS:
#
# - Send the API key to each developer who needs access
#   (via email, Slack, shared document, password manager, etc.)
# - Communicate the API provider's endpoint URL to developers
#   (e.g. https://openrouter.ai/api/v1)
# - Communicate usage guidelines, rate limits, and cost expectations
# - For each additional team or project that needs a separate key,
#   repeat prerequisite steps 4-8 (create, copy, store, distribute)
#
# Prerequisite steps: 8
# Distribution steps: 4
# Grand total: 12
#
# NOTE: There is no centralized service, no discovery mechanism, and no proxy.
# Each developer independently:
#   - Stores the key in their own project
#   - Configures the endpoint URL and auth headers
#   - Handles errors, retries, and rate limiting themselves
#
# The sysadmin has:
#   - No visibility into usage across teams
#   - No way to revoke one developer's access without rotating the key for everyone
#   - No unified logging or monitoring
#   - No centralized failover or load balancing
#
# Compare to cog_saturn.py: 8 prerequisites + 18 code steps = 26 total
#   (but produces a centralized service with mDNS discovery)
# Compare to cog_sat_package.py: 8 prerequisites + 6 code steps = 14 total
#   (same outcome as manual Saturn, less code)

# The code below shows what a developer receiving the key would write:

# Step 1: Install the openai and dotenv packages
#   - `pip install openai python-dotenv`

# Step 2: Import os to access environment variables
import os

# Step 3: Import and call load_dotenv to load the .env file
from dotenv import load_dotenv

load_dotenv()

# Step 4: Read the API key from the environment variable
#   - The developer must have previously set OPENROUTER_API_KEY in .env
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
