from backend.config.app.engine import base, SessionLocal
from sqlalchemy import String, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

sessao= SessionLocal()

class Application(base):
    __tablename__ = 'applications'
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)

    candidate_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    candidate = relationship('Users', back_populates='candidate')
    job_id = mapped_column(ForeignKey('job.id', ondelete='CASCADE'))

    job = relationship('Jobs', back_populates='application')
    
    cv: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default='Pendente')

    @staticmethod
    def Create_Application(candidate_id, cv, status):
        try:
            new_application = Application(candidate_id=candidate_id, cv=cv, status=status)
            sessao.add(new_application)
        except Exception as e:
            sessao.rollback()
            print(f'aconteceu algo aqui em application: {e}')
        finally:
            sessao.close()