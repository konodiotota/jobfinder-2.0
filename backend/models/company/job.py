from backend.config.app.engine import base, SessionLocal
from sqlalchemy import String, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

sessao = SessionLocal()

class Jobs(base):
    __tablename__ = 'job'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)

    company_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    company = relationship('Users', back_populates='company_job')
    application = relationship('Application', back_populates='job')

    name_job: Mapped[str] = mapped_column(String(200), nullable=False)
    quantity_oppening: Mapped[int] = mapped_column(Integer, nullable=False)
    salary: Mapped[float] = mapped_column(Numeric(10,2), nullable=True)
    working_hrs: Mapped[str] = mapped_column(String(21), nullable=False)
    responsability: Mapped[str] = mapped_column(String(2500), nullable=True)
    requirements: Mapped[str] = mapped_column(String(2500), nullable=True)
    addtional_info: Mapped[str] = mapped_column(String(2500), nullable=True)