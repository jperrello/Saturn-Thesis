# Cog Walkthrough Project

## Purpose
Cognitive walkthrough comparing traditional API key setup vs Saturn server setup. Every step must be documented as bullet points.

## Tech Stack
- Python
- dotenv for env vars
- FastAPI (for Saturn server)
- zeroconf / dns-sd for mDNS service discovery

## Structure
- `cog_traditional.py` - Traditional API key setup (load_dotenv + os.getenv)
- `cog_saturn.py` - Saturn server implementation (to be built)
- `.env` - Contains OPENROUTER_API_KEY
- `CLAUDE.md` - Project instructions (document every step as bullet points)

## Key Rules
- Document every step (function calls, imports, file creation)
- Use bullet points, not tables
- Follow CLAUDE.md coding conventions (no docstrings, single-word names, no else, inline single-use vars)
