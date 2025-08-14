#!/usr/bin/env python3
"""
Test script for the enhanced coding editor functionality
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
TEST_USER = {
    "username": "testuser",
    "password": "testpass123"
}

def login():
    """Login and get JWT token"""
    try:
        response = requests.post(f"{BASE_URL}/login", json=TEST_USER)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("✅ Login successful")
            return token
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_code_validation(token):
    """Test code validation endpoint"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    test_cases = [
        {
            "name": "Valid Python Code",
            "code": 'print("Hello, World!")',
            "expected": True
        },
        {
            "name": "Function Definition",
            "code": 'def greet(name):\n    return f"Hello, {name}!"\n\nprint(greet("Alice"))',
            "expected": True
        },
        {
            "name": "Syntax Error",
            "code": 'print("Hello, World!"',
            "expected": False
        },
        {
            "name": "Dangerous Code (should be rejected)",
            "code": 'eval("print(\'Hello\')")',
            "expected": False
        },
        {
            "name": "Empty Code",
            "code": "",
            "expected": False
        }
    ]
    
    print("\n🧪 Testing Code Validation:")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   Code: {repr(test_case['code'])}")
        
        try:
            submission = {
                "exercise_id": f"test_exercise_{i}",
                "user_code": test_case["code"],
                "step_number": 1
            }
            
            response = requests.post(f"{BASE_URL}/validate-code", json=submission, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                is_correct = result["is_correct"]
                score = result["score"]
                feedback = result["feedback"]
                
                status = "✅ PASS" if is_correct == test_case["expected"] else "❌ FAIL"
                print(f"   Status: {status}")
                print(f"   Result: Correct={is_correct}, Score={score}")
                print(f"   Feedback: {feedback}")
                
                if result.get("error_message"):
                    print(f"   Error: {result['error_message']}")
                    
            else:
                print(f"   ❌ Request failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"   ❌ Test error: {e}")
        
        time.sleep(0.5)  # Small delay between requests

def test_learning_plan_with_exercises(token):
    """Test learning plan generation with coding exercises"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    print("\n🧪 Testing Learning Plan with Coding Exercises:")
    print("=" * 50)
    
    # Test with a simple repository
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
    
    try:
        request = {
            "repository_info": repo_info
        }
        
        response = requests.post(f"{BASE_URL}/generate-plan", json=request, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result["success"]:
                plan = result["learning_plan"]
                print(f"✅ Learning plan generated successfully!")
                print(f"   Title: {plan['title']}")
                print(f"   Steps: {len(plan['learning_steps'])}")
                
                # Check if steps have coding exercises
                for i, step in enumerate(plan['learning_steps']):
                    exercises_count = len(step.get('coding_exercises', []))
                    print(f"   Step {i+1}: {exercises_count} coding exercises")
                    
                    if exercises_count > 0:
                        print(f"      First exercise: {step['coding_exercises'][0]['title']}")
                        print(f"      Difficulty: {step['coding_exercises'][0]['difficulty']}")
            else:
                print(f"❌ Plan generation failed: {result.get('error_message', 'Unknown error')}")
        else:
            print(f"❌ Request failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Test error: {e}")

def main():
    """Main test function"""
    print("🚀 Testing Enhanced Coding Editor Functionality")
    print("=" * 60)
    
    # Login
    token = login()
    if not token:
        print("❌ Cannot proceed without authentication")
        return
    
    # Test code validation
    test_code_validation(token)
    
    # Test learning plan with exercises
    test_learning_plan_with_exercises(token)
    
    print("\n✅ Testing completed!")

if __name__ == "__main__":
    main()
