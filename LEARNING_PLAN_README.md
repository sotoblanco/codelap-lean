# Learning Plan Generation Service

## 🎯 Overview

The Learning Plan Generation service uses `litellm` to create comprehensive, AI-powered learning plans for GitHub repositories. It analyzes repository characteristics and generates structured learning paths tailored to the repository's complexity and technology stack.

## 🔧 Features

- **AI-Powered Generation**: Uses litellm with OpenAI models to generate detailed learning plans
- **Repository Analysis**: Analyzes repository complexity, topics, languages, and characteristics
- **Structured Learning Paths**: Creates progressive, step-by-step learning plans
- **Multiple Input Sources**: Accepts repository ID, URL, or direct repository information
- **Database Integration**: Automatically stores generated plans in the database
- **Specialized Prompts**: Tailored prompts for different repository types (web frameworks, ML, APIs)
- **Fallback Mechanisms**: Graceful handling of API failures with basic plan generation

## 🚀 How to Use

### Prerequisites

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Database**:
   ```bash
   cd database
   python3 init_db.py
   ```

3. **Configure API Keys** (optional but recommended):
   ```bash
   export OPENAI_API_KEY="your_openai_api_key"
   # or
   export LITELLM_API_KEY="your_api_key"
   export LITELLM_MODEL="gpt-4"  # Optional: default is gpt-3.5-turbo
   ```

4. **Start the Server**:
   ```bash
   python3 app.py
   ```

### Testing the Service

#### Method 1: Using the Test Script
```bash
python3 test_learning_plan.py
```

#### Method 2: Using curl

1. **Login to get JWT token**:
   ```bash
   curl -X POST "http://localhost:8000/login" \
        -H "Content-Type: application/json" \
        -d '{"username": "johndoe", "password": "secret"}'
   ```

2. **Generate plan from GitHub URL**:
   ```bash
   TOKEN="your_jwt_token_here"
   curl -X POST "http://localhost:8000/generate-plan" \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "repository_url": "https://github.com/tiangolo/fastapi"
        }'
   ```

3. **Generate plan from search result**:
   ```bash
   # First search for repositories
   curl -X POST "http://localhost:8000/search-repo" \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"query": "machine learning", "limit": 1}'
   
   # Then use the repository info to generate plan
   curl -X POST "http://localhost:8000/generate-plan" \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "repository_info": {
            "id": 123456,
            "name": "repo-name",
            "full_name": "owner/repo-name",
            "description": "Repository description",
            "html_url": "https://github.com/owner/repo-name",
            "language": "Python",
            "stars": 1000,
            "forks": 100,
            "topics": ["machine-learning", "python"]
          }
        }'
   ```

4. **Generate plan from database repository**:
   ```bash
   curl -X POST "http://localhost:8000/generate-plan" \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "repository_id": 1
        }'
   ```

## 📋 API Endpoint Details

### Endpoint: `POST /generate-plan`

**Request Body** (one of the following):
```json
{
  "repository_id": 1
}
```
```json
{
  "repository_url": "https://github.com/owner/repo-name"
}
```
```json
{
  "repository_info": {
    "id": 123456,
    "name": "repo-name",
    "full_name": "owner/repo-name",
    "description": "Repository description",
    "html_url": "https://github.com/owner/repo-name",
    "clone_url": "https://github.com/owner/repo-name.git",
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
}
```

**Response**:
```json
{
  "success": true,
  "learning_plan": {
    "title": "Comprehensive Learning Plan for FastAPI",
    "description": "A detailed learning path to master FastAPI and its technologies",
    "difficulty_level": "intermediate",
    "estimated_duration": "25 hours",
    "learning_steps": [
      {
        "step": 1,
        "title": "Understanding FastAPI Fundamentals",
        "description": "Learn the basics of FastAPI framework and its advantages",
        "duration": "3 hours",
        "resources": ["FastAPI documentation", "Official tutorials"],
        "exercises": ["Install FastAPI", "Create first endpoint"],
        "completed": false
      }
    ],
    "prerequisites": [
      "Basic Python knowledge",
      "Understanding of HTTP and REST APIs",
      "Familiarity with async/await syntax"
    ],
    "learning_objectives": [
      "Master FastAPI framework",
      "Build RESTful APIs",
      "Implement authentication and authorization",
      "Deploy FastAPI applications"
    ],
    "technologies_covered": [
      "FastAPI",
      "Pydantic",
      "SQLAlchemy",
      "JWT Authentication",
      "Docker"
    ]
  },
  "repository_info": {
    "id": 123456,
    "name": "fastapi",
    "full_name": "tiangolo/fastapi",
    "description": "FastAPI framework, high performance, easy to learn...",
    "html_url": "https://github.com/tiangolo/fastapi",
    "language": "Python",
    "stars": 65000,
    "forks": 5500
  }
}
```

## 🤖 AI Prompt System

### Main Prompt Structure

The system uses a comprehensive prompt that includes:

1. **Repository Analysis**: Name, description, language, topics, metrics
2. **Learning Requirements**: Assessment, prerequisites, core path, hands-on practice, advanced topics
3. **Output Format**: Structured JSON with learning steps, prerequisites, objectives
4. **Guidelines**: Complexity assessment, step progression, practical focus

### Specialized Prompts

The system automatically adds specialized prompts based on repository characteristics:

