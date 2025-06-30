# AImpact Super Agent

## Overview

The AImpact Super Agent is an AI-powered assistant designed to streamline marketing and business intelligence tasks. It leverages specialized tools to autonomously generate SEO keywords, nurture leads, create social media content, and scrape content ideas, aiming to deliver actionable results with minimal user input.

## Quick Start (Local Testing)

To quickly get a feel for the AImpact Super Agent, you can run it locally using the ADK Web interface:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-repo/AImpact.git
    cd AImpact
    ```

2.  **Set up your Python environment and install dependencies**:
    ```bash
    python -m venv .venv
    .venv\Scripts\Activate.ps1  # On Windows PowerShell
    # source .venv/bin/activate  # On Linux/macOS
    pip install -r requirements.txt
    ```

3.  **Configure your Gemini API Key**:
    Create a `.env` file in the project root and add your Google Generative AI API key:
    ```
    GOOGLE_GENERATIVEAI_API_KEY="your_gemini_api_key"
    ```

4.  **Run the ADK Web Agent Server**:
    ```bash
    adk web agents
    ```

5.  **Access the Web UI**: Open your browser to the address provided in the terminal (usually `http://localhost:8080`) and interact with the agent.

## What's Next?

We are actively working on deploying the AImpact Super Agent to Google Cloud Vertex AI's Agent Engines for broader accessibility and scalability.