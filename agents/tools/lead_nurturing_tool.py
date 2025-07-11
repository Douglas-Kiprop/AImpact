import os
import httpx # Keep httpx for async
from pydantic import BaseModel, Field
from typing import Literal
from google.adk.tools import FunctionTool
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

class LeadNurturingInputs(BaseModel):
    full_name: str = Field(..., description="Full name of the lead.")
    email: str = Field(..., description="Email address of the lead.")
    company: str = Field(..., description="Company name of the lead.")
    job_title: str = Field(..., description="Job title of the lead.")
    company_website: str = Field(..., description="Company website of the lead.")
    pain_points: str = Field(..., description="Pain points or challenges faced by the lead.")
    lead_source: str = Field(..., description="Source from which the lead was acquired (e.g., LinkedIn, Website, Referral).")

class LeadNurturingOutputs(BaseModel):
    status: Literal["success", "failure"] = Field(..., description="Status of the lead nurturing request.")
    message: str = Field(..., description="A message describing the outcome of the request.")

async def send_lead_for_nurturing(
    full_name: str,
    email: str,
    company: str,
    job_title: str,
    company_website: str,
    pain_points: str,
    lead_source: str
) -> LeadNurturingOutputs:
    """
    Sends lead information to an n8n webhook to initiate an AI-powered email nurturing sequence.
    """
    webhook_url = os.getenv("N8N_LEADNURTURE_WEBHOOK_URL")
    # api_key = os.getenv("N8N_LEADNURTURE_WEBHOOK_API_KEY") # <--- REMOVE OR COMMENT OUT THIS LINE if no API key is used

    if not webhook_url:
        return LeadNurturingOutputs(status="failure", message="N8N_LEADNURTURE_WEBHOOK_URL environment variable is not set.")

    payload = {
        "Full Name": full_name,
        "Email": email,
        "Company": company,
        "Job Title": job_title,
        "Company Website": company_website,
        "Pain Points / Challenges": pain_points,
        "Lead Source": lead_source,
    }

    # You don't need to explicitly set Content-Type: application/json here if using json=payload
    # httpx will handle it automatically.
    # headers = {
    #     "Content-Type": "application/json"
    # }
    
    try:
        async with httpx.AsyncClient() as client:
            # CHANGE 'data=payload' to 'json=payload'
            response = await client.post(webhook_url, json=payload, timeout=30.0)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

        return LeadNurturingOutputs(status="success", message=f"Lead information sent successfully. Response: {response.text}")
    except httpx.RequestError as exc:
        return LeadNurturingOutputs(status="failure", message=f"An error occurred while requesting {exc.request.url!r}: {exc}")
    except httpx.HTTPStatusError as exc:
        return LeadNurturingOutputs(status="failure", message=f"Error response {exc.response.status_code} while requesting {exc.request.url!r}: {exc.response.text}")
    except Exception as e:
        return LeadNurturingOutputs(status="failure", message=f"An unexpected error occurred: {e}")

lead_nurturing_tool = FunctionTool(func=send_lead_for_nurturing)