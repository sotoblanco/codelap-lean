# GitHub Search Endpoint Implementation

## 🎯 Overview

The `/search-repo` endpoint allows users to search for GitHub repositories in two ways:
1. **By GitHub URL**: Fetches detailed information about a specific repository
2. **By Search Term**: Searches for relevant Python repositories based on keywords

## 🔧 Features

- **GitHub API Integration**: Uses PyGithub library for GitHub API interactions
- **AI Prerequisites Generation**: Automatically generates learning prerequisites based on repository characteristics
- **Flexible Search**: Accepts both URLs and search terms
- **Authentication Required**: Protected endpoint requiring JWT token
- **Comprehensive Repository Data**: Returns detailed repository information including topics, languages, and README preview

## 🚀 How to Test

### Prerequisites

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Database** (if not already done):
   ```bash
   cd database
   python3 init_db.py
   ```

3. **Start the Server**:
   ```bash
   python3 app.py
   ```

4. **Optional: Set GitHub Token** (for higher rate limits):
   ```bash
   export GITHUB_TOKEN="your_github_token_here"
   ```

### Testing Methods

#### Method 1: Using the Test Script
```bash
python3 test_github_search.py
```

#### Method 2: Using curl

1. **Login to get JWT token**:
   ```bash
   curl -X POST "http://localhost:8000/login" \
        -H "Content-Type: application/json" \
        -d '{"username": "johndoe", "password": "secret"}'
   ```

2. **Search by GitHub URL**:
   ```bash
   TOKEN="your_jwt_token_here"
   curl -X POST "http://localhost:8000/search-repo" \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "query": "https://github.com/tiangolo/fastapi",
          "limit": 5
        }'
   ```

3. **Search by term**:
   ```bash
   curl -X POST "http://localhost:8000/search-repo" \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "query": "machine learning",
          "limit": 3
        }'
   ```

#### Method 3: Using the Interactive API Documentation
1. Open your browser and go to: `http://localhost:8000/docs`
2. Click on the `/search-repo` endpoint
3. Click "Try it out"
4. Enter your JWT token in the Authorization header
5. Provide the search request and execute

## 📋 API Endpoint Details

### Endpoint: `POST /search-repo`

**Request Body**:
```json
{
  "query": "string",     // GitHub URL or search term
  "limit": 10           // Optional: number of results (default: 10)
}
```

**Response**:
```json
{
  "query": "string",
  "search_type": "url|search",
  "repositories": [
    {
      "id": 123456,
      "name": "repository-name",
      "full_name": "owner/repository-name",
      "description": "Repository description",
      "html_url": "https://github.com/owner/repository-name",
      "clone_url": "https://github.com/owner/repository-name.git",
      "language": "Python",
      "languages": ["Python", "JavaScript"],
      "topics": ["api", "web", "fastapi"],
      "stars": 15000,
      "forks": 1200,
      "watchers": 500,
      "open_issues": 45,
      "size": 1024,
      "created_at": "2020-01-01T00:00:00Z",
      "updated_at": "2023-12-01T00:00:00Z",
      "readme_preview": "Preview of README content...",
      "default_branch": "main",
      "license": "MIT",
      "archived": false,
      "fork": false,
      "private": false
    }
  ],
  "ai_prerequisites": [
    "Basic Python knowledge",
    "Understanding of HTTP and REST APIs",
    "Understanding of Python syntax and data structures"
  ],
  "total_count": 1
}
```

## 🔍 Search Types

### 1. URL Search
- **Input**: GitHub repository URL (e.g., `https://github.com/tiangolo/fastapi`)
- **Behavior**: Fetches detailed information about the specific repository
- **Returns**: Single repository with comprehensive details

### 2. Term Search
- **Input**: Search keywords (e.g., `machine learning`, `web framework`)
- **Behavior**: Searches for Python repositories matching the keywords
- **Returns**: List of relevant repositories sorted by stars

## 🤖 AI Prerequisites Generation

The system automatically generates learning prerequisites based on:

- **Programming Language**: Python, JavaScript, Java, etc.
- **Repository Topics**: API, web, database, machine-learning, etc.
- **Repository Characteristics**: Stars, forks, complexity indicators
- **General Skills**: Command line, version control, etc.

## ⚠️ Rate Limiting

- **Without GitHub Token**: 60 requests/hour
- **With GitHub Token**: 5000 requests/hour

To avoid rate limiting, consider setting a GitHub personal access token:
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with `public_repo` scope
3. Set the environment variable: `export GITHUB_TOKEN="your_token"`

## 🐛 Troubleshooting

### Common Issues:

1. **Rate Limit Exceeded**:
   - Set a GitHub token
   - Wait for rate limit to reset

2. **Authentication Errors**:
   - Ensure you're logged in and have a valid JWT token
   - Check token expiration (30 minutes by default)

3. **Repository Not Found**:
   - Verify the GitHub URL is correct
   - Check if the repository is private (requires authentication)

4. **Import Errors**:
   - Ensure all dependencies are installed
   - Check Python path and imports

## 📝 Example Usage Scenarios

### Scenario 1: Learning FastAPI
```bash
# Search for FastAPI repository
curl -X POST "http://localhost:8000/search-repo" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"query": "https://github.com/tiangolo/fastapi"}'
```

### Scenario 2: Finding Machine Learning Projects
```bash
# Search for ML repositories
curl -X POST "http://localhost:8000/search-repo" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"query": "machine learning", "limit": 5}'
```

### Scenario 3: Web Development Frameworks
```bash
# Search for web frameworks
curl -X POST "http://localhost:8000/search-repo" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"query": "web framework", "limit": 3}'
```

## 🎉 Success Indicators

When the implementation is working correctly, you should see:

1. ✅ Successful login and JWT token generation
2. ✅ Repository details fetched from GitHub API
3. ✅ AI prerequisites generated based on repository characteristics
4. ✅ Proper error handling for invalid URLs or rate limits
5. ✅ Search results sorted by relevance (stars for term searches)
6. ✅ Comprehensive repository information including topics and languages
