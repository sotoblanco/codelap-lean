#!/usr/bin/env python3
"""
Debug script to see what the learning plan service returns
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.learning_plan_service import LearningPlanService

def main():
    # Create a test repository info
    repo_info = {
        "id": 12345,
        "name": "test-repo",
        "full_name": "testuser/test-repo",
        "description": "A test repository for learning Python basics",
        "html_url": "https://github.com/testuser/test-repo",
        "clone_url": "https://github.com/testuser/test-repo.git",
        "language": "Python",
        "languages": ["Python"],
        "topics": ["python", "learning", "basics"],
        "stars": 100,
        "forks": 10,
        "watchers": 50,
        "open_issues": 5,
        "size": 1024,
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-12-01T00:00:00Z",
        "readme_preview": "A test repository for learning Python basics",
        "default_branch": "main",
        "license": "MIT",
        "archived": False,
        "fork": False,
        "private": False
    }
    
    # Create learning plan service
    service = LearningPlanService()
    
    # Generate a plan
    print("Generating learning plan...")
    plan = service.generate_learning_plan(repo_info)
    
    print(f"Plan title: {plan.get('title')}")
    print(f"Plan description: {plan.get('description')}")
    print(f"Number of steps: {len(plan.get('learning_steps', []))}")
    
    # Check the first step
    if plan.get('learning_steps'):
        first_step = plan['learning_steps'][0]
        print(f"\nFirst step type: {type(first_step)}")
        print(f"First step content: {first_step}")
        
        if hasattr(first_step, 'coding_exercises'):
            print(f"Has coding_exercises: {hasattr(first_step, 'coding_exercises')}")
            print(f"Number of coding exercises: {len(first_step.coding_exercises)}")
        else:
            print("No coding_exercises attribute")
            print(f"Available keys: {list(first_step.keys()) if isinstance(first_step, dict) else 'Not a dict'}")

if __name__ == "__main__":
    main()
