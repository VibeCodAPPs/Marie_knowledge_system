"""
Database configuration and initialization for Marie Knowledge System
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import asyncio
from pathlib import Path

from app.core.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=settings.DEBUG
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Metadata for database operations
metadata = MetaData()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db():
    """Initialize database with tables"""
    # Import all models to ensure they are registered
    from app.models import laboratory, concept, source, tag, notebook, assessment
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create default data if needed
    await create_default_data()


async def create_default_data():
    """Create default laboratories and initial data"""
    db = SessionLocal()
    try:
        from app.models.laboratory import Laboratory
        
        # Check if we already have laboratories
        existing_labs = db.query(Laboratory).count()
        if existing_labs == 0:
            # Create default laboratories
            default_labs = [
                {
                    "name": "Laboratorio de Inteligencia Artificial",
                    "description": "Espacio dedicado al estudio de IA, ML, y tecnologías relacionadas",
                    "color_theme": "#FF6B6B",
                    "icon": "🤖"
                },
                {
                    "name": "Laboratorio de Filosofía",
                    "description": "Exploración de conceptos filosóficos y pensamiento crítico",
                    "color_theme": "#4ECDC4", 
                    "icon": "🏛️"
                }
            ]
            
            for lab_data in default_labs:
                lab = Laboratory(**lab_data)
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
