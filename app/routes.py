import os
import uuid
import flask as fk
from sqlalchemy.exc import IntegrityError, OperationalError

from servicos import (
    autenticar_usuario,
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
    cadastrar_mensagem,
    listar_mensagens,
    validar_cpf
)

bp = fk.Blueprint("api", __name__, url_prefix="/api")


def _obter_dados():
    """Extrai dados de JSON, Formulários (FormData) ou Query Params."""
    dados = {}
    # Pega dados de formulários (multipart/form-data ou x-www-form-urlencoded)
    if fk.request.form:
        dados.update(fk.request.form.to_dict())
    # Se for JSON, combina com o que já tem
    if fk.request.is_json:
        dados.update(fk.request.get_json(silent=True) or {})
    return dados

def _erro(mensagem, status=400):
    return fk.jsonify({"erro": mensagem}), status

@bp.get("/usuarios")
def get_usuarios():
    return fk.jsonify(listar_usuarios())


@bp.post("/usuarios")
def post_usuarios():
    dados = _obter_dados()
    try:
        return fk.jsonify(cadastrar_usuario(dados)), 201
    except ValueError as exc:
        return _erro(str(exc))
    except IntegrityError:
        return _erro("Já existe um usuário com este e-mail ou CPF.", 409)
    except OperationalError:
        return _erro("Não foi possível salvar o usuário no momento. Tente novamente.", 500)


@bp.post("/login")
def login_usuario():
    dados = _obter_dados()
    try:
        usuario = autenticar_usuario(dados)
        fk.session["usuario_id"] = usuario["id"]
        fk.session["usuario_nome"] = usuario["nome"]
        fk.session["usuario_email"] = usuario["email"]
        return fk.jsonify({"ok": True, "usuario": usuario}), 200
    except ValueError as exc:
        return _erro(str(exc), 401)
    except OperationalError:
        return _erro("Não foi possível autenticar o usuário no momento.", 500)


@bp.post("/logout")
def logout_usuario():
    fk.session.clear()
    return fk.jsonify({"ok": True}), 200


@bp.get("/produtos")
def produtos():
    return fk.jsonify(listar_produtos())

@bp.post("/produtos")
def criar_produtos():
    dados = _obter_dados()
    
    # Tratamento da Foto vinda da Galeria
    if "imagem" in fk.request.files:
        arquivo = fk.request.files["imagem"]
        if arquivo and arquivo.filename != "":
            # Garante que a pasta de uploads existe
            pasta_uploads = os.path.join("app", "static", "uploads")
            os.makedirs(pasta_uploads, exist_ok=True)
            
            # Gera um nome único para o arquivo
            extensao = os.path.splitext(arquivo.filename)[1]
            nome_unico = f"{uuid.uuid4()}{extensao}"
            
            arquivo.save(os.path.join(pasta_uploads, nome_unico))
            dados["imagem"] = f"/static/uploads/{nome_unico}"

    try:
        return fk.jsonify(cadastrar_produto(dados)), 201
    except ValueError as exc:
        return _erro(str(exc))
    except IntegrityError:
        return _erro("Erro de integridade ao cadastrar produto.", 409)

@bp.get("/favoritos")
def favoritos():
    return fk.jsonify(listar_favoritos())

@bp.post("/favoritos")
def criar_favorito():
    dados = _obter_dados()
    try:
        return fk.jsonify(cadastrar_favorito(dados)), 201
    except ValueError as exc:
        return _erro(str(exc))

@bp.get("/enderecos")
def enderecos():
    return fk.jsonify(listar_endereco())

@bp.post("/enderecos")
def criar_endereco():
    dados = _obter_dados()
    try:
        return fk.jsonify(cadastrar_endereco(dados)), 201
    except ValueError as exc:
        return _erro(str(exc))
        
@bp.get("/carrinhos")
def carrinhos():
    return fk.jsonify(listar_carrinhos())

@bp.post("/carrinhos")
def criar_carrinho():
    dados = _obter_dados()
    try:
        return fk.jsonify(cadastrar_carrinho(dados)), 201
    except ValueError as exc:
        return _erro(str(exc))

@bp.get("/mensagens")
def mensagens():
    return fk.jsonify(listar_mensagens())

@bp.post("/mensagens")
def criar_mensagem():
    dados = _obter_dados()
    try:
        return fk.jsonify(cadastrar_mensagem(dados)), 201
    except ValueError as exc:
        return _erro(str(exc))



paginas = fk.Blueprint("paginas", __name__)


@paginas.get("/")
def home():
    usuario = None
    if fk.session.get("usuario_id"):
        usuario = {
            "id": fk.session.get("usuario_id"),
            "nome": fk.session.get("usuario_nome"),
            "email": fk.session.get("usuario_email"),
        }
    return fk.render_template("home.html", usuario=usuario)


@paginas.get("/login")
def login_page():
    if fk.session.get("usuario_id"):
        return fk.redirect(fk.url_for("paginas.home"))
    return fk.render_template("login.html")


@paginas.get("/cadastro")
def cadastro_usuario():
    if fk.session.get("usuario_id"):
        return fk.redirect(fk.url_for("paginas.home"))
    return fk.render_template("cadastro_usuario.html")


@paginas.get("/logout")
def logout_page():
    fk.session.clear()
    return fk.redirect(fk.url_for("paginas.cadastro_usuario"))
