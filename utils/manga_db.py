from sqlalchemy import func, create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

username = 'root'
password = ""
database_name = "crawl_beetoon"
port = 3306

urls = f'mysql+mysqlconnector://{username}:{password}@localhost:{port}/{database_name}'
engine = create_engine(urls)
#"mysql+pymysql://root:S%401989@localhost/colornote?charset=utf8"
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Manga(Base):
    __tablename__ = 'manga'
    id = Column(Integer, primary_key=True)
    domain_id = Column(Integer)
    manga_id = Column(Integer())
    manga_type = Column(String(255))
    manga_name = Column(String(255))
    authors = Column(String(255))
    categories = Column(String(255))
    slug = Column(String(255))
    status = Column(String(255))
    is_active = Column(Integer())
    image = Column(Text)
    chapter_count = Column(Integer())
    rank = Column(Integer())
    view = Column(Integer())
    description = Column(Text())
    release_at = Column(String(255))
    created_at = Column(String(255))
    updated_at = Column(String(255))
    deleted_at = Column(Integer())

class Authors(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer)
    name = Column(String(255))
    manga_by_author = Column(Text())
    created_at = Column(String(255))
    updated_at = Column(String(255))
    deleted_at = Column(String(255))

class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    domain_id = Column(Integer)
    category_id = Column(Integer)
    title = Column(String(255))
    slug = Column(String(255))
    is_active = Column(Integer)
    total_manga = Column(Text)
    description = Column(String(255))
    created_at = Column(Integer())
    updated_at = Column(Integer())
    deleted_at = Column(Integer())

class Chapters(Base):
    __tablename__ = 'chapters'
    id = Column(Integer, primary_key=True)
    manga_id = Column(Integer)
    manga_name = Column(String(255))
    chapter_id = Column(Integer)
    chapter_name = Column(String(255))
    is_active = Column(Integer)
    thumbnail_count = Column(String(255))
    created_at = Column(String(255))
    updated_at = Column(String(255))
    deleted_at = Column(String(255))

class Chapters_Detail(Base):
    __tablename__ = 'chapter_thumbnails'
    id = Column(Integer, primary_key=True)
    manga_id = Column(Integer)
    chapter_id = Column(Integer)
    chapter_name = Column(String(255))
    thumbnail_url = Column(Text)
    is_active = Column(Integer)
    created_at = Column(Integer())
    updated_at = Column(Integer())
    deleted_at = Column(Integer())

class User_Info(Base):
    __tablename__ = 'user_information'
    id = Column(Integer(), primary_key=True)
    username = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    phone_number = Column(String(255))
    avatar = Column(String(255))
    provider = Column(String(255))
    is_active = Column(Integer())
    created_at = Column(String(255))
    updated_at = Column(String(255))
    deleted_at = Column(String(255))
    last_login = Column(String(255))
    verified_at = Column(String(255))
    favorite_manga = Column(Text())

class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer(), primary_key=True)
    comment_id = Column(Integer())
    user_id = Column(Integer())
    manga_id = Column(Integer())
    parent_id = Column(Integer())
    content = Column(Text)
    updated_at = Column(String(255))
    created_at = Column(String(255))