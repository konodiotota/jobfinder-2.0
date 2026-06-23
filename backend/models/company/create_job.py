from config.app.engine import base, sessao
from sqlalchemy import String, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Jobs(base):
    __tablename__ = 'create_job'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)

    company_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    company = relationship('Users', back_populates='company_job')

    name_job: Mapped[str] = mapped_column(String(200), nullable=False)
    quantity_oppening: Mapped[int] = mapped_column(Integer, nullable=False)
    salary: Mapped[float] = mapped_column(Numeric(10,2), nullable=True)
    working_hrs: Mapped[str] = mapped_column(String(21), nullable=False)
    responsability: Mapped[str] = mapped_column(String(2500), nullable=True)
    requirements: Mapped[str] = mapped_column(String(2500), nullable=True)
    addional_info: Mapped[str] = mapped_column(String(2500), nullable=True)

    @staticmethod
    def Create_job_Company(company_id, name_job, quantity_oppening, salary, working_hrs, responsability, requirements, addional_info):
        try:
            new_job = Jobs(
                company_id=company_id,
                name_job=name_job, 
                quantity_oppening=quantity_oppening, 
                salary=salary, 
                working_hrs=working_hrs, 
                responsability=responsability, 
                requirements=requirements, 
                addional_info=addional_info
            )
            sessao.add(new_job)
            sessao.commit()
        except Exception as e:
            sessao.rollback()
            print(f'deu erro aqui em new_job: {e}')
        finally:
            sessao.close()