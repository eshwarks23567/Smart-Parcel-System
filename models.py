import os
import json
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data.db')
DATABASE_URL = f'sqlite:///{DB_PATH}'

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    phone = Column(String(50), nullable=True)
    face_uuid = Column(String(64), nullable=True, unique=True)
    embedding_json = Column(Text, nullable=False)
    photo_path = Column(String(400), nullable=True)


class Parcel(Base):
    __tablename__ = 'parcels'
    id = Column(Integer, primary_key=True)
    tracking_code = Column(String(200), nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    status = Column(String(50), default='stored')
    slot = Column(String(50), nullable=True)
    arrival_time = Column(DateTime, default=datetime.utcnow)
    collected_time = Column(DateTime, nullable=True)
    note = Column(Text, nullable=True)

    owner = relationship('User', backref='parcels')


class FaceSample(Base):
    __tablename__ = 'face_samples'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    face_uuid = Column(String(64), nullable=False)  # stable uuid per identity
    sample_uuid = Column(String(64), nullable=False)  # unique per synthetic sample
    image_path = Column(String(400), nullable=False)
    embedding_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', backref='samples')


def init_db():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)


def get_engine():
    return create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()
