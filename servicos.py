"""
Regras de negócio e acesso ao banco (sessão + consultas).
Nas rotas só chamamos estas funções e devolvemos JSON — fica mais fácil de explicar.
"""

from datetime import datetime

from sqlalchemy import select

from database import SessionLocal
from models import Aluno, Turma, Produto, TipoAnimal, Usuario
from models import Aluno, Turma, Produto, TipoAnimal, Usuario, Animal, Funcionario, Departamento


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
        linhas = session.scalars(select(Produto).order_by(Produto.nome)).all()
        return [p.to_dict() for p in linhas]
    finally:
        session.close()


def listar_turmas():
    session = SessionLocal()
    try:
        linhas = session.scalars(select(Turma).order_by(Turma.codigo)).all()
        return [t.to_dict() for t in linhas]
    finally:
        session.close()


def listar_alunos():
    session = SessionLocal()
    try:
        linhas = session.scalars(select(Aluno).order_by(Aluno.nome)).all()
        return [a.to_dict() for a in linhas]
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

def cadastrar_turma(dados):
    nome = _texto_obrigatorio(dados.get("nome"), "nome")
    codigo = _texto_obrigatorio(dados.get("codigo"), "codigo")
    usuario_id = dados.get("usuario_id")
    if not usuario_id:
        raise ValueError("O campo 'usuario_id' é obrigatório.")

    session = SessionLocal()
    try:
        usuario = session.get(Usuario, int(usuario_id))
        if usuario is None:
            raise ValueError(f"Usuário {usuario_id} não encontrado.")

        turma = Turma(nome=nome, codigo=codigo, usuario_id=usuario.id)
        session.add(turma)
        session.commit()
        session.refresh(turma)
        return turma.to_dict()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def cadastrar_aluno(dados):
    nome = _texto_obrigatorio(dados.get("nome"), "nome")
    email = _texto_opcional(dados.get("email"))
    endereco = _texto_obrigatorio(dados.get("endereco"), "endereco")
    turma_id = dados.get("turma_id")
    if not turma_id:
        raise ValueError("O campo 'turma_id' é obrigatório.")

    session = SessionLocal()
    try:
        turma = session.get(Turma, int(turma_id))
        if turma is None:
            raise ValueError(f"Turma {turma_id} não encontrada.")

        aluno = Aluno(nome=nome, email=email, turma_id=turma.id, endereco=endereco)
        session.add(aluno)
        session.commit()
        session.refresh(aluno)
        return aluno.to_dict()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()



def cadastrar_tipoAnimal(dados):
    nome = _texto_obrigatorio(dados.get("nome"), "nome")
    session = SessionLocal()
    try:
        tipoAnimal = TipoAnimal(
            nome=nome
        )
        session.add(tipoAnimal)
        session.commit()
        session.refresh(tipoAnimal)
        return tipoAnimal.to_dict()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
