"""
This Python file is part of a FastAPI application, demonstrating user management functionalities including creating, reading,
updating, and deleting (CRUD) user information. It uses OAuth2 with Password Flow for security, ensuring that only authenticated
users can perform certain operations. Additionally, the file showcases the integration of FastAPI with SQLAlchemy for asynchronous
database operations, enhancing performance by non-blocking database calls.

The implementation emphasizes RESTful API principles, with endpoints for each CRUD operation and the use of HTTP status codes
and exceptions to communicate the outcome of operations. It introduces the concept of HATEOAS (Hypermedia as the Engine of
Application State) by including navigational links in API responses, allowing clients to discover other related operations dynamically.

OAuth2PasswordBearer is employed to extract the token from the Authorization header and verify the user's identity, providing a layer
of security to the operations that manipulate user data.

Key Highlights:
- Use of FastAPI's Dependency Injection system to manage database sessions and user authentication.
- Demonstrates how to perform CRUD operations in an asynchronous manner using SQLAlchemy with FastAPI.
- Implements HATEOAS by generating dynamic links for user-related actions, enhancing API discoverability.
- Utilizes OAuth2PasswordBearer for securing API endpoints, requiring valid access tokens for operations.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import timedelta
import logging

from app.database import get_db
from app.schemas.user_schemas import UserCreate, UserResponse, UserUpdate, TokenResponse
from app.services.user_service import UserService
from app.services.email_service import EmailService
from app.dependencies import get_current_user, require_role, get_email_service
from app.core.security import create_access_token
from app.core.config import settings
from app.utils.links import create_user_links
from app.models.user_model import UserRole
from app.models.audit_log_model import AuditLog

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/signup", response_model=UserResponse, tags=["Authentication"])
async def signup_user(
    user_data: UserCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    email_service: EmailService = Depends(get_email_service)
):
    user = await UserService.create_user(db, user_data)
    await email_service.send_registration_email(user.email, user.first_name)
    return UserResponse.model_construct(
        **user.dict(),
        links=create_user_links(user.id, request)
    )


@router.post("/login", response_model=TokenResponse, tags=["Authentication"])
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await UserService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)

    return TokenResponse(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse, tags=["User Profile"])
async def get_profile(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    return UserResponse.model_construct(
        **current_user,
        links=create_user_links(UUID(current_user["id"]), request)
    )


@router.put("/me", response_model=UserResponse, tags=["User Profile"])
async def update_profile(
    updated_data: UserUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    updated_user = await UserService.update_user(db, UUID(current_user["id"]), updated_data)
    return UserResponse.model_construct(
        **updated_user.dict(),
        links=create_user_links(updated_user.id, request)
    )


@router.put("/users/{user_id}/role", response_model=UserResponse, tags=["User Management Requires (Admin Role)"])
async def change_user_role(
    user_id: UUID,
    new_role: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(require_role(["ADMIN"]))
):
    """
    Change a user's role.
    Only admins can perform this action.
    Logs the action in the audit_logs table.
    """
    if new_role not in [role.value for role in UserRole]:
        raise HTTPException(status_code=400, detail="Invalid role")

    user = await UserService.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = UserRole[new_role]

    audit_log = AuditLog(
        action=f"Changed role to {new_role}",
        user_id=user_id,
        performed_by=UUID(current_user["id"])
    )
    db.add(user)
    db.add(audit_log)
    await db.commit()

    return UserResponse.model_construct(
        id=user.id,
        nickname=user.nickname,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        bio=user.bio,
        profile_picture_url=user.profile_picture_url,
        linkedin_profile_url=user.linkedin_profile_url,
        github_profile_url=user.github_profile_url,
        role=user.role,
        is_professional=user.is_professional,
        last_login_at=user.last_login_at,
        created_at=user.created_at,
        updated_at=user.updated_at,
        links=create_user_links(user.id, request)
    )
