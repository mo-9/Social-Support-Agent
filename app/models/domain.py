import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    emirates_id = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    applications = relationship("Application", back_populates="user")

class Application(Base):
    __tablename__ = "applications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    status = Column(String, default="PENDING")
    total_income = Column(Float, nullable=True)
    family_size = Column(Integer, nullable=True)
    eligibility_score = Column(Float, nullable=True)
    final_decision = Column(String, nullable=True)
    ai_analysis_data = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = relationship("User", back_populates="applications")
    documents = relationship("Document", back_populates="application")

class Document(Base):
    __tablename__ = "documents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey("applications.id"))
    file_type = Column(String)
    file_path = Column(String, nullable=False)
    is_processed = Column(Boolean, default=False)
    vector_id = Column(String, nullable=True)
    application = relationship("Application", back_populates="documents")
