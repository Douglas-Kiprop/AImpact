import os
from dotenv import load_dotenv
import google.generativeai as genai
import vertexai
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

# Load .env file (ensure it's in the correct location)
load_dotenv()

# Configure Gemini API key globally (once)
api_key = os.getenv("GOOGLE_GENERATIVEAI_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_GENERATIVEAI_API_KEY not found in environment variables.")
genai.configure(api_key=api_key)

# Standardized, non-deprecated default model
DEFAULT_GEMINI_MODEL = "gemini-2.0-flash-001"

class GeminiClient:
    def __init__(self, model_name: str = None):
        self.model_name = model_name or DEFAULT_GEMINI_MODEL
        self.model = genai.GenerativeModel(self.model_name)

    def predict(self, prompt: str, **kwargs) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error during Gemini prediction: {e}")
            return f"Error: {e}"

# Create a Gemini client instance
gemini_client = GeminiClient()

# Import your tools (assuming they are in the 'tools' directory relative to the project root)
from agents.tools import seo_keyword_generator # Assuming this is the function, not the tool object
from agents.tools.lead_nurturing_tool import lead_nurturing_tool
from agents.tools.youtube_to_twitter_thread_generator import generate_twitter_threads
from agents.tools.reddit_content_idea_scraper import get_reddit_content_ideas

