"""
Regras de negócio e acesso ao banco (sessão + consultas).
Nas rotas só chamamos estas funções e devolvemos JSON — fica mais fácil de explicar.
"""

from datetime import datetime

from sqlalchemy import select

from database import SessionLocal
from models import Produto, Usuario, Favorito, Carrinho, Endereco, Mensagem



def listar_usuarios():
    session = SessionLocal()
    try:
        linhas = session.scalars(select(Usuario).order_by(Usuario.nome)).all()
        return [u.to_dict() for u in linhas]
    finally:
        session.close()

def listar_produtos():
    session = SessionLocal()
    try:
        linhas = session.scalars(select(Produto).order_by(Produto.nomeProduto)).all()
        return [p.to_dict() for p in linhas]
    finally:
        session.close()

def listar_favoritos():
    session = SessionLocal()
    try:
        linhas = session.scalars(select(Favorito).order_by(Favorito.id)).all()
        return [f.to_dict() for f in linhas]
    finally:
        session.close()
        
def listar_endereco():
    session = SessionLocal()
    try:
        linhas = session.scalars(select(Endereco).order_by(Endereco.id)).all()
        return [e.to_dict() for e in linhas]
    finally:
        session.close()
        
def listar_carrinhos():
    session = SessionLocal()
    try:
        linhas = session.scalars(select(Carrinho).order_by(Carrinho.id)).all()
        return [c.to_dict() for c in linhas]
    finally:
        session.close()

def listar_mensagens():
    session = SessionLocal()
    try:
        linhas = session.scalars(select(Mensagem).order_by(Mensagem.id)).all()
        return [m.to_dict() for m in linhas]
    finally:
        session.close()

def _texto_obrigatorio(valor, campo):
    if valor is None or str(valor).strip() == "":
        raise ValueError(f"O campo '{campo}' é obrigatório.")
    return str(valor).strip()


def _texto_opcional(valor):
    if valor is None:
        return None
    texto = str(valor).strip()
    return texto or None


def cadastrar_usuario(dados):
    nome = _texto_obrigatorio(dados.get("nome"), "nome")
    email = _texto_opcional(dados.get("email"))
    senha = _texto_obrigatorio(dados.get("senha"), "senha")
    cpf = _texto_obrigatorio(dados.get("cpf"), "cpf")

    session = SessionLocal()
    try:
        usuario = Usuario(nome=nome, email=email, senha=senha, cpf=cpf)
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario.to_dict()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def cadastrar_produto(dados):
    nomeProduto = _texto_obrigatorio(dados.get("nomeProduto"), "nomeProduto")

    preco = float(_texto_obrigatorio(dados.get("preco"), "preco"))
    descricao = _texto_opcional(dados.get("descricao"))
    disponivel = dados.get("disponivel") if dados.get("disponivel") is not None else True
    imagem = _texto_opcional(dados.get("imagem"))

    session = SessionLocal()
    try:
        produto = Produto(
            nomeProduto=nomeProduto,
            preco=preco,
            descricao=descricao,
            disponivel=bool(disponivel),
            imagem=imagem,
            created_at=datetime.now(),
        )
        session.add(produto)
        session.commit()
        session.refresh(produto)
        return produto.to_dict()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        
def cadastrar_favorito(dados):
    usuario_id = dados.get("usuario_id")
    produto_id = dados.get("produto_id")
    if not usuario_id or not produto_id:
        raise ValueError("Os campos 'usuario_id' e 'produto_id' são obrigatórios.")

    session = SessionLocal()
    try:
        produto = session.get(Produto, int(produto_id))
        if produto is None:
            raise ValueError(f"Produto {produto_id} não encontrado.")
        
        favorito = Favorito(usuario_id=usuario_id, produto_id=produto.id)
        session.add(favorito)
        session.commit()
        session.refresh(favorito)
        return favorito.to_dict()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        
def cadastrar_endereco(dados):
    cep = _texto_obrigatorio(dados.get("cep"), "cep")
    rua = _texto_obrigatorio(dados.get("rua"), "rua")
    numero = dados.get("numero")
    bairro = _texto_obrigatorio(dados.get("bairro"), "bairro")
    cidade = _texto_obrigatorio(dados.get("cidade"), "cidade")
    estado = _texto_obrigatorio(dados.get("estado"), "estado")
    complemento = _texto_opcional(dados.get("complemento"))
    usuario_id = dados.get("usuario_id")
    if not cep or not rua or not numero or not bairro or not cidade or not estado or not usuario_id:
        raise ValueError("Todos os campos são obrigatórios.")

    session = SessionLocal()
    try:
        endereco = Endereco(
            cep=cep,
            rua=rua,
            numero=numero,
            bairro=bairro,
            cidade=cidade,
            estado=estado,
            complemento=complemento,
            usuario_id=usuario_id,
        )
        session.add(endereco)
        session.commit()
        session.refresh(endereco)
        return endereco.to_dict()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        
        
def cadastrar_carrinho(dados):
    usuario_id = _texto_obrigatorio(dados.get("usuario_id"), "usuario_id")
    produto_id = _texto_obrigatorio(dados.get("produto_id"), "produto_id")

    session = SessionLocal()
    try:
        produto = session.get(Produto, int(produto_id))
        if produto is None:
            raise ValueError(f"produto {produto_id} não encontrado.")
        carrinho = Carrinho(usuario_id=usuario_id, produto_id=produto_id)
        session.add(carrinho)
        session.commit()
        session.refresh(carrinho)
        return carrinho.to_dict()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
        
        
def cadastrar_mensagem(dados):
    descricao = _texto_obrigatorio(dados.get("descricao"), "descricao")
    usuario_id = dados.get("usuario_id")
    if not descricao or not usuario_id:
        raise ValueError("Os campos 'descricao' e 'usuario_id' são obrigatórios.")

    session = SessionLocal()
    try:
        mensagem = Mensagem(descricao=descricao, usuario_id=usuario_id)
        session.add(mensagem)
        session.commit()
        session.refresh(mensagem)
        return mensagem.to_dict()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
