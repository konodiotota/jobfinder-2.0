from config.app.engine import base, sessao
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
    candidate = relationship('Application', back_populates='_candidate')

    @staticmethod
    def Create_User(name,email,password, role):
        try:
            password_hash = bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt()).decode("utf-8")
            new_user = Users(name=name, email=email,password_hash=password_hash,role=role)
            sessao.add(new_user)
            sessao.commit()
        except Exception as e:
            sessao.rollback()
            print(f'Algo aconteceu na create_user: {e}')
        finally:
            sessao.close()