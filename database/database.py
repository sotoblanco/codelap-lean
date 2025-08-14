from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime
import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./codelap_lean.db")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    full_name = Column(String(100), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    learning_plans = relationship("LearningPlan", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    repo_url = Column(String(500), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    ai_prerequisites = Column(JSON, nullable=True)  # Store AI-generated prerequisites as JSON
    language = Column(String(50), nullable=True)
    stars = Column(Integer, default=0)
    forks = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    learning_plans = relationship("LearningPlan", back_populates="repository", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Repository(id={self.id}, name='{self.name}', url='{self.repo_url}')>"


class LearningPlan(Base):
    __tablename__ = "learning_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    learning_steps = Column(JSON, nullable=False)  # Store learning steps as JSON array
    status = Column(String(20), default="active")  # active, completed, paused
    difficulty_level = Column(String(20), nullable=True)  # beginner, intermediate, advanced
    estimated_duration = Column(Integer, nullable=True)  # in hours
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="learning_plans")
    repository = relationship("Repository", back_populates="learning_plans")

    def __repr__(self):
        return f"<LearningPlan(id={self.id}, title='{self.title}', user_id={self.user_id})>"


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create all tables
def create_tables():
    Base.metadata.create_all(bind=engine)


# Database utility functions
def init_db():
    """Initialize the database with tables"""
    create_tables()
    print("Database tables created successfully!")


def get_user_by_username(db, username: str):
    """Get user by username"""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db, email: str):
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def get_repository_by_url(db, repo_url: str):
    """Get repository by URL"""
    return db.query(Repository).filter(Repository.repo_url == repo_url).first()


def get_learning_plans_by_user(db, user_id: int):
    """Get all learning plans for a user"""
    return db.query(LearningPlan).filter(LearningPlan.user_id == user_id).all()


def get_learning_plans_by_repository(db, repository_id: int):
    """Get all learning plans for a repository"""
    return db.query(LearningPlan).filter(LearningPlan.repository_id == repository_id).all()


# Example usage and initialization
if __name__ == "__main__":
    init_db()
