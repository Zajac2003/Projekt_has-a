from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Md5Hash(Base):
    __tablename__ = "md5_hashes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hash_value = Column(String(32), unique=True, nullable=False, index=True)
    password_raw = Column(String(255), nullable=True)
    czas_lamania = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Sha1Hash(Base):
    __tablename__ = "sha1_hashes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hash_value = Column(String(40), unique=True, nullable=False, index=True)
    password_raw = Column(String(255), nullable=True)
    czas_lamania = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Sha256Hash(Base):
    __tablename__ = "sha256_hashes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hash_value = Column(String(64), unique=True, nullable=False, index=True)
    password_raw = Column(String(255), nullable=True)
    czas_lamania = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class BcryptHash(Base):
    __tablename__ = "bcrypt_hashes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hash_value = Column(String(255), unique=True, nullable=False, index=True)
    password_raw = Column(String(255), nullable=True)
    czas_lamania = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
