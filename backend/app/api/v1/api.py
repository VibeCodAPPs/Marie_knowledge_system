"""
API router for Marie Knowledge System v1
"""

from fastapi import APIRouter
from app.api.v1.endpoints import laboratories, concepts, sources, search, notebook

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    laboratories.router, 
    prefix="/laboratories", 
    tags=["laboratories"]
)

api_router.include_router(
    concepts.router, 
    prefix="/concepts", 
    tags=["concepts"]
)

api_router.include_router(
    sources.router, 
    prefix="/sources", 
    tags=["sources"]
)

api_router.include_router(
    search.router, 
    prefix="/search", 
    tags=["search"]
)

api_router.include_router(
    notebook.router, 
    prefix="/notebook", 
    tags=["notebook"]
)
