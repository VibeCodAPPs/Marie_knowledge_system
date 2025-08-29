"""
Tag model for categorizing and organizing concepts.
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class Tag(Base, TimestampMixin):
    """
    Tag represents a label or category for organizing concepts.
    Tags enable flexible categorization and filtering of knowledge.
    """
    
    __tablename__ = "tags"
    
    # Basic information
    name = Column(String(50), nullable=False, index=True)
    description = Column(Text)
    color = Column(String(7), default="#6B7280")  # Hex color for UI
    
    # Laboratory association (tags can be laboratory-specific)
    laboratory_id = Column(Integer, ForeignKey("laboratories.id"), nullable=True, index=True)
    
    # Tag hierarchy (optional parent-child relationships)
    parent_id = Column(Integer, ForeignKey("tags.id"), nullable=True)
    
    # Usage statistics
    usage_count = Column(Integer, default=0)
    is_system_tag = Column(Boolean, default=False)  # System vs user-created tags
    is_active = Column(Boolean, default=True)
    
    # Relationships
    laboratory = relationship("Laboratory", backref="tags")
    parent = relationship("Tag", remote_side="Tag.id", backref="children")
    concepts = relationship("Concept", secondary="concept_tags", back_populates="tags")
    
    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}', lab={self.laboratory_id})>"
    
    @property
    def full_name(self):
        """Full hierarchical name (parent/child)."""
        if self.parent:
            return f"{self.parent.name}/{self.name}"
        return self.name
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            "id": self.id,
            "name": self.name,
            "full_name": self.full_name,
            "description": self.description,
            "color": self.color,
            "laboratory_id": self.laboratory_id,
            "parent_id": self.parent_id,
            "usage_count": self.usage_count,
            "is_system_tag": self.is_system_tag,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
