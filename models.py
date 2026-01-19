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
    face_uuid = Column(String(64), nullable=True, unique=True, index=True)  # Index for fast lookups
    embedding_json = Column(Text, nullable=False)
    photo_path = Column(String(400), nullable=True)


class Parcel(Base):
    __tablename__ = 'parcels'
    id = Column(Integer, primary_key=True)
    tracking_code = Column(String(200), nullable=True, index=True)  # Index for tracking search
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=True, index=True)  # Index for user parcels
    status = Column(String(50), default='stored', index=True)  # Index for filtering by status
    slot = Column(String(50), nullable=True)
    storage_location = Column(String(100), nullable=True)  # e.g., "Shelf A-3", "Locker 12"
    estimated_delivery_days = Column(Integer, nullable=True)  # days until pickup/delivery
    arrival_time = Column(DateTime, default=datetime.utcnow, index=True)  # Index for sorting by date
    collected_time = Column(DateTime, nullable=True)
    note = Column(Text, nullable=True)

    owner = relationship('User', backref='parcels')


class FaceSample(Base):
    __tablename__ = 'face_samples'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    face_uuid = Column(String(64), nullable=False, index=True)  # Index for UUID lookups
    sample_uuid = Column(String(64), nullable=False)  # unique per synthetic sample
    image_path = Column(String(400), nullable=False)
    embedding_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', backref='samples')


class TrackingVariation(Base):
    __tablename__ = 'tracking_variations'
    id = Column(Integer, primary_key=True)
    parcel_id = Column(Integer, ForeignKey('parcels.id'), nullable=False)
    original_code = Column(String(200), nullable=False)
    variation_code = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    parcel = relationship('Parcel', backref='tracking_variations')


def init_db():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)


def get_engine():
    return create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_size=10,  # Connection pool size
        max_overflow=20,  # Maximum overflow connections
        pool_pre_ping=True,  # Verify connections before using
        pool_recycle=3600  # Recycle connections after 1 hour
    )


def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()
