"""
Database configuration and initialization for Marie Knowledge System
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# Database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency to get database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables.
    """
    # Import all models to ensure they are registered
    from app.models import (
        Laboratory, Concept, Source, Tag, NotebookEntry, 
        ConceptRelationship, ConceptTag
    )
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create default data
    db = SessionLocal()
    try:
        # Check if we have any laboratories
        existing_labs = db.query(Laboratory).count()
        if existing_labs == 0:
            # Create default laboratories
            default_labs = [
                Laboratory(
                    name="Getting Started",
                    description="Your first laboratory to explore Marie's features",
                    color="#3B82F6",
                    icon="🚀",
                    is_active=True
                ),
                Laboratory(
                    name="Artificial Intelligence",
                    description="Machine Learning, Deep Learning, and AI applications",
                    color="#10B981",
                    icon="🤖",
                    is_active=True
                ),
                Laboratory(
                    name="Philosophy",
                    description="Stoicism, Ethics, and Modern Philosophy",
                    color="#8B5CF6",
                    icon="🏛️",
                    is_active=True
                )
            ]
            
            for lab in default_labs:
                db.add(lab)
            
            db.commit()
            print("✅ Default laboratories created")
    
    except Exception as e:
        print(f"❌ Error creating default data: {e}")
        db.rollback()
    finally:
        db.close()


def reset_database():
    """Reset database - USE WITH CAUTION"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("🔄 Database reset completed")
