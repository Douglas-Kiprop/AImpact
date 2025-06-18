import asyncio
import os
from dotenv import load_dotenv

# Add the parent directory to the Python path to allow importing from agents.tools
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'agents')))

from tools.google_trends_scraper import google_trends_scraper

async def main():
    load_dotenv() # Load environment variables from .env file
    print("Attempting to trigger Google Trends n8n workflow...")
    try:
        result = await google_trends_scraper()
        print("\n--- Google Trends Scraper Output ---")
        print(result)
        print("------------------------------------")
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())