- **Web Frameworks**: Routing, middleware, database integration, authentication
- **Machine Learning**: Mathematical foundations, algorithms, data preprocessing
- **APIs**: RESTful design, authentication, rate limiting, security

### Prompt Customization

You can customize prompts by modifying `prompts.py`:

```python
# Add new specialized prompt
MOBILE_APP_PROMPT = """
Additional considerations for mobile app repositories:
- Focus on mobile development patterns
- Include platform-specific considerations
- Cover app store deployment
"""

# Update the get_specialized_prompt function
def get_specialized_prompt(repo_info):
    # ... existing code ...
    if any(topic in ['mobile', 'ios', 'android'] for topic in topics):
        specialized_prompts.append(MOBILE_APP_PROMPT)
    return '\n'.join(specialized_prompts)
```

## 🔧 Service Architecture

### LearningPlanService Class

```python
class LearningPlanService:
    def __init__(self):
        # Configure litellm with environment variables
        self.model = os.getenv("LITELLM_MODEL", "gpt-3.5-turbo")
        self.api_key = os.getenv("OPENAI_API_KEY")
    
    def generate_learning_plan(self, repo_info: Dict[str, Any]) -> Dict[str, Any]:
        # Main method to generate learning plans
    
    def _validate_learning_plan(self, learning_plan: Dict[str, Any], repo_info: Dict[str, Any]) -> Dict[str, Any]:
        # Validate and clean the generated plan
    
    def _create_fallback_plan(self, repo_info: Dict[str, Any], ai_content: str) -> Dict[str, Any]:
        # Create fallback plan when AI generation fails
```

### Error Handling

The service includes comprehensive error handling:

1. **API Failures**: Falls back to basic plan generation
2. **JSON Parsing Errors**: Creates structured fallback plans
3. **Invalid Input**: Returns appropriate error messages
4. **Rate Limiting**: Handles API rate limits gracefully

## 📊 Learning Plan Structure

### Generated Learning Plans Include:

1. **Assessment Phase** (1-2 steps)
   - Repository complexity evaluation
   - Technology stack identification
   - Learning objectives definition

2. **Prerequisites** (2-4 steps)
   - Essential knowledge and skills
   - Required technologies and tools
   - Framework-specific requirements

3. **Core Learning Path** (5-10 steps)
   - Progressive learning steps
   - Theoretical and practical components
   - Repository-specific patterns

4. **Hands-on Practice** (3-6 steps)
   - Code analysis exercises
   - Modification tasks
   - Testing and debugging

5. **Advanced Topics** (2-4 steps)
   - Architecture understanding
   - Performance optimization
   - Contributing guidelines

## 🎯 Use Cases

### 1. Learning New Technologies
```bash
# Generate plan for a new framework
curl -X POST "http://localhost:8000/generate-plan" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{"repository_url": "https://github.com/vercel/next.js"}'
```

### 2. Contributing to Open Source
```bash
# Generate plan for contributing to a project
curl -X POST "http://localhost:8000/generate-plan" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{"repository_url": "https://github.com/tensorflow/tensorflow"}'
```

### 3. Team Onboarding
```bash
# Generate plan for team member onboarding
curl -X POST "http://localhost:8000/generate-plan" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{"repository_id": 1}'
```

## ⚙️ Configuration

### Environment Variables

```bash
# Required for AI generation
export OPENAI_API_KEY="your_openai_api_key"

# Optional configurations
export LITELLM_MODEL="gpt-4"  # Default: gpt-3.5-turbo
export LITELLM_API_KEY="your_api_key"  # Alternative to OPENAI_API_KEY
```

### Model Configuration

You can configure different models by setting `LITELLM_MODEL`:

- `gpt-3.5-turbo`: Fast, cost-effective (default)
- `gpt-4`: More detailed, higher quality
- `claude-3-sonnet`: Alternative AI model
- `gemini-pro`: Google's model

## 🐛 Troubleshooting

### Common Issues:

1. **API Key Missing**:
   - Set `OPENAI_API_KEY` environment variable
   - Check API key validity

2. **Rate Limiting**:
   - Wait for rate limit to reset
   - Use a different API key
   - Reduce request frequency

3. **JSON Parsing Errors**:
   - Check AI model response format
   - Verify prompt structure
   - Review fallback mechanisms

4. **Database Errors**:
   - Ensure database is initialized
   - Check database connection
   - Verify schema compatibility

## 📈 Performance Optimization

### Tips for Better Results:

1. **Use GPT-4**: Better quality plans but higher cost
2. **Provide Detailed Repository Info**: More context = better plans
3. **Set Appropriate Temperature**: 0.7 for creativity, 0.3 for consistency
4. **Use Specialized Prompts**: Leverage repository-specific guidance

## 🔮 Future Enhancements

### Planned Features:

1. **Multi-language Support**: Generate plans in different languages
2. **Interactive Learning**: Step-by-step guided learning
3. **Progress Tracking**: Track learning plan completion
4. **Collaborative Learning**: Share and modify learning plans
5. **Integration with IDEs**: Direct integration with development environments

## 🎉 Success Indicators

When the service is working correctly, you should see:

1. ✅ Successful AI plan generation
2. ✅ Structured learning steps with resources and exercises
3. ✅ Appropriate difficulty level assessment
4. ✅ Repository-specific technology coverage
5. ✅ Automatic database storage of generated plans
6. ✅ Graceful fallback for API failures
7. ✅ Comprehensive error handling and validation
