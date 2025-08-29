"""
Concept model for atomic knowledge units.
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class Concept(Base, TimestampMixin):
    """
    Concept represents an atomic unit of knowledge following Zettelkasten principles.
    Each concept is self-contained and can be linked to other concepts.
    """
    
    __tablename__ = "concepts"
    
    # Basic information
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    summary = Column(Text)  # AI-generated summary
    
    # Zettelkasten ID (unique identifier like "202501280001")
    zettel_id = Column(String(20), unique=True, index=True)
    
    # Laboratory association
    laboratory_id = Column(Integer, ForeignKey("laboratories.id"), nullable=False, index=True)
    
    # Source information
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True, index=True)
    source_location = Column(String(100))  # Page number, timestamp, etc.
    
    # AI analysis
    embedding_vector = Column(Text)  # JSON string of vector embeddings
    complexity_score = Column(Float, default=0.0)  # 0-1 difficulty rating
    importance_score = Column(Float, default=0.0)  # 0-1 importance rating
    
    # Learning progress
    mastery_level = Column(Integer, default=0)  # 0=new, 1=learning, 2=review, 3=mastered
    review_count = Column(Integer, default=0)
    last_reviewed = Column(DateTime)
    next_review = Column(DateTime)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_validated = Column(Boolean, default=False)  # Human or AI validation
    
    # Relationships
    laboratory = relationship("Laboratory", back_populates="concepts")
    source = relationship("Source", back_populates="concepts")
    tags = relationship("Tag", secondary="concept_tags", back_populates="concepts")
    
    # Self-referential relationships for concept connections
    parent_relationships = relationship(
        "ConceptRelationship",
        foreign_keys="ConceptRelationship.target_concept_id",
        back_populates="target_concept"
    )
    child_relationships = relationship(
        "ConceptRelationship", 
        foreign_keys="ConceptRelationship.source_concept_id",
        back_populates="source_concept"
    )
    
    def __repr__(self):
        return f"<Concept(id={self.id}, title='{self.title[:50]}...', lab={self.laboratory_id})>"
    
    @property
    def mastery_status(self):
        """Human-readable mastery status."""
        statuses = {0: "New", 1: "Learning", 2: "Review", 3: "Mastered"}
        return statuses.get(self.mastery_level, "Unknown")
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "summary": self.summary,
            "zettel_id": self.zettel_id,
            "laboratory_id": self.laboratory_id,
            "source_id": self.source_id,
            "source_location": self.source_location,
            "complexity_score": self.complexity_score,
            "importance_score": self.importance_score,
            "mastery_level": self.mastery_level,
            "mastery_status": self.mastery_status,
            "review_count": self.review_count,
            "last_reviewed": self.last_reviewed.isoformat() if self.last_reviewed else None,
            "next_review": self.next_review.isoformat() if self.next_review else None,
            "is_active": self.is_active,
            "is_validated": self.is_validated,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
