# Cognitive Walkthrough: Saturn Server via saturn-ai Package (Sysadmin/IT)
# Each step is documented as a bullet point below.
#
# PREREQUISITE STEPS (shared with traditional):
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
# SATURN PACKAGE SETUP STEPS:
#
# - pip install saturn-ai
# - Import ServiceConfig and its sub-configs from saturn.config
# - Import run_service from saturn.runner
# - Import load_dotenv from dotenv and call it to load .env
# - Create a ServiceConfig object with:
#   - name="openrouter"
#   - deployment="cloud"
#   - api_type="openai"
#   - priority=50
#   - upstream base_url pointing to OpenRouter
#   - upstream api_key_env referencing OPENROUTER_API_KEY
# - Call run_service(config) which internally:
#   - finds an available port
#   - creates a FastAPI app with /v1/health, /v1/models, /v1/chat/completions
#   - registers on mDNS via SaturnAdvertiser
#   - starts uvicorn
#
# Prerequisite steps: 8
# Saturn code steps: 6
# Grand total: 14
#
# Compare to cog_saturn.py (manual): 8 prerequisites + 18 code = 26 total
# Compare to cog_traditional.py: 8 prerequisites + 4 distribution = 12 total
#   (but no centralized service, no discovery, no proxy)
#
# NOTE: The package also supports a one-liner CLI:
#   $ saturn openrouter
# Which uses the built-in openrouter.toml config. That's effectively 1 step
# (after pip install saturn-ai and setting the env var).

from dotenv import load_dotenv
from saturn.config import ServiceConfig, UpstreamConfig
from saturn.runner import run_service

load_dotenv()

config = ServiceConfig(
    name="openrouter",
    deployment="cloud",
    api_type="openai",
    priority=50,
    upstream=UpstreamConfig(
        base_url="https://openrouter.ai/api/v1",
        api_key_env="OPENROUTER_API_KEY",
    ),
)

if __name__ == "__main__":
    run_service(config)
