from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List, Union
import jwt
from passlib.context import CryptContext
import os
import re
import json
from urllib.parse import urlparse
from github import Github, GithubException

# Import database models and schemas
from database.database import get_db, User, Repository, LearningPlan, get_user_by_username

# Import services
from services.learning_plan_service import LearningPlanService
from services.code_validator import code_validator
from services.exercise_generator import exercise_generator
from database.schemas import (
    User as UserSchema, UserCreate, UserUpdate,
    Repository as RepositorySchema, RepositoryCreate, RepositoryUpdate,
    LearningPlan as LearningPlanSchema, LearningPlanCreate, LearningPlanUpdate,
    Token, TokenData, UserLogin, LearningStep,
    GitHubRepositoryInfo, SearchRequest, SearchResponse,
    GeneratedLearningPlan, GeneratePlanRequest, GeneratePlanResponse, EnhancedLearningStepDetail,
    CodingExercise, CodingExerciseSubmission, CodingExerciseValidation
)

# Create FastAPI app instance
app = FastAPI(
    title="CodeLap Lean API",
    description="A FastAPI application for CodeLap Lean project",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token security
security = HTTPBearer()

# GitHub configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
github_client = Github(GITHUB_TOKEN) if GITHUB_TOKEN else Github()

# Learning Plan Service
learning_plan_service = LearningPlanService()

# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# GitHub utility functions
def is_github_url(url: str) -> bool:
    """Check if the provided string is a GitHub URL"""
    try:
        parsed = urlparse(url)
        return parsed.netloc in ['github.com', 'www.github.com']
    except:
        return False

def extract_repo_info_from_url(url: str) -> tuple:
    """Extract owner and repo name from GitHub URL"""
    try:
        # Remove trailing slash and split by '/'
        url = url.rstrip('/')
        parts = url.split('/')
        
        # Find github.com in the URL
        github_index = -1
        for i, part in enumerate(parts):
            if 'github.com' in part:
                github_index = i
                break
        
        if github_index == -1 or github_index + 2 >= len(parts):
            raise ValueError("Invalid GitHub URL format")
        
        owner = parts[github_index + 1]
        repo_name = parts[github_index + 2]
        
        return owner, repo_name
    except Exception as e:
        raise ValueError(f"Could not parse GitHub URL: {str(e)}")

def get_repository_details(owner: str, repo_name: str) -> dict:
    """Get detailed information about a specific repository"""
    try:
        repo = github_client.get_repo(f"{owner}/{repo_name}")
        
        # Get topics
        topics = list(repo.get_topics()) if repo.get_topics() else []
        
        # Get languages
        languages = list(repo.get_languages().keys()) if repo.get_languages() else []
        
        # Get README content (first 500 characters)
        readme_content = ""
        try:
            readme = repo.get_readme()
            readme_content = readme.decoded_content.decode('utf-8')[:500]
        except:
            pass
        
        return {
            "id": repo.id,
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "html_url": repo.html_url,
            "clone_url": repo.clone_url,
            "language": repo.language,
            "languages": languages,
            "topics": topics,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "watchers": repo.watchers_count,
            "open_issues": repo.open_issues_count,
            "size": repo.size,
            "created_at": repo.created_at.isoformat() if repo.created_at else None,
            "updated_at": repo.updated_at.isoformat() if repo.updated_at else None,
            "readme_preview": readme_content,
            "default_branch": repo.default_branch,
            "license": repo.license.name if hasattr(repo, 'license') and repo.license else None,
            "archived": repo.archived,
            "fork": repo.fork,
            "private": repo.private
        }
    except GithubException as e:
        if e.status == 404:
            raise HTTPException(status_code=404, detail="Repository not found")
        elif e.status == 403:
            raise HTTPException(status_code=403, detail="Access denied. Check your GitHub token.")
        else:
            raise HTTPException(status_code=500, detail=f"GitHub API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching repository: {str(e)}")

def search_python_repositories(query: str, limit: int = 10) -> List[dict]:
    """Search for Python repositories based on a query"""
    try:
        # Search for Python repositories
        search_query = f"{query} language:python"
        repositories = github_client.search_repositories(
            query=search_query,
            sort="stars",
            order="desc"
        )
        
        results = []
        for repo in repositories[:limit]:
            # Get basic info
            repo_info = {
                "id": repo.id,
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "html_url": repo.html_url,
                "clone_url": repo.clone_url,
                "language": repo.language,
                "languages": [],
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "watchers": repo.watchers_count,
                "open_issues": repo.open_issues_count,
                "size": repo.size,
                "created_at": repo.created_at.isoformat() if repo.created_at else None,
                "updated_at": repo.updated_at.isoformat() if repo.updated_at else None,
                "readme_preview": "",
                "default_branch": repo.default_branch,
                "license": repo.license.name if hasattr(repo, 'license') and repo.license else None,
                "archived": repo.archived,
                "fork": repo.fork,
                "private": repo.private
            }
            
            # Get topics if available
            try:
                topics = list(repo.get_topics())
                repo_info["topics"] = topics
            except:
                repo_info["topics"] = []
            
            results.append(repo_info)
        
        return results
    except GithubException as e:
        if e.status == 403:
            raise HTTPException(status_code=403, detail="Access denied. Check your GitHub token.")
        else:
            raise HTTPException(status_code=500, detail=f"GitHub API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching repositories: {str(e)}")

def generate_ai_prerequisites(repo_info: dict) -> List[str]:
    """Generate AI-suggested prerequisites based on repository information"""
    prerequisites = []
    
    # Basic prerequisites based on language
    if repo_info.get("language"):
        if repo_info["language"].lower() == "python":
            prerequisites.append("Basic Python knowledge")
            prerequisites.append("Understanding of Python syntax and data structures")
        elif repo_info["language"].lower() == "javascript":
            prerequisites.append("JavaScript fundamentals")
            prerequisites.append("Understanding of ES6+ features")
        elif repo_info["language"].lower() == "java":
            prerequisites.append("Java programming basics")
            prerequisites.append("Object-oriented programming concepts")
    
    # Prerequisites based on topics
    topics = repo_info.get("topics", [])
    if "api" in topics or "rest" in topics:
        prerequisites.append("Understanding of HTTP and REST APIs")
    if "web" in topics or "frontend" in topics:
        prerequisites.append("HTML and CSS basics")
    if "database" in topics or "sql" in topics:
        prerequisites.append("Database concepts and SQL")
    if "machine-learning" in topics or "ai" in topics:
        prerequisites.append("Basic understanding of machine learning concepts")
    if "docker" in topics or "containerization" in topics:
        prerequisites.append("Docker and containerization basics")
    if "testing" in topics:
        prerequisites.append("Software testing principles")
    
    # Prerequisites based on repository characteristics
    if repo_info.get("stars", 0) > 1000:
        prerequisites.append("Intermediate programming skills")
    if repo_info.get("forks", 0) > 100:
        prerequisites.append("Understanding of version control (Git)")
    
    # Add general prerequisites
    prerequisites.extend([
        "Basic command line usage",
        "Understanding of version control concepts"
    ])
    
    return list(set(prerequisites))  # Remove duplicates

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to CodeLap Lean API"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/login", response_model=Token)
async def login_for_access_token(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login endpoint that returns JWT token"""
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information (protected endpoint)"""
    return current_user

@app.get("/protected")
async def protected_endpoint(current_user: User = Depends(get_current_active_user)):
    """Example protected endpoint"""
    return {
        "message": "This is a protected endpoint",
        "user": current_user.username,
        "full_name": current_user.full_name
    }

@app.post("/register", response_model=UserSchema)
async def register_user(user_credentials: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if username already exists
    existing_user = get_user_by_username(db, user_credentials.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_credentials.password)
    db_user = User(
        username=user_credentials.username,
        email=user_credentials.email,
        full_name=user_credentials.full_name,
        hashed_password=hashed_password,
        disabled=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Repository endpoints
@app.post("/repositories/", response_model=RepositorySchema)
async def create_repository(
    repository: RepositoryCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new repository"""
    db_repository = Repository(**repository.dict())
    db.add(db_repository)
    db.commit()
    db.refresh(db_repository)
    return db_repository

@app.get("/repositories/", response_model=List[RepositorySchema])
async def get_repositories(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Get all repositories"""
    repositories = db.query(Repository).offset(skip).limit(limit).all()
    return repositories

@app.get("/repositories/{repository_id}", response_model=RepositorySchema)
async def get_repository(repository_id: int, db: Session = Depends(get_db)):
    """Get a specific repository"""
    repository = db.query(Repository).filter(Repository.id == repository_id).first()
    if repository is None:
        raise HTTPException(status_code=404, detail="Repository not found")
    return repository

# Learning Plan endpoints
@app.post("/learning-plans/", response_model=LearningPlanSchema)
async def create_learning_plan(
    learning_plan: LearningPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new learning plan"""
    db_learning_plan = LearningPlan(
        **learning_plan.dict(),
        user_id=current_user.id
    )
    db.add(db_learning_plan)
    db.commit()
    db.refresh(db_learning_plan)
    return db_learning_plan

@app.get("/learning-plans/", response_model=List[LearningPlanSchema])
async def get_learning_plans(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get learning plans for current user"""
    learning_plans = db.query(LearningPlan).filter(
        LearningPlan.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return learning_plans

@app.get("/learning-plans/{learning_plan_id}", response_model=LearningPlanSchema)
async def get_learning_plan(
    learning_plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific learning plan"""
    learning_plan = db.query(LearningPlan).filter(
        LearningPlan.id == learning_plan_id,
        LearningPlan.user_id == current_user.id
    ).first()
    if learning_plan is None:
        raise HTTPException(status_code=404, detail="Learning plan not found")
    return learning_plan

# GitHub Search endpoint
@app.post("/search-repo", response_model=SearchResponse)
async def search_repository(
    search_request: SearchRequest,
    current_user: User = Depends(get_current_active_user)
):
    """
    Search for repositories on GitHub.
    Accepts either a GitHub URL or a search term.
    If URL is provided, fetches specific repository details.
    If search term is provided, searches for relevant Python repositories.
    """
    query = search_request.query.strip()
    limit = search_request.limit or 10
    
    if is_github_url(query):
        # Handle GitHub URL
        try:
            owner, repo_name = extract_repo_info_from_url(query)
            repo_details = get_repository_details(owner, repo_name)
            
            # Generate AI prerequisites for the specific repository
            ai_prerequisites = generate_ai_prerequisites(repo_details)
            
            return SearchResponse(
                query=query,
                search_type="url",
                repositories=[GitHubRepositoryInfo(**repo_details)],
                ai_prerequisites=ai_prerequisites,
                total_count=1
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing GitHub URL: {str(e)}")
    
    else:
        # Handle search term
        try:
            repositories = search_python_repositories(query, limit)
            
            # Generate AI prerequisites for the first repository (most relevant)
            ai_prerequisites = None
            if repositories:
                ai_prerequisites = generate_ai_prerequisites(repositories[0])
            
            return SearchResponse(
                query=query,
                search_type="search",
                repositories=[GitHubRepositoryInfo(**repo) for repo in repositories],
                ai_prerequisites=ai_prerequisites,
                total_count=len(repositories)
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error searching repositories: {str(e)}")

# Learning Plan Generation endpoint
@app.post("/generate-plan", response_model=GeneratePlanResponse)
async def generate_learning_plan(
    request: GeneratePlanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Generate an AI-powered learning plan for a repository.
    Can accept repository ID, URL, or direct repository information.
    """
    try:
        repo_info = None
        
        # Get repository information from different sources
        if request.repository_id:
            # Get repository from database
            db_repo = db.query(Repository).filter(Repository.id == request.repository_id).first()
            if not db_repo:
                raise HTTPException(status_code=404, detail="Repository not found in database")
            
            repo_info = {
                "id": db_repo.id,
                "name": db_repo.name,
                "description": db_repo.description,
                "html_url": db_repo.repo_url,
                "language": db_repo.language,
                "stars": db_repo.stars,
                "forks": db_repo.forks,
                "topics": json.loads(db_repo.ai_prerequisites) if db_repo.ai_prerequisites else [],
                "size": 0,
                "created_at": db_repo.created_at.isoformat() if db_repo.created_at else None,
                "updated_at": db_repo.updated_at.isoformat() if db_repo.updated_at else None,
                "readme_preview": ""
            }
            
        elif request.repository_url:
            # Fetch repository from GitHub
            if not is_github_url(request.repository_url):
                raise HTTPException(status_code=400, detail="Invalid GitHub URL")
            
            try:
                owner, repo_name = extract_repo_info_from_url(request.repository_url)
                repo_info = get_repository_details(owner, repo_name)
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error fetching repository: {str(e)}")
                
        elif request.repository_info:
            # Use provided repository information
            repo_info = request.repository_info.dict()
            
        else:
            raise HTTPException(status_code=400, detail="Must provide repository_id, repository_url, or repository_info")
        
        # Generate learning plan using the service
        generated_plan = learning_plan_service.generate_learning_plan(repo_info)
        
        # Convert the generated plan to the response format
        learning_steps = []
        for step in generated_plan.get("learning_steps", []):
            # Convert coding_exercises from dict to CodingExercise objects
            if "coding_exercises" in step:
                step["coding_exercises"] = [CodingExercise(**ex) for ex in step["coding_exercises"]]
            learning_steps.append(EnhancedLearningStepDetail(**step))
        
        response_plan = GeneratedLearningPlan(
            title=generated_plan.get("title", ""),
            description=generated_plan.get("description", ""),
            difficulty_level=generated_plan.get("difficulty_level", "intermediate"),
            estimated_duration=generated_plan.get("estimated_duration", "20 hours"),
            learning_steps=learning_steps,
            prerequisites=generated_plan.get("prerequisites", []),
            learning_objectives=generated_plan.get("learning_objectives", []),
            technologies_covered=generated_plan.get("technologies_covered", [])
        )
        
        # Store the learning plan in the database
        db_learning_plan = LearningPlan(
            user_id=current_user.id,
            repository_id=repo_info.get("id") if repo_info.get("id") else None,
            title=response_plan.title,
            description=response_plan.description,
            learning_steps=json.dumps([step.dict() for step in response_plan.learning_steps]),
            status="active",
            difficulty_level=response_plan.difficulty_level,
            estimated_duration=int(response_plan.estimated_duration.split()[0]) if response_plan.estimated_duration.split()[0].isdigit() else 20
        )
        
        db.add(db_learning_plan)
        db.commit()
        db.refresh(db_learning_plan)
        
        return GeneratePlanResponse(
            success=True,
            learning_plan=response_plan,
            repository_info=GitHubRepositoryInfo(**repo_info) if repo_info else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error generating learning plan: {e}")
        return GeneratePlanResponse(
            success=False,
            error_message=f"Error generating learning plan: {str(e)}"
        )

@app.post("/validate-code", response_model=CodingExerciseValidation)
async def validate_code(
    submission: CodingExerciseSubmission,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Validate user code submission for a coding exercise"""
    try:
        # Get the exercise details (in a real app, you'd fetch this from database)
        # For now, we'll use a simple validation approach
        
        # Get the exercise details (in a real app, you'd fetch this from database)
        # For now, we'll use a simple validation approach
        
        # Basic validation using the code validator
        validation_result = code_validator.validate_exercise(
            user_code=submission.user_code,
            exercise={
                "solution": "",  # We don't expose the solution
                "validation_rules": [
                    "contains:print",  # Basic validation rules
                    "contains:def"
                ],
                "blanks": []  # Add blanks if available
            }
        )
        
        return CodingExerciseValidation(
            exercise_id=submission.exercise_id,
            is_correct=validation_result.is_valid,
            feedback=validation_result.feedback,
            hints=validation_result.hints or [],
            score=validation_result.score,
            execution_result=validation_result.execution_result,
            error_message=validation_result.error_message
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating code: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
