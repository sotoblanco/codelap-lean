from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class User(UserBase):
    id: int
    disabled: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Repository schemas
class RepositoryBase(BaseModel):
    repo_url: HttpUrl
    name: str
    description: Optional[str] = None
    language: Optional[str] = None

class RepositoryCreate(RepositoryBase):
    ai_prerequisites: Optional[List[str]] = None
    stars: Optional[int] = 0
    forks: Optional[int] = 0

class RepositoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    ai_prerequisites: Optional[List[str]] = None
    language: Optional[str] = None
    stars: Optional[int] = None
    forks: Optional[int] = None

class Repository(RepositoryBase):
    id: int
    ai_prerequisites: Optional[List[str]] = None
    stars: int
    forks: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Learning Plan schemas
class LearningStep(BaseModel):
    step: int
    title: str
    description: str
    completed: bool = False

class LearningPlanBase(BaseModel):
    title: str
    description: Optional[str] = None
    difficulty_level: Optional[str] = None
    estimated_duration: Optional[int] = None

class LearningPlanCreate(LearningPlanBase):
    repository_id: int
    learning_steps: List[LearningStep]

class LearningPlanUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    learning_steps: Optional[List[LearningStep]] = None
    status: Optional[str] = None
    difficulty_level: Optional[str] = None
    estimated_duration: Optional[int] = None

class LearningPlan(LearningPlanBase):
    id: int
    user_id: int
    repository_id: int
    learning_steps: List[LearningStep]
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    user: User
    repository: Repository

    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

# Response schemas
class LearningPlanWithDetails(LearningPlan):
    """Learning plan with full user and repository details"""
    pass

class UserWithLearningPlans(User):
    """User with their learning plans"""
    learning_plans: List[LearningPlan] = []

class RepositoryWithLearningPlans(Repository):
    """Repository with learning plans"""
    learning_plans: List[LearningPlan] = []

# GitHub Search schemas
class GitHubRepositoryInfo(BaseModel):
    """GitHub repository information from API"""
    id: int
    name: str
    full_name: str
    description: Optional[str] = None
    html_url: str
    clone_url: str
    language: Optional[str] = None
    languages: Optional[List[str]] = None
    topics: Optional[List[str]] = None
    stars: int
    forks: int
    watchers: int
    open_issues: int
    size: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    readme_preview: Optional[str] = None
    default_branch: Optional[str] = None
    license: Optional[str] = None
    archived: bool
    fork: bool
    private: bool

class SearchRequest(BaseModel):
    """Request model for repository search"""
    query: str  # Can be GitHub URL or search term
    limit: Optional[int] = 10

class SearchResponse(BaseModel):
    """Response model for repository search"""
    query: str
    search_type: str  # "url" or "search"
    repositories: List[GitHubRepositoryInfo]
    ai_prerequisites: Optional[List[str]] = None
    total_count: int

# Learning Plan Generation schemas
class LearningStepDetail(BaseModel):
    """Detailed learning step with additional information"""
    step: int
    title: str
    description: str
    duration: str
    resources: List[str]
    exercises: List[str]
    completed: bool = False

class CodingExercise(BaseModel):
    """Individual coding exercise with validation"""
    id: str
    title: str
    description: str
    difficulty: str  # "beginner", "intermediate", "advanced"
    code_template: str  # Code with placeholders like {{variable_name}}
    solution: str  # Complete solution
    hints: List[str]
    validation_rules: List[str]  # Rules for validation
    expected_output: Optional[str] = None
    test_cases: List[dict] = []  # Test cases for validation
    blanks: List[Dict[str, str]] = []  # Fill-in-the-blank definitions

class CodingExerciseSubmission(BaseModel):
    """User submission for a coding exercise"""
    exercise_id: str
    user_code: str
    step_number: int

class CodingExerciseValidation(BaseModel):
    """Validation result for coding exercise"""
    exercise_id: str
    is_correct: bool
    feedback: str
    hints: List[str]
    score: int  # 0-100
    execution_result: Optional[str] = None
    error_message: Optional[str] = None

class EnhancedLearningStepDetail(BaseModel):
    """Enhanced learning step with coding exercises"""
    step: int
    title: str
    description: str
    duration: str
    resources: List[str]
    exercises: List[str]
    coding_exercises: List[CodingExercise] = []
    completed: bool = False
    exercises_completed: int = 0
    total_exercises: int = 0

class GeneratedLearningPlan(BaseModel):
    """AI-generated learning plan"""
    title: str
    description: str
    difficulty_level: str
    estimated_duration: str
    learning_steps: List[EnhancedLearningStepDetail]
    prerequisites: List[str]
    learning_objectives: List[str]
    technologies_covered: List[str]

class GeneratePlanRequest(BaseModel):
    """Request model for learning plan generation"""
    repository_id: Optional[int] = None
    repository_url: Optional[str] = None
    repository_info: Optional[GitHubRepositoryInfo] = None

class GeneratePlanResponse(BaseModel):
    """Response model for learning plan generation"""
    success: bool
    learning_plan: Optional[GeneratedLearningPlan] = None
    repository_info: Optional[GitHubRepositoryInfo] = None
    error_message: Optional[str] = None
