from sqlalchemy import Column, String, DateTime, Boolean, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from datetime import datetime
from uuid import uuid4, UUID as UUIDType
from app.models.user_role import UserRole
from app.core.security import hash_password
import pytz

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    nickname: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    bio: Mapped[str] = mapped_column(String(255), nullable=True)
    profile_picture_url: Mapped[str] = mapped_column(String(255), nullable=True)
    github_profile_url: Mapped[str] = mapped_column(String(255), nullable=True)
    linkedin_profile_url: Mapped[str] = mapped_column(String(255), nullable=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.PENDING, nullable=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_professional: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    failed_login_attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_login_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    verification_token: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(pytz.UTC))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(pytz.UTC), onupdate=lambda: datetime.now(pytz.UTC))

    def update_professional_status(self, is_professional: bool) -> None:
        """Update the user's professional status."""
        self.is_professional = is_professional
        self.updated_at = datetime.now(pytz.UTC)
    
    def lock_account(self) -> None:
        """Lock the user account due to too many failed login attempts."""
        self.is_locked = True
        self.updated_at = datetime.now(pytz.UTC)
    
    def increment_failed_login_attempts(self) -> None:
        """Increment the failed login attempts counter."""
        self.failed_login_attempts += 1
        self.updated_at = datetime.now(pytz.UTC)
    
    def reset_failed_login_attempts(self) -> None:
        """Reset the failed login attempts counter."""
        self.failed_login_attempts = 0
        self.updated_at = datetime.now(pytz.UTC)
    
    def update_last_login(self) -> None:
        """Update the last login timestamp."""
        self.last_login_at = datetime.now(pytz.UTC)
        self.updated_at = datetime.now(pytz.UTC)
    
    def verify_email(self) -> None:
        """Mark the user's email as verified."""
        self.email_verified = True
        self.role = UserRole.AUTHENTICATED
        self.verification_token = None
        self.updated_at = datetime.now(pytz.UTC)