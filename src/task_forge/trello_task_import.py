import requests
from typing import List, Dict
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Update Trello API credentials
API_KEY = os.getenv("TRELLO_API_KEY")
API_TOKEN = os.getenv("TRELLO_API_TOKEN")
BOARD_ID = os.getenv("TRELLO_BOARD_ID")
LIST_ID = os.getenv("TRELLO_LIST_ID")

def parse_plan(plan: str) -> List[Dict[str, str]]:
    lines = plan.strip().split('\n')
    tasks = []
    current_task = None

    for line in lines:
        if line[0].isdigit():
            if current_task:
                tasks.append(current_task)
            current_task = {"name": line.split('. ', 1)[1], "description": ""}
        elif line.strip().startswith('*'):
            current_task["description"] += f"- {line.strip()[1:].strip()}\n"

    if current_task:
        tasks.append(current_task)

    return tasks

def create_trello_card(name: str, description: str) -> None:
    url = f"https://api.trello.com/1/cards"
    query = {
        'key': API_KEY,
        'token': API_TOKEN,
        'idList': LIST_ID,
        'name': name,
        'desc': description
    }
    response = requests.post(url, params=query)
    response.raise_for_status()
    print(f"Created card: {name}")

def main(plan: str):
    tasks = parse_plan(plan)
    for task in tasks:
        create_trello_card(task['name'], task['description'])

if __name__ == "__main__":
    # Example usage
    plan = """
1. Set up project structure:
   * Create separate directories for frontend (React) and backend (Flask)
2. Frontend development:
   * Initialize a new React project
   * Implement basic components for the Trello Power-Up interface
   * Integrate Trello Power-Up client library
    """
    main(plan)