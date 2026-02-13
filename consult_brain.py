import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

# Basic checking to ensure we can run
try:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env")
        sys.exit(1)
except Exception as e:
    print(f"Error loading environment: {e}")
    sys.exit(1)

client = OpenAI(api_key=api_key)

def read_plan():
    try:
        with open(r"C:\Users\Mudi\.gemini\antigravity\brain\37fe8936-b1c8-4a04-9fc1-2d8d1fe17059\implementation_plan.md", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading plan: {e}")
        sys.exit(1)

def consult_brain(plan_content):
    prompt = f"""
    You are the "External Brain" and Lead Architect for an autonomous AI system.
    Review the following Implementation Plan for an "Autonomous Digital Asset Ecosystem".
    
    The User's Constraints:
    1.  Weak local hardware (optimize for cloud/API).
    2.  High automation.
    3.  Python-based.
    4.  Modular architecture.
    
    The Plan:
    {plan_content}
    
    Your Task:
    Critique this plan. 
    1.  Identify any missing critical components for a truly *autonomous* loop.
    2.  Suggest one specific optimization to reduce local compute further.
    3.  Approve the plan if it is solid, or list aggressive changes if needed.
    
    Format your response as markdown.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a critical, efficiency-obsessed AI architect."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error consulting OpenAI: {e}")
        return None

if __name__ == "__main__":
    print("Reading plan...")
    plan = read_plan()
    print("Consulting Brain...")
    critique = consult_brain(plan)
    if critique:
        print("\n--- BRAIN CRITIQUE ---\n")
        print(critique)
        # Save to a file so we can read it easily
        with open("plan_critique.md", "w", encoding="utf-8") as f:
            f.write(critique)
    else:
        print("Failed to get critique.")
