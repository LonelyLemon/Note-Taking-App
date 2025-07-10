import uuid

from sqlalchemy import Column, Text, String, Integer, UUID, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from ..database import Base


class Users(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default='user')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    notes = relationship("Notes", back_populates="owner")


class Notes(Base):
    __tablename__ = "notes"

    note_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    note_title = Column(String, nullable=False)
    note_content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("Users", back_populates="notes")