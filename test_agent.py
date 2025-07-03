import vertexai
from vertexai.preview import reasoning_engines
from vertexai import agent_engines

GOOGLE_CLOUD_PROJECT_ID = "aimpact-462807"
GOOGLE_CLOUD_LOCATION = "us-central1"
AGENT_ENGINE_RESOURCE_NAME = "projects/653465286381/locations/us-central1/reasoningEngines/4948303702294265856"

# Initialize Vertex AI
vertexai.init(project=GOOGLE_CLOUD_PROJECT_ID, location=GOOGLE_CLOUD_LOCATION)

# Retrieve the deployed Agent Engine using its resource name
try:
    engine = agent_engines.AgentEngine.get(AGENT_ENGINE_RESOURCE_NAME)
    print(f"Successfully loaded Agent Engine: {engine.display_name} ({engine.resource_name})")
except Exception as e:
    raise RuntimeError(f"Failed to load Agent Engine with resource name {AGENT_ENGINE_RESOURCE_NAME}: {e}")

# Create a session and interact with the agent
session = engine.start_session()
response = session.send_message("Your query here")
print(response)