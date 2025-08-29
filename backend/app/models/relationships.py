"""
Relationship models for connecting concepts and managing associations.
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, Float, Boolean, Enum, Table, DateTime
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from datetime import datetime
from .base import Base, TimestampMixin


class RelationshipType(PyEnum):
    """Types of relationships between concepts."""
    SEMANTIC = "semantic"        # Similar meaning or topic
    CAUSAL = "causal"           # Cause and effect
    HIERARCHICAL = "hierarchical"  # Parent-child, general-specific
    TEMPORAL = "temporal"       # Time-based sequence
    CONTRADICTORY = "contradictory"  # Opposing ideas
    COMPLEMENTARY = "complementary"  # Supporting ideas


# Association table for many-to-many relationship between concepts and tags
concept_tags = Table(
    'concept_tags',
    Base.metadata,
    Column('concept_id', Integer, ForeignKey('concepts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True),
    Column('created_at', DateTime, default=datetime.utcnow)
)


class ConceptRelationship(Base, TimestampMixin):
    """
    ConceptRelationship represents bidirectional connections between concepts.
    Implements the core of the knowledge graph structure.
    """
    
    __tablename__ = "concept_relationships"
    
    # Source and target concepts
    source_concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False, index=True)
    target_concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False, index=True)
    
    # Relationship metadata
    relationship_type = Column(Enum(RelationshipType), nullable=False, index=True)
    description = Column(Text)  # Optional description of the relationship
    
    # Strength and confidence
    strength = Column(Float, default=0.5)  # 0-1 relationship strength
    confidence = Column(Float, default=0.5)  # 0-1 confidence in relationship
    
    # Source of relationship (human, AI, automatic)
    created_by = Column(String(20), default="system")  # "user", "ai", "system"
    is_validated = Column(Boolean, default=False)  # Human validation
    is_bidirectional = Column(Boolean, default=True)  # Most relationships are bidirectional
    
    # Usage and learning
    access_count = Column(Integer, default=0)  # How often this relationship is accessed
    is_active = Column(Boolean, default=True)
    
    # Relationships
    source_concept = relationship("Concept", foreign_keys=[source_concept_id], back_populates="child_relationships")
    target_concept = relationship("Concept", foreign_keys=[target_concept_id], back_populates="parent_relationships")
    
    def __repr__(self):
        return f"<ConceptRelationship(id={self.id}, {self.source_concept_id}->{self.target_concept_id}, type={self.relationship_type.value})>"
    
    @property
    def display_type(self):
        """Human-readable relationship type with emoji."""
        type_icons = {
            RelationshipType.SEMANTIC: "🔗 Similar",
            RelationshipType.CAUSAL: "➡️ Causes",
            RelationshipType.HIERARCHICAL: "🌳 Contains",
            RelationshipType.TEMPORAL: "⏰ Follows",
            RelationshipType.CONTRADICTORY: "⚡ Opposes",
            RelationshipType.COMPLEMENTARY: "🤝 Supports"
        }
        return type_icons.get(self.relationship_type, "🔗 Related")
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            "id": self.id,
            "source_concept_id": self.source_concept_id,
            "target_concept_id": self.target_concept_id,
            "relationship_type": self.relationship_type.value,
            "display_type": self.display_type,
            "description": self.description,
            "strength": self.strength,
            "confidence": self.confidence,
            "created_by": self.created_by,
            "is_validated": self.is_validated,
            "is_bidirectional": self.is_bidirectional,
            "access_count": self.access_count,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class ConceptTagAssociation(Base):
    """
    ConceptTagAssociation represents the many-to-many relationship between concepts and tags.
    This is handled by the concept_tags association table, but we can add metadata here if needed.
    """
    
    __tablename__ = "concept_tag_metadata"
    
    concept_id = Column(Integer, ForeignKey("concepts.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Optional metadata for the tag assignment
    confidence = Column(Float, default=1.0)  # Confidence in tag assignment
    assigned_by = Column(String(20), default="user")  # "user", "ai", "system"
    
    def __repr__(self):
        return f"<ConceptTag(concept_id={self.concept_id}, tag_id={self.tag_id})>"
