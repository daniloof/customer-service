from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
import uuid
from datetime import datetime
from sqlalchemy.sql import func

Base = declarative_base()

class CustomerModel(Base):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    name = Column(String,nullable=False)
    email = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now())