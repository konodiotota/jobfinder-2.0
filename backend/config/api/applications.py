from flask import jsonify, request, session
from backend.config.app.app import app
from backend.config.app.engine import SessionLocal
from backend.models.shared.applications import Application
from backend.models.company.job import Jobs
import os
from werkzeug.utils import secure_filename

extensao_permitida = {'.pdf','.docx'}

def Arquivo_permitido(file_name):
    extensao = os.path.splitext(file_name)[1].lower()
    return extensao in extensao_permitida

@app.route('/api/applications/<int:candidate_id>', methods=['GET'])
def Minhas_Applications(candidate_id):
    sessao = SessionLocal()
    if 'user_id' not in session:
        return {'erro':'Usuario não autenticado'},401
    
    try:
        application = sessao.query(Application).filter_by(candidate_id=candidate_id).all()
        if not application:
            return {"erro":"Nada encontrado"},200

        resultado = []
        for a in application:
            resultado.append({
                'Nome vaga': a.job.name_job,
                'Nome candidato': a.candidate.name,
                'status': a.status
            })
        return jsonify(resultado)
    except Exception as e:
        sessao.rollback()
        print(f'deu erro aqui em applications GET: {e}')
        return {'erro': 'Ocorreu um erro interno'}, 500
    finally:
        sessao.close()

@app.route('/api/applications/<int:job_id>', methods=['POST'])
def Iniciar_Candidatura(job_id):
    sessao = SessionLocal()
    if 'user_id' not in session:
        return {'erro':'Usuario não autenticado'}, 401
    
    job = sessao.query(Jobs).filter_by(id=job_id).first()
    if not job:
        return {'erro':'Nenhuma vaga encontrada'},200

    try:
        cv = request.files.get('cv')
        if not cv:
            return {'erro':'Curriculo é obrigatório'},400
        
        if not Arquivo_permitido(cv.filename):
            return {'erro':'tipo de arquivo nao permitido'},400

        nome = secure_filename(cv.filename)
        UPLOAD_FOLDER = 'uploads/curriculos'
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        cv.save(os.path.join(UPLOAD_FOLDER, nome))

        existe = (
            sessao.query(Application).filter_by(candidate_id=session['user_id'], job_id=job_id).first()
            )

        if existe:
            return {'erro':'Voce já se candidatou a essa vaga'},409

        application = Application(
            candidate_id=session['user_id'],
            job_id= job.id,
            cv= nome
        )
        sessao.add(application)
        sessao.commit()
        return {'sucess':'Candidatura criado com sucesso'},201

    except Exception as e:
        sessao.rollback()
        print(f'erro api applications post: {e}')
        return {'erro':'Erro interno'},500

    finally:
        sessao.close()