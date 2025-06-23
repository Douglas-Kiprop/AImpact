import os
import requests
import json

def get_reddit_content_ideas(keywords: str, subreddits: str):
    """
    Fetches content ideas from Reddit based on keywords and subreddits using an n8n webhook.

    Args:
        keywords (str): A comma-separated string of keywords.
        subreddits (str): A comma-separated string of subreddits.

    Returns:
        list: A list of content ideas, or an empty list if an error occurs.
    """
    webhook_url = os.getenv("N8N_REDDIT_CONTENT_IDEA_WEBHOOK_URL")
    if not webhook_url:
        print("Error: N8N_REDDIT_CONTENT_IDEA_WEBHOOK_URL not set in .env file.")
        return []

    # Clean subreddits by removing 'r/' prefix if present
    cleaned_subreddits = ",".join([s.strip().replace("r/", "") for s in subreddits.split(',')])

    payload = {
        "Keyword": keywords,
        "Subreddit": cleaned_subreddits
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Reddit content ideas: {e}")
        return []

if __name__ == "__main__":
    # Example usage for testing
    print("Testing Reddit Content Idea Scraper...")
    # Make sure to set N8N_REDDIT_CONTENT_IDEA_WEBHOOK_URL in your .env for this to work
    # For testing, you might temporarily hardcode the URL or ensure your .env is loaded

    # Mock data for testing
    test_keywords = "farming"
    test_subreddits = "r/agriculture" # Changed to include r/ for testing the cleaning logic

    ideas = get_reddit_content_ideas(test_keywords, test_subreddits)

    if ideas:
        print("Successfully fetched content ideas:")
        for i, idea in enumerate(ideas):
            print(f"\n--- Idea {i+1} ---")
            for key, value in idea.items():
                print(f"{key}: {value}")
    else:
        print("Failed to fetch content ideas or no ideas returned.")