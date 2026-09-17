from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL connection URL (შეცვალეთ თქვენი მონაცემებით)
# ფორმატი: postgresql://<username>:<password>@<host>:<port>/<database_name>
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Chigladze12@localhost:5432/movies_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency Database Session-ის მისაღებად
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()