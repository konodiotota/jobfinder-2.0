from backend.config.app.engine import base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Application(base):
    __tablename__ = 'applications'
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)

    candidate_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    job_id = mapped_column(ForeignKey('job.id', ondelete='CASCADE'))
    cv: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=True, default='Pendente')

    job = relationship('Jobs', back_populates='application')
    candidate = relationship('Users', back_populates='candidate')
