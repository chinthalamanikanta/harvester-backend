from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = (
    "mysql+pymysql://maniadmin:admin%40123@"
    "mani-server-db.mysql.database.azure.com:3306/harvester_db"
)

# DATABASE_URL = (
#     "mysql+pymysql://root:Mani%40123@localhost:3306/harvester_db"
# )

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()