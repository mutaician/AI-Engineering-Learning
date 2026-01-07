# This doesn't work.


import os
import re
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment")

client = genai.Client(api_key=api_key)
MODEL_ID = "gemini-3-flash-preview"

SKILLS_DIR = "skills"

def list_skills() -> str:
    """Returns Metadata (Level 1) for all discovery by scanning the skills directory."""
    skills_metadata = []
    if not os.path.exists(SKILLS_DIR):
        return "No skills directory found."
        
    for skill_id in os.listdir(SKILLS_DIR):
        skill_path = os.path.join(SKILLS_DIR, skill_id)
        if os.path.isdir(skill_path):
            skill_md = os.path.join(skill_path, "SKILL.md")
            if os.path.exists(skill_md):
                with open(skill_md, "r") as f:
                    content = f.read()
                    match = re.search(r"---\n(.*?)\n---", content, re.DOTALL)
                    if match:
                        skills_metadata.append(f"Skill ID: {skill_id}\nMetadata:\n{match.group(1).strip()}")
                    
    return "\n---\n".join(skills_metadata) if skills_metadata else "No modular skills found."

def activate_skill(skill_id: str) -> str:
    """Loads Instructions (Level 2). Returns the full manual content of SKILL.md for the given skill_id."""
    skill_md = os.path.join(SKILLS_DIR, skill_id, "SKILL.md")
    if os.path.exists(skill_md):
        with open(skill_md, "r") as f:
            return f.read()
    return f"Skill '{skill_id}' not found at {skill_md}."

def execute_command(command: str) -> str:
    """Level 3: Resource & Tool Execution. Executes a bash or python command and returns the output."""
    print(f"\n[AGENT EXECUTING]: {command}")
    try:
        # We run from the root. Skills might reference internal scripts.
        # e.g. python skills/pptx/scripts/inventory.py
        import subprocess
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout + result.stderr
        return output if output.strip() else "Command executed successfully (no output)."
    except Exception as e:
        return f"Error executing command: {str(e)}"

SYSTEM_INSTRUCTION = """
You are a highly capable AI Assistant implementing the 'Agent Skills' architecture.
Your goal is to help the user by autonomously managing modular capabilities (Skills).

MODULAR ARCHITECTURE:
1. Level 1 (Discovery): Use 'list_skills' to scan the filesystem and discover what specialized tools you have.
2. Level 2 (Activation): Once you identify a relevant skill, YOU MUST call 'activate_skill' to read its full manual and procedural knowledge. Do not guess how a skill works; read the manual.
3. Level 3 (Execution): Follow the instructions in the manual to execute specific scripts or commands using 'execute_command'.

DASHBOARD GUIDELINES:
- When the user asks for a task (e.g., 'Create a presentation'), your first priority is to check your skills.
- Be proactive. If you have a skill that can do parts or all of the task, use it immediately.
- State your design approach clearly if the skill manual requires it.
- If a skill produces files, tell the user the filename and where it is saved.
"""

def chat():
    config = types.GenerateContentConfig(
        tools=[list_skills, activate_skill, execute_command],
        system_instruction=SYSTEM_INSTRUCTION,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False)
    )
    
    chat_session = client.chats.create(model=MODEL_ID, config=config)
    
    print(f"--- Gemini Agent Skills (Model: {MODEL_ID}) ---")
    print("Agent is ready. Type 'exit' to quit.\n")
    
    while True:
        try:
            user_input = input("User: ")
            if not user_input.strip():
                continue
            if user_input.lower() in ["exit", "quit"]:
                break
                
            response = chat_session.send_message(user_input)
            
            # Print the final textual response
            if response.text:
                print(f"\nGemini: {response.text}")
            else:
                # In case of empty text but function calls happened (Automatic calling is enabled so should be fine)
                print("\nGemini: [Action completed]")
                
        except Exception as e:
            print(f"\n[ERROR]: {str(e)}")

if __name__ == "__main__":
    chat()
