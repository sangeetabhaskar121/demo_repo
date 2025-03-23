# from sqlalchemy import Column, Integer, String, LargeBinary
# # from demo_project.db import Base  # Use 'db' instead of 'database'
# from db import Base

# # from .db import Base

# class Document(Base):
#     __tablename__ = "documents"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     content = Column(String)
#     embedding = Column(LargeBinary)

from sqlalchemy import Column, Integer, String, Text
from db import Base  # Fixed incorrect import

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    content = Column(Text)  # Use Text instead of String for larger document content
    embedding = Column(String)  # Store embedding as JSON string

