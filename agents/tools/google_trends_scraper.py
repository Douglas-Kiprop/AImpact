import os
import httpx
from google.adk.tools import FunctionTool

async def google_trends_scraper(output_filename: str = "google_trends_output.csv") -> str:
    """
    Triggers an n8n workflow to scrape Google Trends data and saves the output to a CSV file.
    This tool does not send any payload to the n8n webhook, it merely triggers the workflow.
    It expects a CSV response from the n8n webhook.
    """
    n8n_webhook_url = os.getenv("N8N_GTRENDS_WEBHOOK_URL")
    n8n_api_key = os.getenv("N8N_GTRENDS_WEBHOOK_API_KEY")

    if not n8n_webhook_url:
        raise ValueError("N8N_GTRENDS_WEBHOOK_URL environment variable not set.")
    if not n8n_api_key:
        raise ValueError("N8N_GTRENDS_WEBHOOK_API_KEY environment variable not set.")

    headers = {
        "Authorization": n8n_api_key, # Corrected: Send API key directly as Authorization header
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(n8n_webhook_url, headers=headers, timeout=160.0)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx responses
            
            # Save the content to a CSV file
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(response.text)
            
            return f"CSV data saved to {output_filename}"
    except httpx.RequestError as exc:
        return f"An error occurred while requesting {exc.request.url!r}: {exc}"
    except httpx.HTTPStatusError as exc:
        return f"Error response {exc.response.status_code} while requesting {exc.request.url!r}: {exc.response.text}"

# --- CORRECTED INITIALIZATION ---
google_trends_scraper_tool = FunctionTool(func=google_trends_scraper)