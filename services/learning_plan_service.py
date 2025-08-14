"""
Learning Plan Generation Service using litellm
"""

import json
import os
from typing import Dict, Any, Optional
from litellm import completion
import sys
import os

# Add the parent directory to the path to import prompts
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prompts import format_learning_plan_prompt
from services.exercise_generator import exercise_generator
from database.schemas import EnhancedLearningStepDetail

class LearningPlanService:
    """Service for generating learning plans using litellm"""
    
    def __init__(self):
        # Configure litellm with environment variables
        self.model = os.getenv("LITELLM_MODEL", "gpt-3.5-turbo")
        self.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("LITELLM_API_KEY")
        
        if not self.api_key:
            print("Warning: No API key found. Set OPENAI_API_KEY or LITELLM_API_KEY environment variable.")
    
    def generate_learning_plan(self, repo_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a learning plan for a given repository
        
        Args:
            repo_info: Dictionary containing repository information
            
        Returns:
            Dictionary containing the generated learning plan
        """
        try:
            # Format the prompt with repository information
            prompt = format_learning_plan_prompt(repo_info)
            
            # Generate the learning plan using litellm
            response = completion(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert programming instructor and learning path designer. Generate detailed, structured learning plans for GitHub repositories."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Extract the content from the response
            content = response.choices[0].message.content
            
            # Try to parse the JSON response
            try:
                # Find JSON content in the response (in case there's extra text)
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                
                if start_idx != -1 and end_idx != 0:
                    json_content = content[start_idx:end_idx]
                    learning_plan = json.loads(json_content)
                else:
                    # If no JSON found, create a structured response
                    learning_plan = self._create_fallback_plan(repo_info, content)
                
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                print(f"Raw content: {content}")
                # Create a fallback plan if JSON parsing fails
                learning_plan = self._create_fallback_plan(repo_info, content)
            
            # Validate and clean the learning plan
            learning_plan = self._validate_learning_plan(learning_plan, repo_info)
            
            return learning_plan
            
        except Exception as e:
            print(f"Error generating learning plan: {e}")
            # Return a basic fallback plan
            return self._create_basic_plan(repo_info)
    
    def _create_fallback_plan(self, repo_info: Dict[str, Any], ai_content: str) -> Dict[str, Any]:
        """Create a fallback plan when JSON parsing fails"""
        return {
            "title": f"Learning Plan for {repo_info.get('name', 'Repository')}",
            "description": f"Generated learning plan for {repo_info.get('name', 'Repository')}",
            "difficulty_level": "intermediate",
            "estimated_duration": "20 hours",
            "learning_steps": [
                {
                    "step": 1,
                    "title": "Repository Analysis",
                    "description": f"Analyze the {repo_info.get('name', 'repository')} structure and understand its purpose",
                    "duration": "2 hours",
                    "resources": ["Repository README", "Documentation"],
                    "exercises": ["Clone the repository", "Run the project"],
                    "completed": False
                },
                {
                    "step": 2,
                    "title": "Technology Stack Understanding",
                    "description": f"Learn about the technologies used in {repo_info.get('name', 'the repository')}",
                    "duration": "4 hours",
                    "resources": ["Official documentation", "Tutorials"],
                    "exercises": ["Set up development environment", "Basic examples"],
                    "completed": False
                }
            ],
            "prerequisites": [
                "Basic programming knowledge",
                "Understanding of version control (Git)"
            ],
            "learning_objectives": [
                f"Understand {repo_info.get('name', 'the repository')} architecture",
                "Learn the technology stack",
                "Contribute to the project"
            ],
            "technologies_covered": [
                repo_info.get('language', 'Programming language'),
                "Version control",
                "Development tools"
            ],
            "ai_generated_content": ai_content[:500] + "..." if len(ai_content) > 500 else ai_content
        }
    
    def _create_basic_plan(self, repo_info: Dict[str, Any]) -> Dict[str, Any]:
        """Create a basic learning plan when AI generation fails"""
        return {
            "title": f"Basic Learning Plan for {repo_info.get('name', 'Repository')}",
            "description": f"Basic learning path for {repo_info.get('name', 'Repository')}",
            "difficulty_level": "beginner",
            "estimated_duration": "15 hours",
            "learning_steps": [
                {
                    "step": 1,
                    "title": "Get Started",
                    "description": "Clone and set up the repository",
                    "duration": "1 hour",
                    "resources": ["Repository README"],
                    "exercises": ["Clone repository", "Install dependencies"],
                    "completed": False
                },
                {
                    "step": 2,
                    "title": "Understand the Code",
                    "description": "Read through the codebase and understand the structure",
                    "duration": "3 hours",
                    "resources": ["Code comments", "Documentation"],
                    "exercises": ["Code review", "Documentation reading"],
                    "completed": False
                },
                {
                    "step": 3,
                    "title": "Run the Project",
                    "description": "Successfully run the project and understand its functionality",
                    "duration": "2 hours",
                    "resources": ["Setup instructions"],
                    "exercises": ["Run the project", "Test basic functionality"],
                    "completed": False
                }
            ],
            "prerequisites": [
                "Basic programming knowledge",
                "Git fundamentals"
            ],
            "learning_objectives": [
                "Set up the development environment",
                "Understand the project structure",
                "Run the application"
            ],
            "technologies_covered": [
                repo_info.get('language', 'Programming language'),
                "Git",
                "Development tools"
            ]
        }
    
    def _validate_learning_plan(self, learning_plan: Dict[str, Any], repo_info: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean the learning plan"""
        # Ensure required fields exist
        required_fields = ["title", "description", "difficulty_level", "estimated_duration", "learning_steps"]
        
        for field in required_fields:
            if field not in learning_plan:
                if field == "title":
                    learning_plan[field] = f"Learning Plan for {repo_info.get('name', 'Repository')}"
                elif field == "description":
                    learning_plan[field] = f"Learning path for {repo_info.get('name', 'Repository')}"
                elif field == "difficulty_level":
                    learning_plan[field] = "intermediate"
                elif field == "estimated_duration":
                    learning_plan[field] = "20 hours"
                elif field == "learning_steps":
                    learning_plan[field] = []
        
        # Ensure learning_steps is a list and has proper structure
        if not isinstance(learning_plan.get("learning_steps"), list):
            learning_plan["learning_steps"] = []
        
        # Clean up each learning step
        for i, step in enumerate(learning_plan["learning_steps"]):
            if not isinstance(step, dict):
                learning_plan["learning_steps"][i] = {
                    "step": i + 1,
                    "title": f"Step {i + 1}",
                    "description": "Learning step description",
                    "duration": "2 hours",
                    "resources": [],
                    "exercises": [],
                    "completed": False
                }
            else:
                # Ensure step has required fields
                step["step"] = step.get("step", i + 1)
                step["title"] = step.get("title", f"Step {i + 1}")
                step["description"] = step.get("description", "Learning step description")
                step["duration"] = step.get("duration", "2 hours")
                step["resources"] = step.get("resources", [])
                step["exercises"] = step.get("exercises", [])
                step["completed"] = step.get("completed", False)
                
                # Generate coding exercises for this step
                coding_exercises = exercise_generator.generate_exercises_for_step(
                    step["title"], 
                    step["description"], 
                    learning_plan.get("difficulty_level", "intermediate")
                )
                step["coding_exercises"] = [ex.dict() for ex in coding_exercises]
                step["exercises_completed"] = 0
                step["total_exercises"] = len(coding_exercises)
        
        # Ensure other fields exist
        learning_plan["prerequisites"] = learning_plan.get("prerequisites", [])
        learning_plan["learning_objectives"] = learning_plan.get("learning_objectives", [])
        learning_plan["technologies_covered"] = learning_plan.get("technologies_covered", [])
        
        return learning_plan
    
    def estimate_complexity(self, repo_info: Dict[str, Any]) -> str:
        """Estimate repository complexity based on various factors"""
        stars = repo_info.get('stars', 0)
        forks = repo_info.get('forks', 0)
        size = repo_info.get('size', 0)
        
        # Simple complexity estimation
        if stars > 1000 and forks > 100:
            return "advanced"
        elif stars > 100 or forks > 10:
            return "intermediate"
        else:
            return "beginner"
