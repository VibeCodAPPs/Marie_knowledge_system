"""
Source model for content references and materials.
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, Float, Boolean, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import Base, TimestampMixin


class SourceType(PyEnum):
    """Types of content sources."""
    PDF = "pdf"
    VIDEO = "video"
    ARTICLE = "article"
    BOOK = "book"
    PODCAST = "podcast"
    COURSE = "course"
    PAPER = "paper"
    WEBSITE = "website"
    NOTE = "note"
    OTHER = "other"


class Source(Base, TimestampMixin):
    """
    Source represents external content that concepts are derived from.
    Supports various content types and metadata extraction.
    """
    
    __tablename__ = "sources"
    
    # Basic information
    title = Column(String(300), nullable=False, index=True)
    author = Column(String(200))
    url = Column(Text)
    description = Column(Text)
    
    # Source classification
    source_type = Column(Enum(SourceType), nullable=False, index=True)
    category = Column(String(100))  # Subject category
    language = Column(String(10), default="en")
    
    # Laboratory association
    laboratory_id = Column(Integer, ForeignKey("laboratories.id"), nullable=False, index=True)
    
    # Content metadata
    file_path = Column(String(500))  # Local file path if downloaded
    file_size = Column(Integer)  # Size in bytes
    page_count = Column(Integer)  # For PDFs/books
    duration = Column(Integer)  # For videos/podcasts in seconds
    
    # Quality and relevance
    quality_score = Column(Float, default=0.0)  # 0-1 quality rating
    relevance_score = Column(Float, default=0.0)  # 0-1 relevance to laboratory
    difficulty_level = Column(Integer, default=1)  # 1-5 difficulty scale
    
    # Processing status
    is_processed = Column(Boolean, default=False)
    is_favorite = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    
    # AI analysis
    summary = Column(Text)  # AI-generated summary
    key_topics = Column(Text)  # JSON array of extracted topics
    
    # Academic metadata (for papers/articles)
    doi = Column(String(100))  # Digital Object Identifier
    isbn = Column(String(20))  # For books
    publication_date = Column(String(20))  # YYYY-MM-DD format
    journal = Column(String(200))  # Journal or conference name
    
    # Relationships
    laboratory = relationship("Laboratory", back_populates="sources")
    concepts = relationship("Concept", back_populates="source")
    
    def __repr__(self):
        return f"<Source(id={self.id}, title='{self.title[:50]}...', type={self.source_type.value})>"
    
    @property
    def display_type(self):
        """Human-readable source type."""
        type_names = {
            SourceType.PDF: "📄 PDF",
            SourceType.VIDEO: "🎥 Video", 
            SourceType.ARTICLE: "📰 Article",
            SourceType.BOOK: "📚 Book",
            SourceType.PODCAST: "🎧 Podcast",
            SourceType.COURSE: "🎓 Course",
            SourceType.PAPER: "📋 Paper",
            SourceType.WEBSITE: "🌐 Website",
            SourceType.NOTE: "📝 Note",
            SourceType.OTHER: "📎 Other"
        }
        return type_names.get(self.source_type, "📎 Unknown")
    
    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "url": self.url,
            "description": self.description,
            "source_type": self.source_type.value,
            "display_type": self.display_type,
            "category": self.category,
            "language": self.language,
            "laboratory_id": self.laboratory_id,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "page_count": self.page_count,
            "duration": self.duration,
            "quality_score": self.quality_score,
            "relevance_score": self.relevance_score,
            "difficulty_level": self.difficulty_level,
            "is_processed": self.is_processed,
            "is_favorite": self.is_favorite,
            "is_archived": self.is_archived,
            "summary": self.summary,
            "key_topics": self.key_topics,
            "doi": self.doi,
            "isbn": self.isbn,
            "publication_date": self.publication_date,
            "journal": self.journal,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
