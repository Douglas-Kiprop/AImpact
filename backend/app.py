from flask import Flask, request, jsonify
from flask_cors import CORS
import google.auth
import google.auth.transport.requests
import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins for simplicity during development

# Environment variables for your Agent Engine details
# For local testing, you can hardcode the URL here.
# For deployment, ensure this is set as an environment variable in your deployment environment.
AGENT_ENGINE_QUERY_URL = os.environ.get("AGENT_ENGINE_QUERY_URL")

@app.route('/query-agent', methods=['POST'])
def query_agent():
    if not AGENT_ENGINE_QUERY_URL:
        return jsonify({"error": "AGENT_ENGINE_QUERY_URL environment variable not set."}), 500

    try:
        # Get credentials for Google Cloud
        credentials, project = google.auth.default()
        auth_req = google.auth.transport.requests.Request()
        credentials.refresh(auth_req)
        access_token = credentials.token

        # Prepare the request to the Agent Engine
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Forward the request body from the frontend directly to the Agent Engine
        frontend_data = request.json
        user_query = frontend_data.get("query")
        if not user_query:
            return jsonify({"error": "Missing 'query' in request."}), 400

        # Build the payload exactly like your working curl
        agent_request_body = {
            "class_method": "stream_query",
            "input": {
                "user_id": "test_user",
                "message": {
                    "parts": [{"text": user_query}],
                    "role": "user"
                }
            }
        }

        app.logger.info("Sending to Agent Engine URL: %s", AGENT_ENGINE_QUERY_URL)
        app.logger.info("Sending to Agent Engine Body:\n%s", json.dumps(agent_request_body, indent=2))

        # Make the request to the Agent Engine
        response = requests.post(AGENT_ENGINE_QUERY_URL, headers=headers, json=agent_request_body)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Log the raw response text before parsing
        raw_response = response.text
        app.logger.info("Raw Response from Agent Engine:\n%s", raw_response)

        # Attempt to parse the response as JSON
        agent_response_json = response.json()
        app.logger.info("Parsed Response from Agent Engine:\n%s", json.dumps(agent_response_json, indent=2))

        # Extract the 'text' from the Agent Engine's response and return it in a 'response' field
        agent_response_text = agent_response_json.get('content', {}).get('parts', [{}])[0].get('text', '')
        return jsonify({"response": agent_response_text})

    except Exception as e:
        app.logger.error(f"Error querying Agent Engine: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.logger.setLevel('DEBUG')
    app.run(host='0.0.0.0', port=8080)