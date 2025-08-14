# AI Prompts for Learning Plan Generation
# This file contains prompts used by litellm to generate learning plans

LEARNING_PLAN_PROMPT = """
You are an expert programming instructor and learning path designer. Your task is to create a comprehensive, step-by-step learning plan for a GitHub repository.

## Repository Information:
- Name: {repo_name}
- Description: {repo_description}
- Language: {repo_language}
- Topics: {repo_topics}
- Stars: {repo_stars}
- Forks: {repo_forks}
- Size: {repo_size} KB
- Created: {repo_created_at}
- Last Updated: {repo_updated_at}
- README Preview: {readme_preview}

## Task:
Create a detailed learning plan that will help a developer understand and contribute to this repository. The plan should be structured, progressive, and tailored to the repository's complexity and technology stack.

## Requirements:

### 1. **Assessment Phase** (1-2 steps)
- Evaluate the repository's complexity level (Beginner/Intermediate/Advanced)
- Identify the main technologies and frameworks used
- Determine the learning objectives

### 2. **Prerequisites** (2-4 steps)
- List essential knowledge and skills needed before starting
- Include specific technologies, tools, and concepts
- Consider the repository's language and framework requirements

### 3. **Core Learning Path** (5-10 steps)
- Break down the learning into logical, progressive steps
- Each step should build upon the previous one
- Include both theoretical understanding and practical exercises
- Focus on the repository's specific implementation patterns

### 4. **Hands-on Practice** (3-6 steps)
- Practical exercises using the repository's code
- Code analysis and understanding tasks
- Small modifications or feature additions
- Testing and debugging exercises

### 5. **Advanced Topics** (2-4 steps)
- Deep dive into complex parts of the codebase
- Architecture understanding
- Performance optimization concepts
- Contributing guidelines and best practices

## Output Format:
Return a JSON object with the following structure:

```json
{{
    "title": "Comprehensive Learning Plan for [Repository Name]",
    "description": "A detailed learning path to master [Repository Name] and its technologies",
    "difficulty_level": "beginner|intermediate|advanced",
    "estimated_duration": "X hours",
    "learning_steps": [
        {{
            "step": 1,
            "title": "Step Title",
            "description": "Detailed description of what to learn and why",
            "duration": "X hours",
            "resources": ["resource1", "resource2"],
            "exercises": ["exercise1", "exercise2"],
            "completed": false
        }}
    ],
    "prerequisites": [
        "Prerequisite 1",
        "Prerequisite 2"
    ],
    "learning_objectives": [
        "Objective 1",
        "Objective 2"
    ],
    "technologies_covered": [
        "Technology 1",
        "Technology 2"
    ]
}}
```

## Guidelines:

1. **Complexity Assessment**: 
   - Beginner: Basic syntax, simple concepts, well-documented
   - Intermediate: Multiple technologies, some advanced patterns, moderate documentation
   - Advanced: Complex architecture, multiple integrations, minimal documentation

2. **Step Progression**:
   - Start with fundamentals and gradually increase complexity
   - Each step should be achievable in 1-4 hours
   - Include both reading/learning and hands-on practice

3. **Practical Focus**:
   - Emphasize hands-on learning over theoretical concepts
   - Include code analysis and modification exercises
   - Provide specific tasks related to the repository

4. **Resource Integration**:
   - Reference the repository's documentation
   - Include relevant external resources when needed
   - Suggest tools and development environment setup

5. **Real-world Application**:
   - Connect learning to actual development scenarios
   - Include debugging and problem-solving exercises
   - Prepare learners for contributing to the project

## Important Notes:
- Be specific and actionable in your recommendations
- Consider the repository's actual code structure and patterns
- Adapt the plan based on the technology stack and complexity
- Ensure the plan is realistic and achievable
- Focus on practical skills that will help with the actual repository

Generate a learning plan that will transform a developer from a beginner to someone capable of understanding and contributing to this specific repository.
"""

# Additional specialized prompts for different types of repositories
WEB_FRAMEWORK_PROMPT = """
Additional considerations for web framework repositories:
- Focus on routing, middleware, and request/response patterns
- Include database integration and ORM concepts
- Cover authentication and authorization patterns
- Include testing strategies for web applications
- Consider deployment and production considerations
"""

MACHINE_LEARNING_PROMPT = """
Additional considerations for machine learning repositories:
- Emphasize mathematical foundations and algorithms
- Include data preprocessing and feature engineering
- Cover model evaluation and validation techniques
- Include practical ML workflow and best practices
- Consider ethical considerations and bias detection
"""

API_PROMPT = """
Additional considerations for API repositories:
- Focus on RESTful design principles
- Include authentication and rate limiting
- Cover API documentation and testing
- Include versioning and backward compatibility
- Consider security best practices
"""

# Function to get specialized prompt based on repository characteristics
def get_specialized_prompt(repo_info):
    """Get additional specialized prompt based on repository topics and characteristics"""
    topics = repo_info.get('topics', [])
    description = repo_info.get('description', '').lower()
    
    specialized_prompts = []
    
    if any(topic in ['web', 'framework', 'api', 'rest'] for topic in topics) or 'web' in description:
        specialized_prompts.append(WEB_FRAMEWORK_PROMPT)
    
    if any(topic in ['machine-learning', 'ai', 'ml', 'deep-learning'] for topic in topics) or 'machine learning' in description:
        specialized_prompts.append(MACHINE_LEARNING_PROMPT)
    
    if any(topic in ['api', 'rest', 'graphql'] for topic in topics) or 'api' in description:
        specialized_prompts.append(API_PROMPT)
    
    return '\n'.join(specialized_prompts)

# Function to format the main prompt with repository data
def format_learning_plan_prompt(repo_info):
    """Format the learning plan prompt with repository information"""
    specialized_prompt = get_specialized_prompt(repo_info)
    
    return LEARNING_PLAN_PROMPT.format(
        repo_name=repo_info.get('name', 'Unknown Repository'),
        repo_description=repo_info.get('description', 'No description available'),
        repo_language=repo_info.get('language', 'Unknown'),
        repo_topics=', '.join(repo_info.get('topics', [])),
        repo_stars=repo_info.get('stars', 0),
        repo_forks=repo_info.get('forks', 0),
        repo_size=repo_info.get('size', 0),
        repo_created_at=repo_info.get('created_at', 'Unknown'),
        repo_updated_at=repo_info.get('updated_at', 'Unknown'),
        readme_preview=repo_info.get('readme_preview', 'No README available')[:500]
    ) + '\n\n' + specialized_prompt
