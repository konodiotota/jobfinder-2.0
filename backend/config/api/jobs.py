from flask import jsonify, request, session
from backend.config.app.app import app
from backend.config.app.engine import SessionLocal
from backend.models.company.job import Jobs
from backend.models.shared.applications import Application

@app.route('/api/jobs/', methods=['POST'])
def Create_job():
    sessao= SessionLocal()
    if "user_id" not in session:
        return {"erro": "Usuario não autenticado"},401

    if session.get("user_role") != 'company':
        print(session.get('user_role'))
        return {"erro": "Usuario não é empresa"},400
    
    dados=request.form
    try:
        nova_vaga = Jobs(
            company_id=session['user_id'],
            name_job=dados['name_job'],
            quantity_oppening=dados['quantity_oppening'], 
            salary=dados['salary'], 
            working_hrs= dados['working_hrs'], 
            responsability= dados['responsability'], 
            requirements= dados['requirements'], 
            addtional_info= dados['addtional_info']
            )
        sessao.add(nova_vaga)
        sessao.commit()
        if not nova_vaga:
            return {"error":"Necessario preencher as informacoes"},401
        return {"sucess": "Vaga criado com sucesso"},200

    except Exception as e:
        print(f'deu erro aqui em jobs post: {e}')
        sessao.rollback()
        return {"erro":"erro desconhecido"},404
    finally:
        sessao.close()


@app.route('/api/jobs/', methods=['GET'])
def All_Jobs():
    if "user_id" not in session:
        return {"Erro":"Usuario não autenticado"},401
    try:
        sessao=SessionLocal()
        jobs = sessao.query(Jobs).all()
        resultado = []
        if not jobs:
            return {"erro":"Sem vagas criadas"}, 200
        for job in jobs:
            resultado.append({
                "id": job.id,
                "company_id": job.company_id,
                "name_job": job.name_job,
                "quantity_oppening": job.quantity_oppening,
                "salary": float(job.salary),
                "working_hrs": job.working_hrs,
                "responsability": job.responsability,
                "requirements": job.requirements,
                "addtional_info": job.addtional_info
            })
        return jsonify(resultado)
    except Exception as e:
        sessao.rollback()
        print(f'algo aconteceu aqui na api jobs get: {e}')
        return {"erro":"Ocorreu um erro interno"},400
    finally:
        sessao.close()

@app.route('/api/jobs/<int:job_id>',methods=['PUT'])
def Edit_vaga(job_id):
    try:
        sessao= SessionLocal()
        if "user_id" not in session:
            return {"erro":"Usuario não autenticado"}, 401
        if session['user_role'] != "company":
            return {"erro":"Usuario não é empresa"},400
        job = sessao.query(Jobs).filter_by(id=job_id).first()

        if not job:
            return {"erro":"nenhuma vaga encontrada"},200
        if job.company_id != session['user_id']:
            return {"erro":"Voce não pode editar esta vaga"},403
        
        dados=request.form

        job.name_job= dados.get("name_job", job.name_job)
        job.quantity_oppening = dados.get("quantity_oppening", job.quantity_oppening)
        job.salary = dados.get("salary", job.salary)
        job.working_hrs = dados.get("working_hrs", job.working_hrs)
        job.responsability = dados.get("responsability", job.responsability)
        job.requirements = dados.get("requirements", job.requirements)
        job.addtional_info = dados.get("addtional_info", job.addtional_info)

        sessao.commit()
        return {"sucess":"Vaga modificada com sucesso"}
    except Exception as e:
        sessao.rollback()
        print(f'deu erro aqui na api jobs put: {e}')
        return {"erro":"Ocorreu um erro interno"},400
    finally:
        sessao.close()

@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def Delete_job(job_id):
    sessao= SessionLocal()
    if "user_id" not in session:
        return {"erro":"Usuario não Autenticado"}, 401
    if session['user_role'] != "company":
        return {"erro":"Usuario não é empresa"}, 400
    try:
        job = sessao.query(Jobs).filter_by(id=job_id).first()
        if not job:
            return {"erro":"Nenhuma vaga encontrada"}, 200

        if job.company_id != session['user_id']:
            return {"erro":"Voce não pode editar essa vaga"}, 403

        sessao.delete(job)
        sessao.commit()
        return {"sucesso":"Sucesso ao deletar a vaga"}, 200

    except Exception as e:
        sessao.rollback()
        print(f'deu erro na api jobs delete: {e}')
        return {"erro":"Ocorreu um erro interno"},400

    finally:
        sessao.close()

@app.route('/api/jobs/company_application/<int:job_id>/<int:candidate_id>', methods=['GET'])
def Application_job(job_id, candidate_id):
    sessao= SessionLocal()

    if 'user_id' not in session:
        return {'erro':'Usuario nao autenticado'},401
    if session['user_role'] != 'company':
        return {'erro':'Usuario nao e empresa'},400
    
    user= sessao.query(Application).filter_by(job_id=job_id, candidate_id=candidate_id).first()
    if not user:
        return {'erro':'Nenhuma vaga encontrada'},200

    return jsonify(user)

@app.route('/api/jobs/company_applications/<int:job_id>', methods=['GET'])
def Applications_job(job_id):
    sessao=SessionLocal()

    if 'user_id' not in session:
        return {'erro':'Usuario nao autenticado'},401
    if session['user_role'] != 'company':
        return {'erro':'Usuario nao e empresa'},400

    try:
        applications= sessao.query(Application).filter_by(job_id=job_id).all()

        if not applications:
            return {'erro':'Sem candidaturas'},200

        resultado = []
        for application in applications:
            resultado.append({
                'nome candidato' : application.candidate.name,
                'nome vaga': application.job.name,
                'curriculo candidato': application.cv
            })
        return jsonify(resultado)

    except Exception as e:
        sessao.rollback()
        print(f'deu erro aqui na api job applications get {e}')
        return {'erro':'Ocorreu um erro interno'}, 404
    
    finally:
        sessao.close()