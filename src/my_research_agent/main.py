#!/usr/bin/env python
import sys
import warnings
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import your Crew class
try:
    from my_research_agent.crew import MyResearchAgent
except ImportError:
    print("\n[!] Error: Could not find 'my_research_agent'.")
    print("Ensure you are running the script with the correct PYTHONPATH.")
    sys.exit(1)

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the multi-agent crew and handle structured Pydantic output.
    """
    print("\n" + "="*60)
    print("      BFSI STRATEGIC MARKET INTELLIGENCE SYSTEM (2026)")
    print("="*60 + "\n")

    # Capture the product concept
    product_concept = input("Enter the product_concept: ")

    if not product_concept.strip():
        print("Error: Product concept cannot be empty.")
        return

    inputs = {
        'product_concept': product_concept,
        'current_year': str(datetime.now().year)
    }

    print(f"\n[🚀] Launching Multi-Agent Team for: '{product_concept}'...\n")

    try:
        # Kickoff the crew execution
        result = MyResearchAgent().crew().kickoff(inputs=inputs)
        
        # Access the structured Pydantic object
        # This handles the data from your models.py
        data = result.pydantic
        
        print("\n" + "="*60)
        print(f"            FINAL STRATEGIC REPORT: {data.product_concept.upper()}")
        print("="*60)
        
        print("\nTOP COMPETITOR ANALYSIS:")
        for comp in data.top_competitors:
            print(f"\n📍 {comp.name}")
            print(f"   - Value Proposition: {comp.value_proposition}")
            print(f"   - Identified Weakness: {comp.weakness}")
            
        print(f"\n🎯 MARKET WHITE SPACE OPPORTUNITY:")
        print(f"   {data.market_white_space}")
        print("\n" + "="*60)

        # Enterprise Tooling: Permanent JSON Export
        export_filename = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(export_filename, 'w') as f:
            json.dump(data.model_dump(), f, indent=4)
            
        print(f"\n[✅] Success! Data exported to: {export_filename}")
        
    except Exception as e:
        print(f"\n[❌] An error occurred during crew execution: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "product_concept": "Generic Product",
        'current_year': str(datetime.now().year)
    }
    try:
        MyResearchAgent().crew().train(
            n_iterations=int(sys.argv[1]), 
            filename=sys.argv[2], 
            inputs=inputs
        )
    except Exception as e:
        print(f"An error occurred while training: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        MyResearchAgent().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        print(f"An error occurred while replaying: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "product_concept": "Generic Product",
        "current_year": str(datetime.now().year)
    }
    try:
        MyResearchAgent().crew().test(
            n_iterations=int(sys.argv[1]), 
            eval_llm=sys.argv[2], 
            inputs=inputs
        )
    except Exception as e:
        print(f"An error occurred while testing: {e}")

if __name__ == "__main__":
    run()