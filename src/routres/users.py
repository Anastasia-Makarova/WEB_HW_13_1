from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_limiter.depends import RateLimiter


from src.entity.models import User
from src.services.auth import auth_service
from src.schemas.user import UserResponse

router = APIRouter(prefix='/users', tags=['users'])

@router.get('/me', response_model=UserResponse, description='No more than 1 requests per 20 sec',
            dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def get_current_user(user: User = Depends(auth_service.get_current_user)):
    return user
                           