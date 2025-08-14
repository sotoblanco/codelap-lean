#!/usr/bin/env python3
"""
Test script for GitHub search functionality
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

def test_search_by_url(token):
    """Test searching by GitHub URL"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test with a popular Python repository
    search_data = {
        "query": "https://github.com/tiangolo/fastapi",
        "limit": 5
    }
    
    print("Testing search by GitHub URL...")
    response = requests.post(f"{BASE_URL}/search-repo", json=search_data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Search by URL successful!")
        print(f"Search type: {result['search_type']}")
        print(f"Total repositories: {result['total_count']}")
        if result['repositories']:
            repo = result['repositories'][0]
            print(f"Repository: {repo['full_name']}")
            print(f"Description: {repo['description']}")
            print(f"Stars: {repo['stars']}")
            print(f"Language: {repo['language']}")
        if result['ai_prerequisites']:
            print(f"AI Prerequisites: {result['ai_prerequisites']}")
    else:
        print(f"❌ Search by URL failed: {response.status_code} - {response.text}")

def test_search_by_term(token):
    """Test searching by search term"""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test with a search term
    search_data = {
        "query": "machine learning",
        "limit": 3
    }
    
    print("\nTesting search by term...")
    response = requests.post(f"{BASE_URL}/search-repo", json=search_data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Search by term successful!")
        print(f"Search type: {result['search_type']}")
        print(f"Total repositories: {result['total_count']}")
        print("Top repositories:")
        for i, repo in enumerate(result['repositories'][:3], 1):
            print(f"  {i}. {repo['full_name']} - {repo['stars']} stars")
        if result['ai_prerequisites']:
            print(f"AI Prerequisites: {result['ai_prerequisites']}")
    else:
        print(f"❌ Search by term failed: {response.status_code} - {response.text}")

def test_invalid_url(token):
    """Test with invalid GitHub URL"""
    headers = {"Authorization": f"Bearer {token}"}
    
    search_data = {
        "query": "https://invalid-url.com/repo",
        "limit": 5
    }
    
    print("\nTesting invalid URL...")
    response = requests.post(f"{BASE_URL}/search-repo", json=search_data, headers=headers)
    
    if response.status_code == 400:
        print(f"✅ Invalid URL properly rejected: {response.json()['detail']}")
    else:
        print(f"❌ Invalid URL not properly handled: {response.status_code} - {response.text}")

def main():
    print("🚀 Testing GitHub Search Functionality")
    print("=" * 50)
    
    # Login
    token = login()
    if not token:
        print("❌ Cannot proceed without authentication token")
        return
    
    print(f"✅ Logged in successfully")
    
    # Run tests
    test_search_by_url(token)
    test_search_by_term(token)
    test_invalid_url(token)
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")

if __name__ == "__main__":
    main()
