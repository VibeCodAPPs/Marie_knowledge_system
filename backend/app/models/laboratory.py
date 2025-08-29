"""
Laboratory model for organizing knowledge domains.
"""

from sqlalchemy import Column, String, Text, Boolean, JSON, Integer
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class Laboratory(Base, TimestampMixin):
    """
    Laboratory represents a knowledge domain (e.g., AI, Philosophy, Physics).
    Each laboratory is an isolated workspace with its own concepts, sources, and configuration.
    """
    
    __tablename__ = "laboratories"
    
    # Basic information
    name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text)
    color = Column(String(7), default="#3B82F6")  # Hex color for UI
    icon = Column(String(50), default="🧪")  # Emoji or icon identifier
    
    # Status and configuration
    is_active = Column(Boolean, default=True, nullable=False)
    is_archived = Column(Boolean, default=False, nullable=False)
    
    # Laboratory-specific settings
    settings = Column(JSON, default=dict)  # Custom configurations
    
    # AI model preferences for this laboratory
    lightweight_model = Column(String(100))  # For quick analysis
    deep_model = Column(String(100))  # For complex analysis
    
    # Statistics (computed fields)
    concept_count = Column(Integer, default=0)
    source_count = Column(Integer, default=0)
    study_hours = Column(Integer, default=0)  # Total study time in minutes
    
    # Relationships
    concepts = relationship("Concept", back_populates="laboratory", cascade="all, delete-orphan")
    sources = relationship("Source", back_populates="laboratory", cascade="all, delete-orphan")
    notebook_entries = relationship("NotebookEntry", back_populates="laboratory", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Laboratory(id={self.id}, name='{self.name}', active={self.is_active})>"
    
    @property
    def display_name(self):
        """Display name with icon for UI."""
        return f"{self.icon} {self.name}"
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "color": self.color,
            "icon": self.icon,
            "is_active": self.is_active,
            "is_archived": self.is_archived,
            "settings": self.settings,
            "lightweight_model": self.lightweight_model,
            "deep_model": self.deep_model,
            "concept_count": self.concept_count,
            "source_count": self.source_count,
            "study_hours": self.study_hours,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "display_name": self.display_name
        }
