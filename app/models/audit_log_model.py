from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from datetime import datetime
from uuid import uuid4, UUID as UUIDType
import pytz

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id: Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), nullable=False)
    performed_by: Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(pytz.UTC))