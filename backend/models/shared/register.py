from backend.config.app.engine import base, SessionLocal
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
import bcrypt


class Users(base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(70), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)

    company_job = relationship('Jobs', back_populates='company')
    candidate = relationship('Application', back_populates='candidate')
