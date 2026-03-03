# Suggested Commands

## Running
```bash
python cog_saturn.py     # Run Saturn server
python cog_traditional.py  # Run traditional setup
```

## Dependencies
```bash
pip install fastapi uvicorn python-dotenv httpx zeroconf
```

## System (Darwin)
```bash
dns-sd -B _saturn._tcp local.  # Browse Saturn services
dns-sd -R "Name" _saturn._tcp local 8080 "key=val"  # Register service
```
