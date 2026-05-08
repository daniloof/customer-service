import pytest
from tests.test_database import engine
from src.adapters.outbound.db.models import Base

@pytest.fixture(scope="function", autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)