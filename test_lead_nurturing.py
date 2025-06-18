import asyncio
from agents.tools.lead_nurturing_tool import send_lead_for_nurturing, LeadNurturingInputs

async def main():
    sample_inputs = LeadNurturingInputs(
        full_name="Alice Johnson",
        email="alice.johnson@examplecorp.com",
        company="Innovate Solutions Inc.",
        job_title="Head of Product Development",
        company_website="https://innovatesolutions.com",
        pain_points="Struggling with integrating disparate data sources and slow reporting.",
        lead_source="LinkedIn"
    )

    print("Sending lead information...")
    print(f"Attempting to activate webhook for: {sample_inputs.full_name} from {sample_inputs.company}")
    result = await send_lead_for_nurturing(sample_inputs)
    print(f"Status: {result.status}")
    print(f"Message: {result.message}")

if __name__ == "__main__":
    asyncio.run(main())