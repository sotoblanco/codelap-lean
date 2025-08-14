#!/usr/bin/env python3
"""
Database initialization script
Creates tables and optionally seeds with initial data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import init_db, SessionLocal, User, Repository, LearningPlan
from passlib.context import CryptContext
import json

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def seed_initial_data():
    """Seed the database with initial data"""
    db = SessionLocal()
    
    try:
        # Check if we already have users
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("Database already has data, skipping seeding...")
            return

        # Create initial users
        users = [
            User(
                username="johndoe",
                email="johndoe@example.com",
                full_name="John Doe",
                hashed_password=get_password_hash("secret"),
                disabled=False
            ),
            User(
                username="alice",
                email="alice@example.com",
                full_name="Alice Wonderson",
                hashed_password=get_password_hash("secret"),
                disabled=False
            )
        ]
        
        for user in users:
            db.add(user)
        db.commit()
        
        # Create sample repositories
        repositories = [
            Repository(
                repo_url="https://github.com/example/fastapi-tutorial",
                name="FastAPI Tutorial",
                description="A comprehensive tutorial for building APIs with FastAPI",
                ai_prerequisites=json.dumps([
                    "Basic Python knowledge",
                    "Understanding of HTTP and REST APIs",
                    "Familiarity with async/await syntax"
                ]),
                language="Python",
                stars=1500,
                forks=300
            ),
            Repository(
                repo_url="https://github.com/example/react-learning",
                name="React Learning Path",
                description="Complete learning path for React development",
                ai_prerequisites=json.dumps([
                    "JavaScript fundamentals",
                    "HTML and CSS basics",
                    "Understanding of component-based architecture"
                ]),
                language="JavaScript",
                stars=2200,
                forks=450
            )
        ]
        
        for repo in repositories:
            db.add(repo)
        db.commit()
        
        # Create sample learning plans
        learning_plans = [
            LearningPlan(
                user_id=1,  # johndoe
                repository_id=1,  # FastAPI Tutorial
                title="Master FastAPI Development",
                description="Complete learning plan to become proficient in FastAPI",
                learning_steps=json.dumps([
                    {"step": 1, "title": "Setup Development Environment", "description": "Install Python and FastAPI", "completed": False},
                    {"step": 2, "title": "Basic FastAPI Concepts", "description": "Learn about routes, requests, and responses", "completed": False},
                    {"step": 3, "title": "Database Integration", "description": "Connect FastAPI with SQLAlchemy", "completed": False},
                    {"step": 4, "title": "Authentication & Authorization", "description": "Implement JWT authentication", "completed": False},
                    {"step": 5, "title": "Testing", "description": "Write tests for your FastAPI application", "completed": False}
                ]),
                status="active",
                difficulty_level="intermediate",
                estimated_duration=20
            ),
            LearningPlan(
                user_id=2,  # alice
                repository_id=2,  # React Learning Path
                title="React Fundamentals",
                description="Learn React from scratch to advanced concepts",
                learning_steps=json.dumps([
                    {"step": 1, "title": "React Basics", "description": "Components, JSX, and props", "completed": False},
                    {"step": 2, "title": "State Management", "description": "useState and useEffect hooks", "completed": False},
                    {"step": 3, "title": "Routing", "description": "React Router implementation", "completed": False},
                    {"step": 4, "title": "State Management Libraries", "description": "Redux or Context API", "completed": False},
                    {"step": 5, "title": "Testing", "description": "Testing React components", "completed": False}
                ]),
                status="active",
                difficulty_level="beginner",
                estimated_duration=25
            )
        ]
        
        for plan in learning_plans:
            db.add(plan)
        db.commit()
        
        print("Database seeded with initial data successfully!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Seeding initial data...")
    seed_initial_data()
    print("Database setup complete!") 