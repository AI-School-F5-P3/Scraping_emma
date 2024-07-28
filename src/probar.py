import logging
import pytest
from src.database import Database
from src.models import Quote, Author

@pytest.fixture
def database():
    logger = logging.getLogger(__name__)
    db = Database(database=':memory:')
    assert not db.is_mysql, "Test database should be SQLite, not MySQL"
    db.create_tables()
    yield db
    db.close()
    logger.info("Test database closed")

# ... (resto de los tests con logging similar)