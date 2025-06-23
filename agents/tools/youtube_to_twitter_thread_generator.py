import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

N8N_YOUTUBE_TO_TWITTER_WEBHOOK_URL = os.getenv("N8N_YOUTUBE_TO_TWITTER_WEBHOOK_URL")

def generate_twitter_threads(
    keyword: str,
    target_audience: str,
    content_type: str
) -> dict:
    """
    Generates Twitter threads from a YouTube video using an n8n webhook.

    Args:
        keyword (str): The main keyword or topic of the YouTube video.
        target_audience (str): The intended audience for the Twitter threads.
        content_type (str): The style or type of content (e.g., "Educational", "Casual").

    Returns:
        dict: A dictionary containing the generated Twitter threads or an error message.
    """
    if not N8N_YOUTUBE_TO_TWITTER_WEBHOOK_URL:
        return {"error": "N8N_YOUTUBE_TO_TWITTER_WEBHOOK_URL environment variable not set."}

    payload = {
        "Keyword": keyword,
        "Target audience": target_audience,
        "Content type": content_type,
    }

    try:
        print(f"Attempting to send request to: {N8N_YOUTUBE_TO_TWITTER_WEBHOOK_URL}")
        print(f"Payload: {payload}")

        response = requests.post(N8N_YOUTUBE_TO_TWITTER_WEBHOOK_URL, json=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        return response.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.text}")
        return {"error": f"HTTP error: {http_err}", "details": response.text}
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
        return {"error": f"Connection error: {conn_err}"}
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
        return {"error": f"Timeout error: {timeout_err}"}
    except requests.exceptions.RequestException as req_err:
        print(f"An unexpected error occurred: {req_err}")
        return {"error": f"An unexpected error occurred: {req_err}"}


if __name__ == "__main__":
    # Example usage:
    # Ensure N8N_YOUTUBE_TO_TWITTER_WEBHOOK_URL is set in your .env file
    # For testing, you might temporarily set it like this if not using .env:
    # os.environ["N8N_YOUTUBE_TO_TWITTER_WEBHOOK_URL"] = "YOUR_TEST_WEBHOOK_URL_HERE"

    print("Testing YouTube to Twitter Thread Generator...")

    test_keyword = "AI in Healthcare"
    test_target_audience = "Healthcare Professionals"
    test_content_type = "Educational"

    result = generate_twitter_threads(test_keyword, test_target_audience, test_content_type)

    if "error" in result:
        print(f"Error: {result['error']}")
        if "details" in result:
            print(f"Details: {result['details']}")
    else:
        print("Successfully generated Twitter threads:")
        # Assuming the response contains thread_1_content, thread_2_content, thread_3_content
        if isinstance(result, dict):
            if "video_title" in result and "video_url" in result:
                print(f"\nVideo Title: {result['video_title']}")
                print(f"Video URL: {result['video_url']}")
                print(f"Video Views: {result.get('video_views', 'N/A')}")
                print(f"Video Channel: {result.get('video_channel', 'N/A')}")

            for i in range(1, 4): # Iterate from 1 to 3 for thread_1, thread_2, thread_3
                thread_content_key = f"thread_{i}_content"
                thread_title_key = f"thread_{i}_title"
                if thread_content_key in result:
                    print(f"\n--- Thread {i} ---")
                    if thread_title_key in result:
                        print(f"Title: {result[thread_title_key]}")
                    print(result[thread_content_key])
                else:
                    print(f"Thread {i} content not found in response.")
            
            if "generated_date" in result:
                print(f"\nGenerated Date: {result['generated_date']}")
            if "status" in result:
                print(f"Status: {result['status']}")

        else:
            print("Unexpected response format:")
            print(result)