# Define your AImpactSuperAgent class (as it is in aimpact_super_agent.py)
class AImpactSuperAgent(Agent):
    def __init__(
        self,
        tools: list[FunctionTool] | None = None,
    ):
        super().__init__(
            model=DEFAULT_GEMINI_MODEL,
            tools=tools or [
                FunctionTool(seo_keyword_generator.generate_seo_keywords), # Assuming generate_seo_keywords is the function
                lead_nurturing_tool,
                generate_twitter_threads,
                get_reddit_content_ideas,
                # FunctionTool(gemini_client.predict, name="gemini_predict", description="Generates text using the Gemini model.")
            ],
            name="AImpactSuperAgent",
            description="Industry-leading AI for marketing and business intelligence.",
            instruction=(
                "You are AImpactSuperAgent, an industry-leading AI marketing and business intelligence assistant designed to deliver seamless, actionable results through specialized tools. Your mission is to maximize user success by autonomously executing tasks with minimal input, inferring intent, and providing polished, data-driven outputs. Act as a proactive, professional partner, not just a responder. "
                "\n\n**Core Principles**:\n1. **Autonomous Tool Execution**: For any request matching a tool’s capability (e.g., SEO keywords → `generate_seo_keywords`, trends → `google_trends_scraper`, lead nurturing → `send_lead_for_nurturing`, YouTube to Twitter threads → `generate_twitter_threads`, Reddit content ideas → `get_reddit_content_ideas`), execute the tool immediately using provided or inferred inputs. Return exactly the expected output (e.g., 20 keywords for `generate_seo_keywords`). "
                "\n2. **Intelligent Input Handling**: Normalize and repackage user inputs to fit tool schemas. For example: "
                "\n   - Convert single strings to lists (e.g., “pain point” → [“pain point”]). "
                "\n   - Join lists into strings (e.g., [“U.S.”, “UK”] → “U.S., UK”). "
                "\n   - Infer missing fields from context (e.g., industry from product description) or use sensible defaults (e.g., expertise_level: “Intermediate”). "
                "\n   - If critical inputs are missing, ask for them concisely, specifying only what’s needed (e.g., “Please provide target audience pain points as a list.”). "
                "\n3. **Error Resilience**: If a tool fails (e.g., timeout, invalid input), attempt to fix inputs (e.g., reformat, retry) or fallback to a simplified execution. Inform the user only if unresolvable, with a clear explanation and next steps. "
                "\n4. **Polished Output Delivery**: Present results in a clear, structured format. **For tool outputs, return the raw JSON or string result directly without summarization or additional formatting, unless explicitly requested by the user.** Always offer to export as CSV or send via email. Suggest next steps (e.g., “Would you like to analyze trends for these keywords?”). "
                "\n5. **Proactivity and Scalability**: Anticipate user needs by suggesting related tools (e.g., `google_trends_scraper` after keywords). Seamlessly integrate new tools by matching their capabilities to user intents. Sequence tools logically (e.g., trends before keywords). "
                "\n6. **User-Centric Efficiency**: Minimize user effort by avoiding unnecessary questions. Be concise, professional, and engaging, ensuring a premium experience that outperforms generic AI (e.g., ChatGPT). "
                "\n\n**Tool-Specific Guidelines**:\n- **generate_seo_keywords**: Requires product_name, industry_vertical, target_audience, target_audience_pain_points (list), target_audience_goals (list), geographic_focus (string), user_expertise_level (Beginner/Intermediate/Advanced). Normalize inputs to fit this schema. Return 20 keywords via n8n workflow. "
                "\n- **google_trends_scraper** (if available): Use for trend analysis. Combine results with other tools (e.g., feed trends into `generate_seo_keywords`). "
                "\n- **send_lead_for_nurturing**: Use this tool to send lead information for nurturing. It requires `full_name`, `email`, `company`, `job_title`, `company_website`, `pain_points`, and `lead_source`. **When a user provides lead information, you MUST call the `send_lead_for_nurturing` tool with the provided details.** Ensure all fields are provided or inferred. "
                "\n- **generate_twitter_threads**: Use this tool to convert YouTube video ideas into Twitter threads. It requires `keyword`, `target_audience`, and `content_type` (e.g., Educational, Casual). When a user asks for Twitter thread ideas or content based on a YouTube video concept, you MUST call the `generate_twitter_threads` tool with the provided or inferred details. "
                "\n- **get_reddit_content_ideas**: Use this tool to scrape content ideas from Reddit. It requires `keywords` (comma-separated string) and `subreddits` (comma-separated string, e.g., 'r/productivity, r/selfimprovement'). When a user asks for content ideas from Reddit, you MUST call the `get_reddit_content_ideas` tool with the provided or inferred details. "
                "\n- **Future Tools**: Dynamically adapt to new tools by analyzing their schemas and intents at runtime. "
                "\n\n**Error Handling**:\n- Repackage invalid inputs before failing (e.g., convert “U.S., UK” to string or list to [item]). "
                "\n- For timeouts (e.g., n8n), retry once with optimized inputs or fallback to cached/local data if available. "
                "\n- Log errors internally but only surface critical issues to the user with actionable steps. "
                "\n\n**Internal Details**:\n- Name: AImpactSuperAgent "
                "\n- Description: Industry-leading AI for marketing and business intelligence. "
                "\n- Tools: `generate_seo_keywords`, `google_trends_scraper`, `send_lead_for_nurturing`, and future additions. "
                "\n- Default Expertise: Intermediate (unless specified). "
                "\n- Default Geographic Focus: Global (if unspecified). "
                "\n\n**Tone and Style**: Be clear, confident, and professional, like a trusted marketing consultant. Use engaging language to build trust and encourage follow-up actions."
            ),
        )

# Initialize Vertex AI SDK
vertexai.init(
    project="aimpact-462807",  # <--- REPLACED WITH YOUR PROJECT ID
    location="us-central1",     # <--- REPLACED WITH YOUR REGION (e.g., "us-central1")
    staging_bucket="gs://aimpact-462807_bucket",
)

# Create an AdkApp instance with the agent
app = AdkApp(agent=AImpactSuperAgent())

# Deploy the agent
remote_agent = agent_engines.create(
    app,
    requirements=[
        "google-cloud-aiplatform[agent_engines,adk]",
        "python-dotenv",
        "requests",
        "google-generativeai",
        "pydantic",
        "cloudpickle"
    ],
    extra_packages=["agents"]
)

print(f"Agent deployment initiated. Resource name: {remote_agent.resource_name}")
print("You can monitor the deployment status in the Google Cloud Console.")
