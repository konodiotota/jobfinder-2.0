from flask import jsonify, request, session
from backend.config.app.app import app
from backend.config.app.engine import SessionLocal
import bcrypt
from backend.models.shared.register import Users

@app.route('/api/oauth/register', methods= ['POST'])
def Register():
    sessao=SessionLocal()
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        password_hash = bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt()).decode("utf-8")

        usuario = sessao.query(Users).filter_by(email=email).first()

        if not name or not email or not password:
            return {"error":"Nome, Email e Senha são obrigatorios"}

        if usuario:
            return jsonify({"error": "Email ja cadastrado"}), 404
        
        new_user = Users(name=name, email=email, password_hash=password_hash, role=role)
        sessao.add(new_user)
        sessao.commit()
        session['user_id'] = new_user.id
        session['user_role'] = new_user.role
        return jsonify({"message": "Usuário criado com sucesso","id": new_user.id}), 201

    except Exception as e:
        sessao.rollback()
        print(f'deu erro aqui na api oauth {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        sessao.close()

#if (response.ok) {
#   window.location.href = "/dashboard"
#   }

@app.route('/api/oauth/login', methods=['POST'])
def Login():
    sessao=SessionLocal()
    try:
        email=request.form.get('email')
        senha=request.form.get('password')
        email_existente = sessao.query(Users).filter_by(email=email).first()

        if not email_existente:
            return{"error":"Email ou senha invalido"},400
        
        if not senha or not email:
            return {"error":"email e senha são obrigatorios"},400

        if bcrypt.checkpw(senha.encode("utf-8"), email_existente.password_hash.encode("utf-8")):
            session['user_id'] = email_existente.id
            return {"sucess":"Login OK"}, 200
        else:
            return {"Error":"Email ou senha invalido"},401

    except Exception as e:
        print(f'deu errado aqui {e}')
