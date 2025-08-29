"""
Notebook model for laboratory journal entries and learning progress.
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, Float, Boolean, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import Base, TimestampMixin


class EntryType(PyEnum):
    """Types of notebook entries."""
    NOTE = "note"
    INSIGHT = "insight"
    QUESTION = "question"
    PROGRESS = "progress"
    REFLECTION = "reflection"
    PLAN = "plan"
    REVIEW = "review"
    DISCOVERY = "discovery"


class NotebookEntry(Base, TimestampMixin):
    """
    NotebookEntry represents entries in the laboratory notebook.
    Used for tracking learning progress, insights, and reflections.
    """
    
    __tablename__ = "notebook_entries"
    
    # Basic information
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    entry_type = Column(Enum(EntryType), nullable=False, index=True)
    
    # Laboratory association
    laboratory_id = Column(Integer, ForeignKey("laboratories.id"), nullable=False, index=True)
    
    # Related concepts and sources
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True, index=True)
    
    # Learning context
    study_session_id = Column(String(50))  # Group related entries
    mood_score = Column(Integer)  # 1-5 learning mood/energy
    difficulty_rating = Column(Integer)  # 1-5 perceived difficulty
    understanding_level = Column(Float, default=0.0)  # 0-1 comprehension
    
    # Progress tracking
    time_spent = Column(Integer, default=0)  # Minutes spent on this entry
    is_milestone = Column(Boolean, default=False)
    is_favorite = Column(Boolean, default=False)
    is_private = Column(Boolean, default=False)
    
    # AI analysis
    sentiment_score = Column(Float)  # -1 to 1 sentiment analysis
    key_insights = Column(Text)  # JSON array of extracted insights
    suggested_actions = Column(Text)  # AI-suggested next steps
    
    # Relationships
    laboratory = relationship("Laboratory", back_populates="notebook_entries")
    concept = relationship("Concept", backref="notebook_entries")
    source = relationship("Source", backref="notebook_entries")
    
    def __repr__(self):
        return f"<NotebookEntry(id={self.id}, title='{self.title[:30]}...', type={self.entry_type.value})>"
    
    @property
    def display_type(self):
        """Human-readable entry type with emoji."""
        type_icons = {
            EntryType.NOTE: "📝 Note",
            EntryType.INSIGHT: "💡 Insight",
            EntryType.QUESTION: "❓ Question",
            EntryType.PROGRESS: "📈 Progress",
            EntryType.REFLECTION: "🤔 Reflection",
            EntryType.PLAN: "📋 Plan",
            EntryType.REVIEW: "🔍 Review",
            EntryType.DISCOVERY: "🔬 Discovery"
        }
        return type_icons.get(self.entry_type, "📄 Entry")
    
    @property
    def mood_emoji(self):
        """Emoji representation of mood score."""
        if not self.mood_score:
            return "😐"
        mood_emojis = {1: "😫", 2: "😕", 3: "😐", 4: "😊", 5: "🤩"}
        return mood_emojis.get(self.mood_score, "😐")
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "entry_type": self.entry_type.value,
            "display_type": self.display_type,
            "laboratory_id": self.laboratory_id,
            "concept_id": self.concept_id,
            "source_id": self.source_id,
            "study_session_id": self.study_session_id,
            "mood_score": self.mood_score,
            "mood_emoji": self.mood_emoji,
            "difficulty_rating": self.difficulty_rating,
            "understanding_level": self.understanding_level,
            "time_spent": self.time_spent,
            "is_milestone": self.is_milestone,
            "is_favorite": self.is_favorite,
            "is_private": self.is_private,
            "sentiment_score": self.sentiment_score,
            "key_insights": self.key_insights,
            "suggested_actions": self.suggested_actions,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
