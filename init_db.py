from sqlalchemy import create_engine

from models import Base


DB_PATH = "hashes.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"


def init_db() -> None:
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print(f"Database initialized: {DB_PATH}")


if __name__ == "__main__":
    init_db()
