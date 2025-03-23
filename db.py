# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# DATABASE_URL = "postgresql+asyncpg://postgres:Sangeeta123@localhost/documentdb"

# engine = create_async_engine(DATABASE_URL, echo=True)
# AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# async def get_db():
#     async with AsyncSessionLocal() as session:
#         yield session
# print("Database script executed successfully!")


from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
DATABASE_URL = "postgresql+asyncpg://postgres:Sangeeta%40123@localhost/documentdb"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

print("Database script executed successfully!")
