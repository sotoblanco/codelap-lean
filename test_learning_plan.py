#!/usr/bin/env python3
"""
Test script for Learning Plan Generation functionality
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
TEST_USER = "johndoe"
TEST_PASSWORD = "secret"

def login():
    """Login and get JWT token"""
    login_data = {
        "username": TEST_USER,
        "password": TEST_PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    if response.status_code == 200:
        token_data = response.json()
        return token_data["access_token"]
    else:
        print(f"Login failed: {response.status_code} - {response.text}")
        return None

def test_generate_plan_from_url(token):
    """Test generating learning plan from GitHub URL"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test with a popular Python repository
    request_data = {
        "repository_url": "https://github.com/tiangolo/fastapi"
    }
    
    print("Testing learning plan generation from GitHub URL...")
    response = requests.post(f"{BASE_URL}/generate-plan", json=request_data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            print(f"✅ Learning plan generated successfully!")
            plan = result['learning_plan']
            print(f"Title: {plan['title']}")
            print(f"Difficulty: {plan['difficulty_level']}")
            print(f"Duration: {plan['estimated_duration']}")
            print(f"Steps: {len(plan['learning_steps'])}")
            print(f"Prerequisites: {len(plan['prerequisites'])}")
            print(f"Technologies: {', '.join(plan['technologies_covered'])}")
            
            # Show first few steps
            print("\nFirst 3 learning steps:")
            for i, step in enumerate(plan['learning_steps'][:3], 1):
                print(f"  {i}. {step['title']} ({step['duration']})")
                print(f"     {step['description'][:100]}...")
        else:
            print(f"❌ Learning plan generation failed: {result['error_message']}")
    else:
        print(f"❌ Request failed: {response.status_code} - {response.text}")

def test_generate_plan_from_search_result(token):
    """Test generating learning plan from search result"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # First, search for a repository
    search_data = {
        "query": "machine learning",
        "limit": 1
    }
    
    print("\nSearching for a repository to generate plan...")
    search_response = requests.post(f"{BASE_URL}/search-repo", json=search_data, headers=headers)
    
    if search_response.status_code == 200:
        search_result = search_response.json()
        if search_result['repositories']:
            repo = search_result['repositories'][0]
            
            # Generate learning plan for the found repository
            request_data = {
                "repository_info": {
                    "id": repo['id'],
                    "name": repo['name'],
                    "full_name": repo['full_name'],
                    "description": repo['description'],
                    "html_url": repo['html_url'],
                    "clone_url": repo['clone_url'],
                    "language": repo['language'],
                    "languages": repo.get('languages', []),
                    "topics": repo.get('topics', []),
                    "stars": repo['stars'],
                    "forks": repo['forks'],
                    "watchers": repo['watchers'],
                    "open_issues": repo['open_issues'],
                    "size": repo.get('size', 0),
                    "created_at": repo.get('created_at'),
                    "updated_at": repo.get('updated_at'),
                    "readme_preview": repo.get('readme_preview', ''),
                    "default_branch": repo.get('default_branch'),
                    "license": repo.get('license'),
                    "archived": repo['archived'],
                    "fork": repo['fork'],
                    "private": repo['private']
                }
            }
            
            print(f"Generating learning plan for: {repo['full_name']}")
            plan_response = requests.post(f"{BASE_URL}/generate-plan", json=request_data, headers=headers)
            
            if plan_response.status_code == 200:
                result = plan_response.json()
                if result['success']:
                    print(f"✅ Learning plan generated successfully!")
                    plan = result['learning_plan']
                    print(f"Title: {plan['title']}")
                    print(f"Difficulty: {plan['difficulty_level']}")
                    print(f"Duration: {plan['estimated_duration']}")
                    print(f"Steps: {len(plan['learning_steps'])}")
                else:
                    print(f"❌ Learning plan generation failed: {result['error_message']}")
            else:
                print(f"❌ Plan generation request failed: {plan_response.status_code} - {plan_response.text}")
        else:
            print("❌ No repositories found in search")
    else:
        print(f"❌ Search request failed: {search_response.status_code} - {search_response.text}")

def test_generate_plan_from_database(token):
    """Test generating learning plan from database repository ID"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test with repository ID 1 (should exist if database was seeded)
    request_data = {
        "repository_id": 1
    }
    
    print("\nTesting learning plan generation from database repository...")
    response = requests.post(f"{BASE_URL}/generate-plan", json=request_data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        if result['success']:
            print(f"✅ Learning plan generated from database successfully!")
            plan = result['learning_plan']
            print(f"Title: {plan['title']}")
            print(f"Difficulty: {plan['difficulty_level']}")
            print(f"Duration: {plan['estimated_duration']}")
            print(f"Steps: {len(plan['learning_steps'])}")
        else:
            print(f"❌ Learning plan generation failed: {result['error_message']}")
    elif response.status_code == 404:
        print("❌ Repository not found in database (database may not be seeded)")
    else:
        print(f"❌ Request failed: {response.status_code} - {response.text}")

def test_invalid_request(token):
    """Test with invalid request data"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test with no repository information
    request_data = {}
    
    print("\nTesting invalid request (no repository info)...")
    response = requests.post(f"{BASE_URL}/generate-plan", json=request_data, headers=headers)
    
    if response.status_code == 400:
        print(f"✅ Invalid request properly rejected: {response.json()['detail']}")
    else:
        print(f"❌ Invalid request not properly handled: {response.status_code} - {response.text}")

def main():
    print("🚀 Testing Learning Plan Generation Functionality")
    print("=" * 60)
    
    # Login
    token = login()
    if not token:
        print("❌ Cannot proceed without authentication token")
        return
    
    print(f"✅ Logged in successfully")
    
    # Run tests
    test_generate_plan_from_url(token)
    test_generate_plan_from_search_result(token)
    test_generate_plan_from_database(token)
    test_invalid_request(token)
    
    print("\n" + "=" * 60)
    print("🎉 Learning Plan Generation Testing completed!")

if __name__ == "__main__":
    main()
