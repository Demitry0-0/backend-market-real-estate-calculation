import databases
from os import environ

environ["TESTING"] = "y"

# берем параметры БД из переменных окружения
DB_USER = environ.get("DB_USER", "postgres")
DB_PASSWORD = environ.get("DB_PASSWORD", "QWERTY")
DB_HOST = environ.get("DB_HOST", "localhost")
DB_NAME = environ.get("DB_HOST", "apartments-temp-for-test")

TEST_SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)
database = databases.Database(TEST_SQLALCHEMY_DATABASE_URL)

user_session = dict()
# key -> user_id
# value -> dict key -> count_rooms
#               value -> Parser
