from flask import Flask, request, jsonify, Response
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

AGENT_ENGINE_QUERY_URL = os.environ.get("AGENT_ENGINE_QUERY_URL")

@app.route('/query-agent', methods=['POST'])
def query_agent():
    if not AGENT_ENGINE_QUERY_URL:
        app.logger.error("AGENT_ENGINE_QUERY_URL environment variable not set.")
        return jsonify({"error": "AGENT_ENGINE_QUERY_URL environment variable not set."}), 500

    try:
        credentials, project = google.auth.default()
        auth_req = google.auth.transport.requests.Request()
        credentials.refresh(auth_req)
        access_token = credentials.token

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        frontend_data = request.json
        user_query = frontend_data.get("query")
        if not user_query:
            return jsonify({"error": "Missing 'query' in request."}), 400

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

        app.logger.info("Sending streaming request to Agent Engine URL: %s", AGENT_ENGINE_QUERY_URL)
        app.logger.info("Sending to Agent Engine Body:\n%s", json.dumps(agent_request_body, indent=2))

        def generate():
            try:
                # Make the request to the Agent Engine with stream=True
                with requests.post(AGENT_ENGINE_QUERY_URL, headers=headers, json=agent_request_body, stream=True) as response:
                    response.raise_for_status()

                    # This is for accumulating the full response content for logging, if needed
                    full_response_content = ""
                    tool_code_buffer = "" # Buffer for collecting tool code

                    for chunk in response.iter_content(chunk_size=None): # Use None for line by line or small chunks
                        if chunk:
                            try:
                                # Agent Engine sends multiple JSON objects separated by newlines
                                # We need to split and process each JSON object
                                for line in chunk.decode('utf-8').splitlines():
                                    if line.strip(): # Ensure line is not empty
                                        json_data = json.loads(line)
                                        # app.logger.debug("Received chunk: %s", json.dumps(json_data)) # Log each chunk received

                                        full_response_content += line + "\n" # Accumulate for full response logging

                                        # Handle different types of events from the Agent Engine
                                        # Tool invocation (e.g., when 'actions' and 'tool_code' are present)
                                        if 'actions' in json_data and 'tool_code' in json_data['actions']:
                                            tool_code_buffer += json_data['actions']['tool_code']
                                            # If tool_code is a complete snippet, yield it
                                            if '\n' in tool_code_buffer: # Heuristic: if a newline, consider it a complete chunk
                                                yield f"data: {json.dumps({'type': 'tool_code', 'content': tool_code_buffer.strip()})}\n\n"
                                                tool_code_buffer = "" # Reset buffer
                                        # Tool result (e.g., when 'tool_result' is present)
                                        elif 'tool_result' in json_data:
                                            tool_result = json_data['tool_result'].get('content', '')
                                            yield f"data: {json.dumps({'type': 'tool_result', 'content': tool_result})}\n\n"
                                        # Content/text parts
                                        elif 'content' in json_data and 'parts' in json_data['content']:
                                            for part in json_data['content']['parts']:
                                                if 'text' in part:
                                                    yield f"data: {json.dumps({'type': 'text', 'content': part['text']})}\n\n"
                                                # Handle other modalities if necessary (e.g., 'image_data')
                                        # Handle cases where the model might indicate it's thinking or processing
                                        elif 'metadata' in json_data and 'reasoning_mode' in json_data['metadata']:
                                            # You can send a special event for 'thinking' state
                                            yield f"data: {json.dumps({'type': 'thinking', 'content': 'Agent is thinking...'})}\n\n"
                                        # For end of stream or other relevant metadata
                                        elif 'usage_metadata' in json_data:
                                            # This might be the final chunk or metadata. You can send an 'end' event.
                                            pass # Or yield f"data: {json.dumps({'type': 'end'})}\n\n"

                            except json.JSONDecodeError as e:
                                app.logger.error(f"JSON Decode Error in chunk: {e} - Raw chunk: {chunk.decode('utf-8')}")
                                # It's possible a chunk doesn't contain a full JSON line.
                                # For robustness, you might need a more sophisticated JSON stream parser.
                                # For this example, we'll try to process line by line.
                            except Exception as e:
                                app.logger.error(f"Error processing chunk: {e}")
                                yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

                app.logger.info("Full Raw Response from Agent Engine (after stream close):\n%s", full_response_content)

            except requests.exceptions.RequestException as e:
                app.logger.error(f"Request error to Agent Engine: {e}")
                yield f"data: {json.dumps({'type': 'error', 'content': f'Network error communicating with Agent Engine: {e}'})}\n\n"
            except Exception as e:
                app.logger.error(f"Unhandled error during streaming: {e}")
                yield f"data: {json.dumps({'type': 'error', 'content': f'An unexpected error occurred: {e}'})}\n\n"
            finally:
                yield f"data: {json.dumps({'type': 'end'})}\n\n" # Signal end of stream

        return Response(generate(), mimetype='text/event-stream')

    except Exception as e:
        app.logger.error(f"Error preparing Agent Engine request: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.logger.setLevel('DEBUG')
    app.run(host='0.0.0.0', port=8080)