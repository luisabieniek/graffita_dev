import flask as fk
from sqlalchemy.exc import IntegrityError

from servicos import (
    cadastrar_usuario,
    listar_usuarios,
    cadastrar_produto,
    listar_produtos,
    cadastrar_favorito,
    listar_favoritos,
    cadastrar_endereco,
    listar_endereco,
    cadastrar_carrinho,
    listar_carrinhos,
    cadastrar_inspiracao,
    listar_inspiracoes,
    listar_pedidos
)

bp = fk.Blueprint("api", __name__, url_prefix="/api")


def _erro(mensagem, status=400):
    return fk.jsonify({"erro": mensagem}), status


@bp.get("/usuarios")
def get_usuarios():
    return fk.jsonify(listar_usuarios())


@bp.post("/usuarios")
def post_usuarios():
    dados = fk.request.get_json(silent=True) or {}
    try:
        return fk.jsonify(cadastrar_usuario(dados)), 201
    except ValueError as exc:
        return _erro(str(exc))
    except IntegrityError:
        return _erro("Já existe um usuário com este e-mail ou CPF.", 409)


@bp.get("/produtos")
def produtos():
    return fk.jsonify(listar_produtos())

@bp.post("/produtos")
def criar_produtos():
    if fk.request.files:
        dados = fk.request.form.to_dict()
        arquivo = fk.request.files.get("imagem")
    else:
        dados = fk.request.get_json(silent=True) or {}
        arquivo = None

    try:
        return fk.jsonify(cadastrar_produto(dados, arquivo)), 201
    except ValueError as exc:
        return _erro(str(exc))
    except IntegrityError:
        return _erro("Erro de integridade ao cadastrar produto.", 409)

@bp.get("/favoritos")
def favoritos():
    return fk.jsonify(listar_favoritos())

@bp.post("/favoritos")
def criar_favorito():
    dados = fk.request.get_json(silent=True) or {}
    try:
        return fk.jsonify(cadastrar_favorito(dados)), 201
    except ValueError as exc:
        return _erro(str(exc))

@bp.get("/enderecos")
def enderecos():
    return fk.jsonify(listar_endereco())

@bp.post("/enderecos")
def criar_endereco():
    dados = fk.request.get_json(silent=True) or {}
    try:
        return fk.jsonify(cadastrar_endereco(dados)), 201
    except ValueError as exc:
        return _erro(str(exc))
        
@bp.get("/carrinhos")
def carrinhos():
    return fk.jsonify(listar_carrinhos())

@bp.post("/carrinhos")
def criar_carrinho():
    dados = fk.request.get_json(silent=True) or {}
    try:
        return fk.jsonify(cadastrar_carrinho(dados)), 201
    except ValueError as exc:
        return _erro(str(exc))

@bp.get("/inspiracoes")
def inspiracoes():
    return fk.jsonify(listar_inspiracoes())

@bp.post("/inspiracoes")
def criar_inspiracao():
    if fk.request.files:
        dados = fk.request.form.to_dict()
        arquivo = fk.request.files.get("imagem")
    else:
        dados = fk.request.get_json(silent=True) or {}
        arquivo = None

    try:
        return fk.jsonify(cadastrar_inspiracao(dados, arquivo)), 201
    except ValueError as exc:
        return _erro(str(exc))
    except IntegrityError:
        return _erro("Erro de integridade ao cadastrar inspiração.", 409)

@bp.get("/pedidos")
def get_pedidos():
    return fk.jsonify(listar_pedidos())



paginas = fk.Blueprint("paginas", __name__)


@paginas.get("/")
def home():
    return fk.render_template("index.html")
