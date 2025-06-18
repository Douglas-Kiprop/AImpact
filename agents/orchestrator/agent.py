from .aimpact_super_agent import AImpactSuperAgent

def create_agent():
    """Creates and returns an instance of the AImpactSuperAgent."""
    return AImpactSuperAgent()

# (Optional) Add a main function for local testing or direct script execution
if __name__ == "__main__":
    agent = create_agent()
    print("AImpactSuperAgent loaded successfully via agent.py.")
    # Example of interacting with the agent if run directly:
    # try:
    #     response = agent.chat("Hello from agent.py test!")
    #     print(f"Agent response: {response.text}")
    # except Exception as e:
    #     print(f"Error during agent.py test: {e}")