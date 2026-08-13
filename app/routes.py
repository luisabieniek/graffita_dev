from flask import Blueprint, jsonify, render_template, request

import servicos

bp = Blueprint("api", __name__, url_prefix="/api")
paginas = Blueprint("paginas", __name__)


# ---------------------------------------------------------------- páginas --

@paginas.route("/")
def index():
    return render_template("index.html")


@paginas.route("/login")
def login_page():
    return render_template("login.html")


@paginas.route("/cadastro")
def cadastro_page():
    return render_template("cadastro.html")


@paginas.route("/postar")
def postar_page():
    return render_template("postar.html")


# --------------------------------------------------------------- produtos --

@bp.route("/produtos", methods=["GET"])
def api_listar_produtos():
    return jsonify(servicos.listar_produtos())


@bp.route("/produtos", methods=["POST"])
def api_cadastrar_produto():
    try:
        produto = servicos.cadastrar_produto(request.get_json(silent=True) or {})
        return jsonify(produto), 201
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400


# --------------------------------------------------------------- usuarios --

@bp.route("/usuarios", methods=["GET"])
def api_listar_usuarios():
    return jsonify(servicos.listar_usuarios())


@bp.route("/usuarios", methods=["POST"])
def api_cadastrar_usuario():
    try:
        usuario = servicos.cadastrar_usuario(request.get_json(silent=True) or {})
        return jsonify(usuario), 201
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400


@bp.route("/login", methods=["POST"])
def api_login():
    try:
        usuario = servicos.autenticar_usuario(request.get_json(silent=True) or {})
        return jsonify(usuario), 200
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 401


@bp.route("/recuperar-senha", methods=["POST"])
def api_recuperar_senha():
    try:
        usuario = servicos.recuperar_senha(request.get_json(silent=True) or {})
        return jsonify(usuario), 200
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400


# -------------------------------------------------------------- favoritos --

@bp.route("/favoritos", methods=["GET"])
def api_listar_favoritos():
    return jsonify(servicos.listar_favoritos())


@bp.route("/favoritos", methods=["POST"])
def api_cadastrar_favorito():
    try:
        favorito = servicos.cadastrar_favorito(request.get_json(silent=True) or {})
        return jsonify(favorito), 201
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400


# --------------------------------------------------------------- carrinho --

@bp.route("/carrinho", methods=["GET"])
def api_listar_carrinho():
    return jsonify(servicos.listar_carrinhos())


@bp.route("/carrinho", methods=["POST"])
def api_cadastrar_carrinho():
    try:
        item = servicos.cadastrar_carrinho(request.get_json(silent=True) or {})
        return jsonify(item), 201
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400


# -------------------------------------------------------------- endereços --

@bp.route("/enderecos", methods=["GET"])
def api_listar_enderecos():
    return jsonify(servicos.listar_endereco())


@bp.route("/enderecos", methods=["POST"])
def api_cadastrar_endereco():
    try:
        endereco = servicos.cadastrar_endereco(request.get_json(silent=True) or {})
        return jsonify(endereco), 201
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400


# -------------------------------------------------------------- mensagens --

@bp.route("/mensagens", methods=["GET"])
def api_listar_mensagens():
    return jsonify(servicos.listar_mensagens())


@bp.route("/mensagens", methods=["POST"])
def api_cadastrar_mensagem():
    try:
        mensagem = servicos.cadastrar_mensagem(request.get_json(silent=True) or {})
        return jsonify(mensagem), 201
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400