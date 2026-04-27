from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
import uuid
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class AddressModel(Base):
    __tablename__ = "addresses"
    
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True),ForeignKey("customers.id"),nullable=False)
    street = Column(String,nullable=False)
    city = Column(String,nullable=False)
    state = Column(String,nullable=False)
    zip_code = Column(String,nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now())

    customer = relationship("CustomerModel",back_populates="addresses")

    
class CustomerModel(Base):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    name = Column(String,nullable=False)
    email = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now())

    addresses = relationship("AddressModel",back_populates="customer", cascade="all, delete-orphan")