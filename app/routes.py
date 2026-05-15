import flask as fk
from sqlalchemy.exc import IntegrityError

from servicos import (
    cadastrar_aluno,
    cadastrar_turma,
    listar_alunos,
    cadastrar_usuario, # Importa cadastrar_usuario
    listar_usuarios, # Importa listar_usuarios
    listar_turmas,
    cadastrar_produto,
    listar_produtos,
    cadastrar_tipoAnimal
)

bp = fk.Blueprint("api", __name__, url_prefix="/api")


def _erro(mensagem, status=400):
    return fk.jsonify({"erro": mensagem}), status


@bp.get("/professores")
def get_professores(): # Renomeado para clareza
    return fk.jsonify(listar_usuarios()) # Chama listar_usuarios do servicos.py


@bp.post("/professores")
def post_professores(): # Renomeado para clareza
    dados = fk.request.get_json(silent=True) or {}
    try:
        return fk.jsonify(cadastrar_usuario(dados)), 201 # Chama cadastrar_usuario do servicos.py
    except ValueError as exc:
        return _erro(str(exc))
    except IntegrityError:
        return _erro("Já existe um professor com este e-mail.", 409)


@bp.get("/turmas")
def turmas():
    return fk.jsonify(listar_turmas())


@bp.get("/produtos")
def produtos():
    return fk.jsonify(listar_produtos())

@bp.post("/produtos")
def criar_produtos():
    dados = fk.request.get_json(silent=True) or {}
    try:
        return fk.jsonify(cadastrar_produto(dados)), 201
    except ValueError as exc:
        return _erro(str(exc))
    except IntegrityError:
        return _erro("Erro de integridade ao cadastrar produto.", 409)


@bp.post("/turmas")
def criar_turma():
    dados = fk.request.get_json(silent=True) or {}
    try:
        return fk.jsonify(cadastrar_turma(dados)), 201
    except ValueError as exc:
        return _erro(str(exc))
    except IntegrityError:
        return _erro("Já existe uma turma com este código.", 409)

@bp.get("/alunos")
def alunos():
    return fk.jsonify(listar_alunos())


@bp.post("/alunos")
def criar_aluno():
    dados = fk.request.get_json(silent=True) or {}
    try:
        return fk.jsonify(cadastrar_aluno(dados)), 201
    except ValueError as exc:
        return _erro(str(exc))
    except IntegrityError as exc:
        orig = str(exc.orig) if getattr(exc, "orig", None) else str(exc)
        orig_l = orig.lower()
        if "unique" in orig_l and "email" in orig_l:
            return _erro("Já existe um aluno com este e-mail.", 409)
        return _erro(
            "Não foi possível cadastrar o aluno (restrição do banco de dados).",
            409,
        )
        
@bp.post("/tipoAnimais")
def criar_tipo_animais():
    dados = fk.request.get_json(silent=True) or {}
    try:
        return fk.jsonify(cadastrar_tipoAnimal(dados)), 201
    except ValueError as exc:
        return _erro(str(exc))
    except IntegrityError:
        return _erro("Erro ao cadastrar tipo de animal.", 409)

paginas = fk.Blueprint("paginas", __name__)


@paginas.get("/")
def home():
    return fk.render_template("index.html")
