"""
Laboratory endpoints for Marie Knowledge System
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.laboratory import Laboratory
from app.schemas.laboratory import LaboratoryCreate, LaboratoryResponse, LaboratoryUpdate

router = APIRouter()


@router.get("/", response_model=List[LaboratoryResponse])
async def get_laboratories(db: Session = Depends(get_db)):
    """Get all laboratories"""
    laboratories = db.query(Laboratory).filter(Laboratory.is_active == True).all()
    return laboratories


@router.post("/", response_model=LaboratoryResponse)
async def create_laboratory(
    laboratory: LaboratoryCreate,
    db: Session = Depends(get_db)
):
    """Create a new laboratory"""
    db_laboratory = Laboratory(**laboratory.dict())
    db.add(db_laboratory)
    db.commit()
    db.refresh(db_laboratory)
    return db_laboratory


@router.get("/{laboratory_id}", response_model=LaboratoryResponse)
async def get_laboratory(laboratory_id: int, db: Session = Depends(get_db)):
    """Get a specific laboratory by ID"""
    laboratory = db.query(Laboratory).filter(Laboratory.id == laboratory_id).first()
    if not laboratory:
        raise HTTPException(status_code=404, detail="Laboratory not found")
    return laboratory


@router.put("/{laboratory_id}", response_model=LaboratoryResponse)
async def update_laboratory(
    laboratory_id: int,
    laboratory_update: LaboratoryUpdate,
    db: Session = Depends(get_db)
):
    """Update a laboratory"""
    laboratory = db.query(Laboratory).filter(Laboratory.id == laboratory_id).first()
    if not laboratory:
        raise HTTPException(status_code=404, detail="Laboratory not found")
    
    for field, value in laboratory_update.dict(exclude_unset=True).items():
        setattr(laboratory, field, value)
    
    db.commit()
    db.refresh(laboratory)
    return laboratory


@router.delete("/{laboratory_id}")
async def delete_laboratory(laboratory_id: int, db: Session = Depends(get_db)):
    """Soft delete a laboratory"""
    laboratory = db.query(Laboratory).filter(Laboratory.id == laboratory_id).first()
    if not laboratory:
        raise HTTPException(status_code=404, detail="Laboratory not found")
    
    laboratory.is_active = False
    db.commit()
    return {"message": "Laboratory deleted successfully"}
